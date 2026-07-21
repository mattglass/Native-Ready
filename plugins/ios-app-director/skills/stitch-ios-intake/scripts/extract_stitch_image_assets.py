#!/usr/bin/env python3
"""Extract and save image assets referenced by saved Stitch HTML files."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import struct
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


SCHEMA = "ready.stitch-image-asset-manifest.v1"
MANIFEST_JSON = "image-asset-manifest.json"
MANIFEST_MD = "image-asset-manifest.md"
USER_AGENT = "READY-Stitch-Image-Asset-Extractor/1.0"


class ImageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.images: list[dict[str, str]] = []
        self.title: str | None = None
        self._in_title = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "title":
            self._in_title = True
            self._title_parts = []
            return

        if tag.lower() != "img":
            return

        values = {key.lower(): value or "" for key, value in attrs}
        src = values.get("src", "").strip()
        if not src.startswith(("http://", "https://")):
            return

        self.images.append(
            {
                "src": html.unescape(src),
                "alt": html.unescape(values.get("alt", "").strip()),
                "dataAlt": html.unescape(values.get("data-alt", "").strip()),
                "class": html.unescape(values.get("class", "").strip()),
            }
        )

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title" and self._in_title:
            title = re.sub(r"\s+", " ", "".join(self._title_parts)).strip()
            self.title = title or None
            self._in_title = False


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def safe_slug(value: str, fallback: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug[:72].strip("-") or fallback


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def image_type(data: bytes, content_type: str | None) -> tuple[str, str]:
    lower_type = (content_type or "").split(";")[0].strip().lower()
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "image/png", ".png"
    if data.startswith(b"\xff\xd8"):
        return "image/jpeg", ".jpg"
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return "image/webp", ".webp"
    if data.startswith(b"GIF87a") or data.startswith(b"GIF89a"):
        return "image/gif", ".gif"
    if lower_type in {"image/png", "image/jpeg", "image/webp", "image/gif"}:
        return lower_type, {
            "image/png": ".png",
            "image/jpeg": ".jpg",
            "image/webp": ".webp",
            "image/gif": ".gif",
        }[lower_type]
    raise RuntimeError("downloaded response does not look like a supported image")


def png_dimensions(data: bytes) -> dict[str, int] | None:
    if len(data) >= 24 and data.startswith(b"\x89PNG\r\n\x1a\n"):
        width, height = struct.unpack(">II", data[16:24])
        return {"width": width, "height": height}
    return None


def jpeg_dimensions(data: bytes) -> dict[str, int] | None:
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
        if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
            if segment_length >= 7:
                height, width = struct.unpack(">HH", data[offset + 3 : offset + 7])
                return {"width": width, "height": height}
            return None
        offset += segment_length
    return None


def image_dimensions(data: bytes) -> dict[str, int] | None:
    return png_dimensions(data) or jpeg_dimensions(data)


def parse_html(path: Path) -> tuple[str | None, list[dict[str, str]]]:
    parser = ImageParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))
    return parser.title, parser.images


def download_image(url: str) -> tuple[bytes, str | None]:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
            content_type = response.headers.get("Content-Type")
    except urllib.error.URLError as error:
        raise RuntimeError(f"failed to download {url}: {error}") from error
    if not data:
        raise RuntimeError(f"downloaded empty image: {url}")
    return data, content_type


def build_records(repo_root: Path, download: bool) -> dict[str, Any]:
    intake_dir = repo_root / ".stitch" / "intake"
    html_dir = intake_dir / "html"
    asset_dir = intake_dir / "assets"
    asset_dir.mkdir(parents=True, exist_ok=True)

    seen: dict[str, dict[str, Any]] = {}
    order: list[str] = []

    for html_path in sorted(html_dir.glob("*.html")):
        title, images = parse_html(html_path)
        html_slug = safe_slug(html_path.stem, "screen")
        for index, image in enumerate(images, start=1):
            url = image["src"]
            if url not in seen:
                seen[url] = {
                    "sourceUrl": url,
                    "alt": image.get("alt") or image.get("dataAlt") or "",
                    "dataAlt": image.get("dataAlt") or "",
                    "sourceHtml": html_path.relative_to(repo_root).as_posix(),
                    "sourceHtmlTitle": title,
                    "occurrences": [],
                }
                order.append(url)

            seen[url]["occurrences"].append(
                {
                    "sourceHtml": html_path.relative_to(repo_root).as_posix(),
                    "sourceHtmlTitle": title,
                    "index": index,
                    "alt": image.get("alt") or "",
                    "dataAlt": image.get("dataAlt") or "",
                }
            )

    assets: list[dict[str, Any]] = []
    digest_to_path: dict[str, Path] = {}

    for asset_index, url in enumerate(order, start=1):
        record = seen[url]
        label = record.get("alt") or record.get("dataAlt") or urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
        slug = safe_slug(str(label), f"image-{asset_index:02d}")
        html_slug = safe_slug(Path(str(record["sourceHtml"])).stem, "screen")

        if download:
            data, content_type = download_image(url)
            media_type, extension = image_type(data, content_type)
            digest = sha256_bytes(data)
            filename = f"{asset_index:02d}-{html_slug}-{slug}{extension}"
            destination = digest_to_path.get(digest, asset_dir / filename)
            if not destination.exists():
                destination.write_bytes(data)
            digest_to_path[digest] = destination
            record.update(
                {
                    "path": destination.relative_to(repo_root).as_posix(),
                    "sha256": digest,
                    "sizeBytes": len(data),
                    "mediaType": media_type,
                    "dimensions": image_dimensions(data),
                    "downloadedAt": utc_now(),
                }
            )
        else:
            record["path"] = None
            record["sha256"] = None
            record["mediaType"] = None

        record["occurrenceCount"] = len(record["occurrences"])
        assets.append(record)

    return {
        "schema": SCHEMA,
        "generatedAt": utc_now(),
        "assetDirectory": asset_dir.relative_to(repo_root).as_posix(),
        "count": len(assets),
        "assets": assets,
    }


def render_markdown(manifest: dict[str, Any]) -> str:
    lines = [
        "# Stitch Image Asset Manifest",
        "",
        f"- schema: `{manifest['schema']}`",
        f"- generated at: `{manifest['generatedAt']}`",
        f"- asset directory: `{manifest['assetDirectory']}`",
        f"- assets: {manifest['count']}",
        "",
        "| Asset | Source HTML | Dimensions | Occurrences | Alt |",
        "| --- | --- | --- | ---: | --- |",
    ]

    for asset in manifest["assets"]:
        dimensions = asset.get("dimensions") or {}
        dim_text = f"{dimensions.get('width')}x{dimensions.get('height')}" if dimensions else "-"
        path = asset.get("path") or asset.get("sourceUrl")
        alt = str(asset.get("alt") or asset.get("dataAlt") or "-").replace("|", "\\|")
        source_html = str(asset.get("sourceHtml") or "-")
        lines.append(
            f"| `{path}` | `{source_html}` | {dim_text} | {asset.get('occurrenceCount', 0)} | {alt[:180]} |"
        )

    lines.extend(
        [
            "",
            "Use these assets as first-class visual-spine evidence. Prefer a saved source image when Stitch HTML already provides product-critical artwork; use generated substitutes only when source artwork is unavailable, unsuitable, or intentionally deferred.",
            "",
        ]
    )
    return "\n".join(lines)


def maybe_rebuild_intake_manifest(repo_root: Path) -> None:
    script = Path(__file__).with_name("build_intake_manifest.py")
    if not script.exists():
        return
    subprocess.run([sys.executable, str(script), "--repo-root", str(repo_root)], check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".", help="App repo root. Defaults to current directory.")
    parser.add_argument("--no-download", action="store_true", help="Only build the manifest of image URLs without downloading.")
    parser.add_argument("--skip-intake-manifest", action="store_true", help="Do not rebuild intake-manifest.* after extraction.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    manifest = build_records(repo_root, download=not args.no_download)
    intake_dir = repo_root / ".stitch" / "intake"
    (intake_dir / MANIFEST_JSON).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (intake_dir / MANIFEST_MD).write_text(render_markdown(manifest), encoding="utf-8")

    if not args.skip_intake_manifest:
        maybe_rebuild_intake_manifest(repo_root)

    print(f"Extracted {manifest['count']} Stitch image assets into {manifest['assetDirectory']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
