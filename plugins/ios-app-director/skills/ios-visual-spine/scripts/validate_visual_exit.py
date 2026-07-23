#!/usr/bin/env python3
"""Validate design-first visual evidence before a maturity claim.

The validator intentionally checks evidence contracts, not aesthetic taste. A
human or vision-capable agent still performs the comparison, but promotion is
blocked when its audit is missing, internally contradictory, under-scoped, or
backed only by same-family evidence.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PROMOTION_CLAIMS = {
    "prototype_exit",
    "user_testing_readiness",
    "beta_readiness",
    "release_readiness",
}
ALLOWED_PROMOTION_TARGETS = {"prototype_visual_gate", "exact_reference"}
BLOCKING_ADOPTION_STATUSES = {
    "same_family_only",
    "partially_adopted",
    "generic_substitute",
    "parity_unproven",
    "deferred",
}
BLOCKING_COVERAGE_STATUSES = {"missing", "deferred"}


def normalized(value: Any) -> str:
    return str(value or "").strip().strip("`").lower().replace("-", "_").replace(" ", "_")


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    return value if isinstance(value, list) else [value]


def markdown_field(text: str, name: str) -> str | None:
    match = re.search(
        rf"^\s*(?:-\s*)?{re.escape(name)}\s*:\s*(.+?)\s*$",
        text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    return match.group(1).strip().strip("`") if match else None


def markdown_matrix(text: str) -> list[dict[str, str]]:
    heading = re.search(r"^##\s+Core Screen Matrix\s*$", text, re.IGNORECASE | re.MULTILINE)
    if not heading:
        return []

    lines = text[heading.end() :].splitlines()
    table_lines: list[str] = []
    for line in lines:
        if line.lstrip().startswith("## "):
            break
        if line.strip().startswith("|"):
            table_lines.append(line.strip())

    if len(table_lines) < 3:
        return []
    headers = [normalized(cell) for cell in table_lines[0].strip("|").split("|")]
    rows: list[dict[str, str]] = []
    for line in table_lines[2:]:
        cells = [cell.strip().strip("`") for cell in line.strip("|").split("|")]
        if len(cells) != len(headers):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def infer_target(audit: dict[str, Any]) -> str:
    explicit = normalized(audit.get("visualParityTarget"))
    if explicit:
        return explicit
    outcome = normalized(audit.get("outcome"))
    if "exact_reference" in outcome:
        return "exact_reference"
    if "prototype_visual_gate" in outcome:
        return "prototype_visual_gate"
    if "same_product_family" in outcome or "same_family" in outcome:
        return "same_product_family"
    return ""


def likely_local_path(value: str) -> bool:
    candidate = value.strip().strip("`")
    return candidate.startswith((".", "/")) or Path(candidate).suffix.lower() in {
        ".heic",
        ".jpeg",
        ".jpg",
        ".png",
        ".webp",
    }


def validate_evidence_paths(
    repo_root: Path,
    values: list[Any],
    label: str,
    errors: list[str],
) -> None:
    for value in values:
        if not isinstance(value, str) or not likely_local_path(value):
            continue
        path = Path(value.strip().strip("`"))
        resolved = path if path.is_absolute() else repo_root / path
        if not resolved.is_file():
            errors.append(f"{label} does not exist: {value}")


def validate(repo_root: Path, claim: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    stitch_root = repo_root / ".stitch"
    metadata_path = stitch_root / "metadata.json"
    audit_path = stitch_root / "visual-parity-audit.md"
    matrix_rows: list[dict[str, str]] = []

    if not metadata_path.is_file():
        return [f"missing structured design evidence: {metadata_path}"], warnings
    try:
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"could not read {metadata_path}: {error}"], warnings
    if not isinstance(metadata, dict):
        return [f"{metadata_path} must contain a JSON object"], warnings

    if not audit_path.is_file():
        errors.append("missing .stitch/visual-parity-audit.md")
        audit_text = ""
    else:
        audit_text = audit_path.read_text(encoding="utf-8")
        overall_status = normalized(markdown_field(audit_text, "overall_status"))
        decision = normalized(markdown_field(audit_text, "decision"))
        if overall_status != "pass":
            errors.append(f"visual audit overall_status is {overall_status or 'missing'}, not pass")
        if claim in PROMOTION_CLAIMS and decision != "promote_maturity":
            errors.append(f"visual audit decision is {decision or 'missing'}, not promote_maturity")

        matrix_rows = markdown_matrix(audit_text)
        if not matrix_rows:
            errors.append("visual audit has no parseable Core Screen Matrix rows")
        for index, row in enumerate(matrix_rows, start=1):
            screen = row.get("screen") or f"row {index}"
            status = normalized(row.get("status"))
            target = normalized(row.get("parity_target"))
            gaps = normalized(row.get("blocking_gaps"))
            if status != "pass":
                errors.append(f"{screen}: matrix status is {status or 'missing'}, not pass")
            if claim in PROMOTION_CLAIMS and target not in ALLOWED_PROMOTION_TARGETS:
                errors.append(
                    f"{screen}: parity target {target or 'missing'} cannot support maturity promotion"
                )
            if claim == "exact_reference" and target != "exact_reference":
                errors.append(f"{screen}: matrix does not claim exact-reference parity")
            if gaps not in {"", "none", "n/a", "not_applicable"}:
                errors.append(f"{screen}: blocking gaps remain: {row.get('blocking_gaps')}")
            reference = row.get("stitch_reference", "").strip()
            if not reference:
                errors.append(f"{screen}: Stitch reference is missing")
            else:
                validate_evidence_paths(
                    repo_root,
                    [reference],
                    f"{screen} Stitch reference",
                    errors,
                )
            simulator_evidence = row.get("simulator_evidence", "").strip()
            if not simulator_evidence:
                errors.append(f"{screen}: simulator evidence is missing")
            else:
                validate_evidence_paths(
                    repo_root,
                    [simulator_evidence],
                    f"{screen} simulator evidence",
                    errors,
                )

        asset_manifest = stitch_root / "intake" / "image-asset-manifest.json"
        if asset_manifest.is_file():
            try:
                asset_data = json.loads(asset_manifest.read_text(encoding="utf-8"))
                if not isinstance(asset_data, dict):
                    raise ValueError("manifest root must be an object")
                asset_paths = [
                    item.get("path")
                    for item in as_list(asset_data.get("assets"))
                    if isinstance(item, dict) and item.get("path")
                ]
            except (OSError, ValueError) as error:
                errors.append(f"could not read {asset_manifest}: {error}")
                asset_paths = []
            if asset_paths and not re.search(
                r"^##\s+Source Artwork Decisions\s*$",
                audit_text,
                flags=re.IGNORECASE | re.MULTILINE,
            ):
                errors.append("visual audit is missing Source Artwork Decisions")
            for asset_path in asset_paths:
                if asset_path not in audit_text:
                    errors.append(f"visual audit has no decision for source asset: {asset_path}")

    parity_audits = metadata.get("visualParityAudits")
    if not isinstance(parity_audits, list) or not parity_audits:
        errors.append("metadata.visualParityAudits is missing or empty")
    else:
        if matrix_rows and len(matrix_rows) < len(parity_audits):
            errors.append(
                "visual audit Core Screen Matrix has fewer rows than "
                "metadata.visualParityAudits"
            )
        for index, item in enumerate(parity_audits, start=1):
            if not isinstance(item, dict):
                errors.append(f"visualParityAudits[{index}] is not an object")
                continue
            screen = item.get("screen") or f"visualParityAudits[{index}]"
            status = normalized(item.get("status"))
            target = infer_target(item)
            references = as_list(item.get("referenceScreens") or item.get("reference"))
            evidence = as_list(item.get("simulatorEvidence") or item.get("nativeEvidence"))
            gaps = [gap for gap in as_list(item.get("blockingGaps")) if str(gap).strip()]
            if status != "pass":
                errors.append(f"{screen}: metadata parity status is {status or 'missing'}, not pass")
            if claim in PROMOTION_CLAIMS and target not in ALLOWED_PROMOTION_TARGETS:
                errors.append(
                    f"{screen}: metadata parity target {target or 'missing'} cannot support maturity promotion"
                )
            if not references:
                errors.append(f"{screen}: reference screen evidence is missing")
            if not evidence:
                errors.append(f"{screen}: simulator evidence is missing")
            if gaps:
                errors.append(f"{screen}: metadata still records blocking gaps")
            validate_evidence_paths(repo_root, references, f"{screen} reference evidence", errors)
            validate_evidence_paths(repo_root, evidence, f"{screen} simulator evidence", errors)

    for index, item in enumerate(as_list(metadata.get("designAdoptions")), start=1):
        if not isinstance(item, dict) or item.get("supersededBy"):
            continue
        status = normalized(item.get("status"))
        if status in BLOCKING_ADOPTION_STATUSES:
            scope = item.get("scope") or item.get("nativeSurfaces") or f"entry {index}"
            errors.append(f"design adoption remains {status}: {scope}")

    for index, item in enumerate(as_list(metadata.get("conceptCoverage")), start=1):
        if not isinstance(item, dict) or item.get("required") is not True:
            continue
        status = normalized(item.get("status"))
        if status in BLOCKING_COVERAGE_STATUSES or not status:
            role = item.get("role") or f"entry {index}"
            errors.append(f"required concept coverage is {status or 'missing'}: {role}")

    if not errors and claim == "exact_reference":
        for item in as_list(metadata.get("visualParityAudits")):
            if isinstance(item, dict) and infer_target(item) != "exact_reference":
                errors.append(f"{item.get('screen', 'screen')}: exact-reference evidence is required")

    return errors, warnings


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="app repository root")
    parser.add_argument(
        "--claim",
        default="prototype_exit",
        choices=sorted(PROMOTION_CLAIMS | {"exact_reference", "regression_check"}),
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).expanduser().resolve()
    errors, warnings = validate(repo_root, args.claim)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        print(f"BLOCKED: visual exit validation failed for {args.claim}")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: visual exit evidence supports {args.claim}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
