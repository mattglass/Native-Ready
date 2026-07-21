#!/usr/bin/env python3
"""Replace section 9 of .stitch/APP.md with a generated feature map."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


HEADING_RE = re.compile(r"^##\s+9\.\s+App Feature Inventory & Requirements Map\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-md", required=True, help="Path to .stitch/APP.md")
    parser.add_argument("--feature-map", required=True, help="Markdown file containing section 9 content")
    parser.add_argument("--dry-run", action="store_true", help="Print result instead of writing APP.md")
    return parser.parse_args()


def normalize_feature_map(raw: str) -> str:
    lines = raw.strip().splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and HEADING_RE.match(lines[0].strip()):
        lines = lines[1:]
    return "## 9. App Feature Inventory & Requirements Map\n\n" + "\n".join(lines).strip() + "\n"


def replace_section(app_text: str, feature_map: str) -> str:
    lines = app_text.splitlines(keepends=True)
    start = None
    for index, line in enumerate(lines):
        if HEADING_RE.match(line.strip()):
            start = index
            break

    replacement = normalize_feature_map(feature_map)

    if start is None:
        suffix = "" if app_text.endswith("\n") else "\n"
        return app_text + suffix + "\n" + replacement

    end = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("## ") and not stripped.startswith("### "):
            end = index
            break

    prefix = "".join(lines[:start]).rstrip() + "\n\n"
    suffix = "".join(lines[end:]).lstrip("\n")
    return prefix + replacement + ("\n" + suffix if suffix else "")


def main() -> None:
    args = parse_args()
    app_path = Path(args.app_md)
    feature_path = Path(args.feature_map)

    app_text = app_path.read_text(encoding="utf-8")
    feature_text = feature_path.read_text(encoding="utf-8")
    result = replace_section(app_text, feature_text)

    if args.dry_run:
        print(result)
        return

    app_path.write_text(result, encoding="utf-8")
    print(f"Updated {app_path}")


if __name__ == "__main__":
    main()
