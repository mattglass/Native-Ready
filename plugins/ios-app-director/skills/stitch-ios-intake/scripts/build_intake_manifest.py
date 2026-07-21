#!/usr/bin/env python3
"""Build a stable manifest for Stitch intake artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import struct
from pathlib import Path
from typing import Any


SCHEMA = "ready.stitch-intake-manifest.v1"
MANIFEST_JSON = "intake-manifest.json"
MANIFEST_MD = "intake-manifest.md"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
HTML_SUFFIXES = {".html", ".htm"}
TEXT_SUFFIXES = {".md", ".txt", ".json"}


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def file_time(path: Path) -> str:
    return (
        dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z")
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> dict[str, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) == 24 and header.startswith(b"\x89PNG\r\n\x1a\n"):
        width, height = struct.unpack(">II", header[16:24])
        return {"width": width, "height": height}
    return None


def jpeg_dimensions(path: Path) -> dict[str, int] | None:
    data = path.read_bytes()
    if not data.startswith(b"\xff\xd8"):
        return None

    offset = 2
    while offset < len(data):
        if data[offset] != 0xFF:
            offset += 1
            continue

        while offset < len(data) and data[offset] == 0xFF:
            offset += 1
        if offset >= len(data):
            return None

        marker = data[offset]
        offset += 1
        if marker in {0xD8, 0xD9, 0x01} or 0xD0 <= marker <= 0xD7:
            continue
        if offset + 2 > len(data):
            return None

        segment_length = struct.unpack(">H", data[offset : offset + 2])[0]
        if segment_length < 2 or offset + segment_length > len(data):
            return None

        if marker in {
            0xC0,
            0xC1,
            0xC2,
            0xC3,
            0xC5,
            0xC6,
            0xC7,
            0xC9,
            0xCA,
            0xCB,
            0xCD,
            0xCE,
            0xCF,
        }:
            if segment_length >= 7:
                height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
                return {"width": width, "height": height}
            return None

        offset += segment_length
    return None


def image_dimensions(path: Path) -> dict[str, int] | None:
    suffix = path.suffix.lower()
    try:
        if suffix == ".png":
            return png_dimensions(path)
        if suffix in {".jpg", ".jpeg"}:
            return jpeg_dimensions(path)
    except OSError:
        return None
    return None


def html_title(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")[:200_000]
    except OSError:
        return None

    match = re.search(r"<title[^>]*>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return None

    title = html.unescape(match.group(1))
    title = re.sub(r"\s+", " ", title).strip()
    return title or None


def category_for(path: Path, intake_dir: Path) -> str:
    suffix = path.suffix.lower()
    relative_parts = path.relative_to(intake_dir).parts
    parent_parts = {part.lower() for part in relative_parts[:-1]}

    if "assets" in parent_parts:
        return "assets"
    if "screenshots" in parent_parts or suffix in IMAGE_SUFFIXES:
        return "screenshots"
    if "html" in parent_parts or suffix in HTML_SUFFIXES:
        return "html"
    if path.name == "design-intake.md":
        return "records"
    if suffix in TEXT_SUFFIXES:
        return "notes"
    return "other"


def artifact_record(path: Path, repo_root: Path, intake_dir: Path) -> dict[str, Any]:
    stat = path.stat()
    category = category_for(path, intake_dir)
    record: dict[str, Any] = {
        "path": path.relative_to(repo_root).as_posix(),
        "category": category,
        "extension": path.suffix.lower(),
        "sizeBytes": stat.st_size,
        "modifiedAt": file_time(path),
        "sha256": sha256(path),
    }

    dimensions = image_dimensions(path)
    if dimensions:
        record["dimensions"] = dimensions

    if category == "html":
        title = html_title(path)
        if title:
            record["title"] = title

    return record


def discover_artifacts(repo_root: Path, intake_dir: Path) -> list[dict[str, Any]]:
    excluded = {MANIFEST_JSON, MANIFEST_MD, ".DS_Store"}
    artifacts = []
    for path in sorted(intake_dir.rglob("*")):
        if not path.is_file():
            continue
        if path.name in excluded:
            continue
        if any(part.startswith(".") and part != ".stitch" for part in path.relative_to(repo_root).parts):
            continue
        artifacts.append(artifact_record(path, repo_root, intake_dir))
    return artifacts


def summarize_counts(artifacts: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for artifact in artifacts:
        category = str(artifact["category"])
        counts[category] = counts.get(category, 0) + 1
    return dict(sorted(counts.items()))


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Stitch Intake Manifest",
        "",
        f"- schema: `{manifest['schema']}`",
        f"- generated at: `{manifest['generatedAt']}`",
        f"- intake dir: `{manifest['intakeDir']}`",
        "",
        "## Counts",
        "",
    ]

    counts: dict[str, int] = manifest["counts"]
    if counts:
        for category, count in counts.items():
            lines.append(f"- {category}: {count}")
    else:
        lines.append("- no intake artifacts found")

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "| Category | Path | Size | Modified | Details |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )

    for artifact in manifest["artifacts"]:
        details = []
        dimensions = artifact.get("dimensions")
        if dimensions:
            details.append(f"{dimensions['width']}x{dimensions['height']}")
        if artifact.get("title"):
            details.append(str(artifact["title"]).replace("|", "\\|"))
        if not details:
            details.append("-")
        lines.append(
            "| {category} | `{path}` | {size} | `{modified}` | {details} |".format(
                category=artifact["category"],
                path=artifact["path"],
                size=artifact["sizeBytes"],
                modified=artifact["modifiedAt"],
                details=", ".join(details),
            )
        )

    lines.extend(
        [
            "",
            "Use this file as the stable index for refreshed Stitch screenshots, HTML exports, notes, and design-intake records.",
            "",
        ]
    )
    return "\n".join(lines)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_manifest(repo_root: Path) -> dict[str, Any]:
    intake_dir = repo_root / ".stitch" / "intake"
    intake_dir.mkdir(parents=True, exist_ok=True)
    artifacts = discover_artifacts(repo_root, intake_dir)
    return {
        "schema": SCHEMA,
        "generatedAt": utc_now(),
        "repoRoot": str(repo_root),
        "intakeDir": ".stitch/intake",
        "counts": summarize_counts(artifacts),
        "artifacts": artifacts,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Stitch intake manifest files.")
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repo root containing .stitch/intake. Defaults to the current directory.",
    )
    parser.add_argument(
        "--json-path",
        default=None,
        help="Optional output path for JSON manifest. Defaults to .stitch/intake/intake-manifest.json.",
    )
    parser.add_argument(
        "--md-path",
        default=None,
        help="Optional output path for Markdown manifest. Defaults to .stitch/intake/intake-manifest.md.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    manifest = build_manifest(repo_root)

    default_dir = repo_root / ".stitch" / "intake"
    json_path = Path(args.json_path).expanduser().resolve() if args.json_path else default_dir / MANIFEST_JSON
    md_path = Path(args.md_path).expanduser().resolve() if args.md_path else default_dir / MANIFEST_MD

    write_text(json_path, json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    write_text(md_path, render_markdown(manifest))

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(f"Artifacts: {len(manifest['artifacts'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
