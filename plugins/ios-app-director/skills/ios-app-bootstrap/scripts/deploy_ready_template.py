#!/usr/bin/env python3
"""Safely deploy the embedded NATIVE READY app template into a repository."""

from __future__ import annotations

import argparse
import filecmp
import shutil
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = SKILL_ROOT / "templates" / "ai-app-engine"
IGNORED_PARTS = {".DS_Store", "__pycache__"}


def template_files(template_root: Path = TEMPLATE_ROOT) -> list[Path]:
    """Return the stable file inventory for a template deployment."""
    return sorted(
        path
        for path in template_root.rglob("*")
        if path.is_file()
        and not path.is_symlink()
        and not any(part in IGNORED_PARTS for part in path.parts)
        and path.suffix != ".pyc"
    )


def has_symlink_component(path: Path, repo_root: Path) -> bool:
    """Return whether an existing destination component redirects elsewhere."""
    current = path
    while current != repo_root:
        if current.is_symlink():
            return True
        current = current.parent
    return False


def deploy_template(
    repo_root: Path,
    *,
    overwrite: bool = False,
    dry_run: bool = False,
    template_root: Path = TEMPLATE_ROOT,
) -> dict[str, list[str]]:
    """Merge the embedded template into ``repo_root`` without losing user work."""
    source_root = template_root.expanduser().resolve()
    destination_root = repo_root.expanduser().resolve()

    if not source_root.is_dir():
        raise FileNotFoundError(f"Embedded READY template not found: {source_root}")
    if destination_root == source_root or source_root in destination_root.parents:
        raise ValueError("Repository root cannot be the embedded template or its child")

    result: dict[str, list[str]] = {
        "created": [],
        "unchanged": [],
        "preserved": [],
        "overwritten": [],
    }

    if not dry_run:
        destination_root.mkdir(parents=True, exist_ok=True)

    for source in template_files(source_root):
        relative_path = source.relative_to(source_root)
        destination = destination_root / relative_path
        display_path = relative_path.as_posix()

        if has_symlink_component(destination, destination_root):
            result["preserved"].append(display_path)
            continue

        if not destination.exists():
            result["created"].append(display_path)
            if not dry_run:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            continue

        if destination.is_file() and filecmp.cmp(source, destination, shallow=False):
            result["unchanged"].append(display_path)
            continue

        if overwrite and not destination.is_dir():
            result["overwritten"].append(display_path)
            if not dry_run:
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)
            continue

        result["preserved"].append(display_path)

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Deploy the iOS App Director plugin's embedded NATIVE READY app "
            "template into a repository. Existing differing files are preserved."
        )
    )
    parser.add_argument("--repo-root", required=True, type=Path)
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Replace differing existing files with template copies.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Report the deployment without writing files.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = deploy_template(
        args.repo_root,
        overwrite=args.overwrite,
        dry_run=args.dry_run,
    )
    mode = "Dry run" if args.dry_run else "Deployment"
    print(f"{mode} complete: {args.repo_root.expanduser().resolve()}")
    for status in ("created", "unchanged", "preserved", "overwritten"):
        print(f"{status}: {len(result[status])}")
        for relative_path in result[status]:
            print(f"  {relative_path}")
    if result["preserved"]:
        print("Existing differing files were preserved. Review them before using --overwrite.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
