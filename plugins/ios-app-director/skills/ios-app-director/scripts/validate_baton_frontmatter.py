#!/usr/bin/env python3
"""Validate READY `.stitch/next-prompt.md` frontmatter."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CORE_REQUIRED = [
    "platform",
    "roadmap_task",
    "task_type",
    "feature",
    "screen",
    "mode",
    "device",
    "app_maturity",
]

RECOMMENDED = [
    "destination",
    "validation_tier",
    "regression_scope",
    "evidence_expectation",
]

KEY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
TEMPLATE_PLACEHOLDER_RE = re.compile(
    r"\[[A-Z][A-Z0-9_]*(?:\s*/\s*[A-Z][A-Z0-9_]*)*\]"
)


def validate(
    path: Path,
    *,
    allow_placeholders: bool = False,
) -> tuple[list[str], list[str], dict[str, str]]:
    errors: list[str] = []
    warnings: list[str] = []
    fields: dict[str, str] = {}

    if not path.exists():
        return [f"missing baton file: {path}"], warnings, fields

    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return ["baton must start with frontmatter delimiter `---`"], warnings, fields

    try:
        end = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return ["baton frontmatter must end with delimiter `---`"], warnings, fields

    for line_no, raw in enumerate(lines[1:end], start=2):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0].isspace():
            errors.append(f"line {line_no}: frontmatter key must not be indented: {raw!r}")
            continue
        if ":" not in raw:
            errors.append(f"line {line_no}: frontmatter line is missing `:`: {raw!r}")
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not KEY_RE.match(key):
            errors.append(f"line {line_no}: invalid frontmatter key `{key}`")
            continue
        if key in fields:
            errors.append(f"line {line_no}: duplicate frontmatter key `{key}`")
            continue
        fields[key] = value

    for key in CORE_REQUIRED:
        if not fields.get(key):
            errors.append(f"missing required frontmatter field `{key}`")

    for key in RECOMMENDED:
        if not fields.get(key):
            warnings.append(f"recommended frontmatter field `{key}` is missing")

    if not allow_placeholders:
        for key, value in fields.items():
            placeholders = TEMPLATE_PLACEHOLDER_RE.findall(value)
            if placeholders:
                errors.append(
                    f"frontmatter field `{key}` contains unresolved template "
                    f"placeholder(s): {', '.join(placeholders)}"
                )

    return errors, warnings, fields


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="READY app repo root")
    parser.add_argument("--file", default=".stitch/next-prompt.md", help="baton path")
    parser.add_argument("--json", action="store_true", help="print JSON result")
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="allow unresolved [PLACEHOLDER] values when validating the source template",
    )
    args = parser.parse_args()

    path = (Path(args.repo_root) / args.file).resolve()
    errors, warnings, fields = validate(
        path,
        allow_placeholders=args.allow_placeholders,
    )
    result = {
        "file": str(path),
        "ok": not errors,
        "allowPlaceholders": args.allow_placeholders,
        "errors": errors,
        "warnings": warnings,
        "fields": fields,
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if errors:
            print("Baton frontmatter errors:")
            for item in errors:
                print(f"- {item}")
        if warnings:
            print("Baton frontmatter warnings:")
            for item in warnings:
                print(f"- {item}")
        if not errors and not warnings:
            print(f"Baton frontmatter OK: {path}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
