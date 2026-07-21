#!/usr/bin/env python3
"""Render a non-blocking READY bootstrap status receipt."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PLACEHOLDER = re.compile(r"\[[A-Z][A-Z0-9_ -]*\]")


def usable(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text or PLACEHOLDER.search(text):
        return None
    return text


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return data if isinstance(data, dict) else {}


def deep_get(data: dict[str, Any], *keys: str) -> Any:
    current: Any = data
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def parse_frontmatter(path: Path) -> dict[str, str]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    fields: dict[str, str] = {}
    for line in parts[1].splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip("\"'")
    return fields


def first_usable(*values: Any, fallback: str = "unknown") -> str:
    for value in values:
        candidate = usable(value)
        if candidate:
            return candidate
    return fallback


def open_risks(metadata: dict[str, Any]) -> list[str]:
    result: list[str] = []
    risks = metadata.get("riskRegister", [])
    if not isinstance(risks, list):
        return result
    for risk in risks:
        if not isinstance(risk, dict) or risk.get("status") in {"closed", "resolved"}:
            continue
        identifier = first_usable(risk.get("id"), fallback="unidentified-risk")
        note = first_usable(risk.get("note"), risk.get("surface"), fallback="No detail recorded")
        result.append(f"{identifier}: {note}")
    return result


def render_receipt(
    repo_root: Path,
    *,
    first_build_result: str,
    baton_validation: str,
    stitch_status: str,
    build_evidence: str | None,
    notes: list[str],
    scheme_discovered: str = "unknown",
) -> str:
    metadata = load_json(repo_root / ".stitch" / "metadata.json")
    baton = parse_frontmatter(repo_root / ".stitch" / "next-prompt.md")
    app = metadata.get("app", {}) if isinstance(metadata.get("app"), dict) else {}
    scaffold = metadata.get("nativeScaffold", {})
    scaffold = scaffold if isinstance(scaffold, dict) else {}

    app_name = first_usable(app.get("name"), fallback=repo_root.name)
    native_project_path = first_usable(
        app.get("nativeProjectPath"), scaffold.get("projectPath"), fallback="unknown"
    )
    native_target = first_usable(app.get("nativeTarget"), scaffold.get("target"))
    native_test_target = first_usable(
        app.get("nativeTestTarget"), scaffold.get("plannedTestTarget"),
        fallback=f"{native_target}Tests" if native_target != "unknown" else "unknown",
    )
    native_scheme = first_usable(scaffold.get("scheme"), native_target)
    bundle_identifier = first_usable(app.get("bundleIdentifier"), scaffold.get("bundleIdentifier"))
    project_exists = (
        native_project_path != "unknown" and (repo_root / native_project_path).exists()
    )

    stitch_project_id = first_usable(
        deep_get(metadata, "stitchOperations", "activeProjectId"),
        deep_get(metadata, "stitchProjects", "primaryConceptProject", "projectId"),
    )
    if stitch_status == "auto":
        stitch_status = "configured" if stitch_project_id != "unknown" else "unknown_or_not_in_scope"

    active_task = first_usable(baton.get("roadmap_task"))
    active_task_type = first_usable(baton.get("task_type"))
    delivery_baton_ready = (
        active_task != "unknown"
        and active_task_type not in {"unknown", "native_scaffold"}
    )
    risks = open_risks(metadata)
    if not project_exists:
        risks.append("native-project: recorded native project was not found")
    if scheme_discovered != "yes":
        risks.append(f"scheme-discovery: {scheme_discovered}")
    if first_build_result != "succeeded":
        risks.append(f"first-build: {first_build_result}")
    if baton_validation != "passed":
        risks.append(f"baton-validation: {baton_validation}")
    elif not delivery_baton_ready:
        risks.append(
            "active-baton: validated baton does not identify the next delivery task"
        )
    risks.extend(note for note in notes if note.strip())

    if (
        project_exists
        and scheme_discovered == "yes"
        and first_build_result == "succeeded"
        and baton_validation == "passed"
        and delivery_baton_ready
    ):
        completion_state = "ready_for_delivery"
        next_prompt = (
            "/goal Build autonomously toward the v1 app until the planned features work, "
            "the roadmap is reconciled, validation evidence is captured, and the app is ready "
            "for real user testing. Use $ios-app-director to continue from the active baton."
        )
    elif not project_exists:
        completion_state = "blocked"
        next_prompt = (
            "Use $ios-app-bootstrap to resume from docs/bootstrap-receipt.md and create or repair "
            "the native scaffold before delivery."
        )
    else:
        completion_state = "partial"
        next_prompt = (
            "Use $ios-app-bootstrap to resume from docs/bootstrap-receipt.md and resolve the "
            "incomplete bootstrap checks without discarding completed work."
        )

    risk_lines = "\n".join(f"- {risk}" for risk in risks) or "- None recorded"
    evidence = build_evidence or "not recorded"
    provisional = "yes" if bundle_identifier.startswith("com.example.") else "no"
    generated = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    return f"""# READY Bootstrap Receipt

