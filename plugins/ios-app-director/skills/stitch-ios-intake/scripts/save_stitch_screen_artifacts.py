#!/usr/bin/env python3
"""Save Stitch screen screenshot/HTML artifacts through one stable command."""

from __future__ import annotations

import argparse
import datetime as dt
import importlib.util
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SOURCE_LOG = "artifact-sources.json"
PENDING_QUEUE = "pending-stitch-artifacts.json"
USER_AGENT = "READY-Stitch-Intake/1.0"


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def safe_slug(value: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    if not slug:
        raise ValueError("slug must contain at least one letter or number")
    return slug


def download(url: str, destination: Path) -> int:
    destination.parent.mkdir(parents=True, exist_ok=True)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
    except urllib.error.URLError as error:
        raise RuntimeError(f"failed to download {url}: {error}") from error

    if not data:
        raise RuntimeError(f"downloaded empty artifact: {url}")

    destination.write_bytes(data)
    return len(data)


def validate_png(path: Path) -> None:
    data = path.read_bytes()[:16]
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise RuntimeError(f"{path} does not look like a PNG file")


def validate_html(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")[:4096].lower()
    if "<html" not in text and "<!doctype html" not in text:
        raise RuntimeError(f"{path} does not look like an HTML file")


def load_sources(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema": "ready.stitch-artifact-sources.v1", "artifacts": []}

    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    data.setdefault("schema", "ready.stitch-artifact-sources.v1")
    data.setdefault("artifacts", [])
    return data


def write_sources(path: Path, new_records: list[dict[str, Any]]) -> None:
    data = load_sources(path)
    artifacts = data["artifacts"]
    if not isinstance(artifacts, list):
        raise RuntimeError(f"{path} artifacts must be a list")

    by_path = {
        str(record.get("path")): record
        for record in artifacts
        if isinstance(record, dict) and record.get("path")
    }
    for record in new_records:
        by_path[record["path"]] = record

    data["updatedAt"] = utc_now()
    data["artifacts"] = [by_path[key] for key in sorted(by_path)]
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def queue_path(repo_root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def load_queue(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise RuntimeError(f"pending artifact queue not found: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        records = data
    elif isinstance(data, dict):
        records = data.get("artifacts", [])
    else:
        raise RuntimeError(f"{path} must contain a JSON object or list")

    if not isinstance(records, list):
        raise RuntimeError(f"{path} artifacts must be a list")

    normalized = []
    for record in records:
        if not isinstance(record, dict):
            raise RuntimeError(f"{path} contains a non-object artifact record")
        normalized.append(record)
    return normalized


def clear_queue(path: Path, processed: list[dict[str, Any]]) -> None:
    data = {
        "schema": "ready.stitch-pending-artifacts.v1",
        "processedAt": utc_now(),
        "artifacts": [],
        "lastProcessed": processed,
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def record_value(record: dict[str, Any], *names: str) -> Any:
    for name in names:
        value = record.get(name)
        if value is not None:
            return value
    return None


def load_manifest_module(script_dir: Path) -> Any:
    manifest_path = script_dir / "build_intake_manifest.py"
    spec = importlib.util.spec_from_file_location("build_intake_manifest", manifest_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {manifest_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules["build_intake_manifest"] = module
    spec.loader.exec_module(module)
    return module


def rebuild_manifest(repo_root: Path) -> None:
    script_dir = Path(__file__).resolve().parent
    manifest_module = load_manifest_module(script_dir)
    manifest = manifest_module.build_manifest(repo_root)
    intake_dir = repo_root / ".stitch" / "intake"
    manifest_module.write_text(
        intake_dir / manifest_module.MANIFEST_JSON,
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
    )
    manifest_module.write_text(
        intake_dir / manifest_module.MANIFEST_MD,
        manifest_module.render_markdown(manifest),
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Stitch screen screenshot/HTML artifacts and refresh the intake manifest."
    )
    parser.add_argument("--repo-root", default=".", help="Repo root containing .stitch/intake.")
    parser.add_argument("--slug", default=None, help="Stable file slug, such as 13-achievement-unlocked.")
    parser.add_argument("--screenshot-url", default=None, help="Screenshot download URL.")
    parser.add_argument("--html-url", default=None, help="HTML download URL.")
    parser.add_argument("--screen-title", default=None, help="Optional Stitch screen title for source metadata.")
    parser.add_argument("--screen-id", default=None, help="Optional Stitch screen ID for source metadata.")
    parser.add_argument(
        "--from-queue",
        nargs="?",
        const=f".stitch/intake/{PENDING_QUEUE}",
        default=None,
        help="Read artifacts from a pending JSON queue. Defaults to .stitch/intake/pending-stitch-artifacts.json when no path is supplied.",
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Save artifacts without PNG/HTML content checks.",
    )
    return parser.parse_args()


def save_artifacts(repo_root: Path, record: dict[str, Any], skip_validation: bool) -> list[dict[str, Any]]:
    intake_dir = repo_root / ".stitch" / "intake"
    slug_value = record_value(record, "slug", "fileSlug")
    if not slug_value:
        raise RuntimeError("artifact record is missing slug")

    slug = safe_slug(str(slug_value))
    screenshot_url = record_value(record, "screenshotUrl", "screenshot_url", "screenshot-url")
    html_url = record_value(record, "htmlUrl", "html_url", "html-url")
    screen_title = record_value(record, "screenTitle", "screen_title", "screen-title")
    screen_id = record_value(record, "screenId", "screen_id", "screen-id")

    if not screenshot_url and not html_url:
        raise RuntimeError(f"artifact record for {slug} needs screenshotUrl, htmlUrl, or both")

    saved: list[dict[str, Any]] = []

    if screenshot_url:
        screenshot_path = intake_dir / "screenshots" / f"{slug}.png"
        size = download(str(screenshot_url), screenshot_path)
        if not skip_validation:
            validate_png(screenshot_path)
        saved.append(
            {
                "path": screenshot_path.relative_to(repo_root).as_posix(),
                "sourceUrl": screenshot_url,
                "artifactType": "screenshot",
                "screenTitle": screen_title,
                "screenId": screen_id,
                "downloadedAt": utc_now(),
                "sizeBytes": size,
            }
        )

    if html_url:
        html_path = intake_dir / "html" / f"{slug}.html"
        size = download(str(html_url), html_path)
        if not skip_validation:
            validate_html(html_path)
        saved.append(
            {
                "path": html_path.relative_to(repo_root).as_posix(),
                "sourceUrl": html_url,
                "artifactType": "html",
                "screenTitle": screen_title,
                "screenId": screen_id,
                "downloadedAt": utc_now(),
                "sizeBytes": size,
            }
        )

    return saved


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    intake_dir = repo_root / ".stitch" / "intake"

    pending_path = queue_path(repo_root, args.from_queue) if args.from_queue else None
    if pending_path:
        artifact_records = load_queue(pending_path)
        if not artifact_records:
            print(f"No pending artifacts in {pending_path}")
            return 0
    else:
        if not args.slug:
            raise SystemExit("provide --slug, or use --from-queue")
        artifact_records = [
            {
                "slug": args.slug,
                "screenshotUrl": args.screenshot_url,
                "htmlUrl": args.html_url,
                "screenTitle": args.screen_title,
                "screenId": args.screen_id,
            }
        ]

    saved: list[dict[str, Any]] = []
    for artifact_record in artifact_records:
        saved.extend(save_artifacts(repo_root, artifact_record, args.skip_validation))

    write_sources(intake_dir / SOURCE_LOG, saved)
    rebuild_manifest(repo_root)
    if pending_path:
        clear_queue(pending_path, artifact_records)

    for record in saved:
        print(f"Saved {record['path']} ({record['sizeBytes']} bytes)")
    print("Refreshed .stitch/intake/intake-manifest.json")
    print("Refreshed .stitch/intake/intake-manifest.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