> This receipt reports setup state. Missing receipt fields do not block independent work.

## Result

- Completion state: `{completion_state}`
- Generated: `{generated}`
- Repo root: `{repo_root}`
- App: `{app_name}`

## Design

- Stitch status: `{stitch_status}`
- Stitch project ID: `{stitch_project_id}`

## Native Scaffold

- Project path: `{native_project_path}`
- Project exists: `{str(project_exists).lower()}`
- Target: `{native_target}`
- Planned test target: `{native_test_target}`
- Scheme: `{native_scheme}`
- Bundle identifier: `{bundle_identifier}`
- Provisional `com.example` identifier: `{provisional}`

## Validation

- Scheme discovered: `{scheme_discovered}`
- First build/launch: `{first_build_result}`
- Build evidence: `{evidence}`
- Active roadmap task: `{active_task}`
- Active task type: `{active_task_type}`
- Baton validation: `{baton_validation}`

## Unresolved Setup Risks

{risk_lines}

## Exact Next Prompt

```text
{next_prompt}
```
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument(
        "--first-build-result",
        choices=("succeeded", "failed", "not_run", "unknown"),
        default="unknown",
    )
    parser.add_argument(
        "--baton-validation",
        choices=("passed", "failed", "not_run", "unknown"),
        default="unknown",
    )
    parser.add_argument(
        "--stitch-status",
        choices=("auto", "configured", "unavailable", "not_in_scope", "partial"),
        default="auto",
    )
    parser.add_argument("--build-evidence")
    parser.add_argument(
        "--scheme-discovered",
        choices=("yes", "no", "unknown"),
        default="unknown",
    )
    parser.add_argument("--note", action="append", default=[])
    parser.add_argument("--output", type=Path, default=Path("docs/bootstrap-receipt.md"))
    return parser


def main() -> int:
    args = build_parser().parse_args()
    repo_root = args.repo_root.expanduser().resolve()
    output = args.output if args.output.is_absolute() else repo_root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    receipt = render_receipt(
        repo_root,
        first_build_result=args.first_build_result,
        baton_validation=args.baton_validation,
        stitch_status=args.stitch_status,
        build_evidence=args.build_evidence,
        notes=args.note,
        scheme_discovered=args.scheme_discovered,
    )
    output.write_text(receipt, encoding="utf-8")

    metadata_path = repo_root / ".stitch" / "metadata.json"
    metadata = load_json(metadata_path)
    if metadata:
        completion_match = re.search(r"Completion state: `([^`]+)`", receipt)
        setup_run = metadata.setdefault("setupRun", {})
        if isinstance(setup_run, dict):
            setup_run["schemeDiscovered"] = args.scheme_discovered
            setup_run["firstBuildResult"] = args.first_build_result
            setup_run["firstLaunchEvidence"] = args.build_evidence
            setup_run["batonValidation"] = args.baton_validation
            setup_run["completionState"] = (
                completion_match.group(1) if completion_match else "partial"
            )
            try:
                receipt_path = str(output.relative_to(repo_root))
            except ValueError:
                receipt_path = str(output)
            setup_run["receipt"] = receipt_path
            metadata_path.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
