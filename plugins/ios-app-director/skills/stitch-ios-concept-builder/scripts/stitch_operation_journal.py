#!/usr/bin/env python3
"""Maintain a small local safety journal for Stitch mutations.

The journal protects project identity and ambiguous-operation recovery. It does
not decide what an app should contain or how a Stitch prompt should be written.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
JOURNAL_RELATIVE_PATH = Path(".stitch/operations/current.json")
PROJECT_SOURCES = {
    "user_input",
    "repo_metadata",
    "exact_discovery",
    "created_current_run",
}
OPERATION_KINDS = {
    "generate_screen",
    "edit_screens",
    "generate_variants",
    "create_design_system",
    "apply_design_system",
}
FAILURE_CLASSES = {
    "none",
    "invalid_argument",
    "timeout_or_connection",
    "auth_required",
    "not_found",
    "rate_limited",
    "server_error",
}
COVERAGE_STATUSES = {"live", "artifact_only", "missing", "deferred", "not_needed"}
TRANSITIONS = {
    "prepared": {"submitted", "failed"},
    "submitted": {"polling", "succeeded", "ambiguous_timeout", "failed"},
    "polling": {"polling", "succeeded", "ambiguous_timeout", "failed"},
    "ambiguous_timeout": {
        "polling",
        "succeeded",
        "replacement_authorized",
        "abandoned",
    },
    "replacement_authorized": {"succeeded", "abandoned"},
    "succeeded": set(),
    "failed": set(),
    "abandoned": set(),
}


class JournalError(ValueError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def journal_path(repo_root: Path) -> Path:
    return repo_root / JOURNAL_RELATIVE_PATH


def new_journal(
    run_id: str,
    project_title: str,
    required_capabilities: list[str] | None = None,
    optional_capabilities: list[str] | None = None,
) -> dict[str, Any]:
    capabilities: dict[str, dict[str, str]] = {}
    for name in required_capabilities or []:
        capabilities[name] = {"scope": "required", "availability": "unknown"}
    for name in optional_capabilities or []:
        capabilities[name] = {"scope": "optional", "availability": "unknown"}
    return {
        "schemaVersion": SCHEMA_VERSION,
        "runId": run_id,
        "requestedProjectTitle": project_title,
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
        "activeProject": None,
        "referenceProjects": [],
        "capabilities": capabilities,
        "operations": [],
    }


def load_journal(repo_root: Path) -> dict[str, Any]:
    path = journal_path(repo_root)
    if not path.exists():
        raise JournalError(f"journal does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schemaVersion") != SCHEMA_VERSION:
        raise JournalError("unsupported journal schema version")
    return data


def save_journal(repo_root: Path, journal: dict[str, Any]) -> Path:
    path = journal_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    journal["updatedAt"] = now_iso()
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(journal, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
    return path


def adopt_project(
    journal: dict[str, Any],
    project_id: str,
    source: str,
    title: str | None = None,
) -> None:
    if source not in PROJECT_SOURCES:
        raise JournalError(f"unsupported project source: {source}")
    project_id = project_id.strip()
    if not project_id:
        raise JournalError("project ID must not be empty")
    active = journal.get("activeProject")
    if active and active.get("id") != project_id:
        raise JournalError(
            f"active project is already {active.get('id')}; refusing unrelated {project_id}"
        )
    if active:
        return
    journal["activeProject"] = {
        "id": project_id,
        "title": title,
        "source": source,
        "adoptedAt": now_iso(),
    }


def ensure_project_allowed(journal: dict[str, Any], project_id: str) -> None:
    active = journal.get("activeProject")
    if not active:
        raise JournalError("no active Stitch project has been adopted")
    if active.get("id") != project_id:
        raise JournalError(
            f"project {project_id} is outside current-run provenance; active project is {active.get('id')}"
        )


def register_reference_project(
    journal: dict[str, Any],
    project_id: str,
    source: str,
    title: str | None = None,
) -> None:
    if source not in PROJECT_SOURCES - {"created_current_run"}:
        raise JournalError(f"unsupported reference project source: {source}")
    project_id = project_id.strip()
    if not project_id:
        raise JournalError("project ID must not be empty")
    active = journal.get("activeProject")
    if active and active.get("id") == project_id:
        return
    references = journal.setdefault("referenceProjects", [])
    if any(item.get("id") == project_id for item in references):
        return
    references.append(
        {
            "id": project_id,
            "title": title,
            "source": source,
            "registeredAt": now_iso(),
        }
    )


def ensure_project_known(journal: dict[str, Any], project_id: str) -> None:
    active = journal.get("activeProject")
    if active and active.get("id") == project_id:
        return
    if any(
        item.get("id") == project_id
        for item in journal.get("referenceProjects", [])
    ):
        return
    raise JournalError(f"project {project_id} is outside current-run provenance")


def find_operation(journal: dict[str, Any], operation_id: str) -> dict[str, Any]:
    for operation in journal.get("operations", []):
        if operation.get("id") == operation_id:
            return operation
    raise JournalError(f"unknown operation: {operation_id}")


def prepare_operation(
    journal: dict[str, Any],
    operation_id: str,
    kind: str,
    project_id: str,
    screen_role: str,
    baseline_screen_ids: list[str] | None = None,
    replacement_for: str | None = None,
) -> None:
    if kind not in OPERATION_KINDS:
        raise JournalError(f"unsupported operation kind: {kind}")
    if any(item.get("id") == operation_id for item in journal.get("operations", [])):
        raise JournalError(f"operation already exists: {operation_id}")
    ensure_project_allowed(journal, project_id)

    unresolved = [
        item
        for item in journal.get("operations", [])
        if item.get("projectId") == project_id
        and item.get("kind") == kind
        and item.get("screenRole") == screen_role
        and item.get("status") in {
            "prepared",
            "submitted",
            "polling",
            "ambiguous_timeout",
            "replacement_authorized",
        }
    ]
    if unresolved:
        if not replacement_for:
            raise JournalError(
                f"unresolved operation already exists for {screen_role}; link an authorized replacement"
            )
        original = find_operation(journal, replacement_for)
        if original not in unresolved or original.get("status") != "replacement_authorized":
            raise JournalError("replacement target is not authorized")

    journal.setdefault("operations", []).append(
        {
            "id": operation_id,
            "kind": kind,
            "projectId": project_id,
            "screenRole": screen_role,
            "baselineScreenIds": sorted(set(baseline_screen_ids or [])),
            "status": "prepared",
            "failureClass": "none",
            "replacementFor": replacement_for,
            "createdAt": now_iso(),
            "updatedAt": now_iso(),
            "newScreenIds": [],
            "notes": [],
        }
    )


def transition_operation(
    journal: dict[str, Any],
    operation_id: str,
    status: str,
    failure_class: str = "none",
    new_screen_ids: list[str] | None = None,
    note: str | None = None,
) -> None:
    if failure_class not in FAILURE_CLASSES:
        raise JournalError(f"unsupported failure class: {failure_class}")
    operation = find_operation(journal, operation_id)
    current = operation.get("status")
    if status not in TRANSITIONS.get(current, set()):
        raise JournalError(f"invalid transition: {current} -> {status}")
    effective_failure = failure_class
    if (
        effective_failure == "none"
        and status != "succeeded"
        and operation.get("failureClass") != "none"
    ):
        effective_failure = operation["failureClass"]
    if status == "ambiguous_timeout" and effective_failure != "timeout_or_connection":
        raise JournalError("ambiguous_timeout requires timeout_or_connection")
    if status == "failed" and effective_failure == "none":
        raise JournalError("failed operations require a failure class")
    if status == "succeeded" and effective_failure != "none":
        raise JournalError("succeeded operations cannot retain a failure class")

    operation["status"] = status
    operation["failureClass"] = effective_failure
    operation["updatedAt"] = now_iso()
    if new_screen_ids:
        operation["newScreenIds"] = sorted(
            set(operation.get("newScreenIds", []) + new_screen_ids)
        )
    if note:
        operation.setdefault("notes", []).append(note)


def set_capability(
    journal: dict[str, Any], name: str, scope: str, availability: str
) -> None:
    if scope not in {"required", "optional", "not_in_scope"}:
        raise JournalError(f"unsupported capability scope: {scope}")
    if availability not in {"unknown", "ready", "unavailable"}:
        raise JournalError(f"unsupported capability availability: {availability}")
    journal.setdefault("capabilities", {})[name] = {
        "scope": scope,
        "availability": availability,
    }


def audit_journal(journal: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    info: list[str] = []
    active = journal.get("activeProject")
    active_id = active.get("id") if active else None

    for operation in journal.get("operations", []):
        if operation.get("projectId") != active_id:
            errors.append(
                f"operation {operation.get('id')} targets a non-active project"
            )
        if operation.get("status") == "ambiguous_timeout":
            warnings.append(
                f"operation {operation.get('id')} needs recovery or replacement authorization"
            )

    for name, capability in journal.get("capabilities", {}).items():
        scope = capability.get("scope")
        availability = capability.get("availability")
        if scope == "required" and availability == "unavailable":
            errors.append(f"required capability unavailable: {name}")
        elif scope in {"optional", "not_in_scope"} and availability == "unavailable":
            info.append(f"ignored unavailable {scope} capability: {name}")

    return errors, warnings, info


def audit_concept_coverage(
    records: list[dict[str, Any]],
) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    seen_roles: set[str] = set()
    for index, record in enumerate(records):
        role = str(record.get("role", "")).strip()
        label = role or f"record {index + 1}"
        if not role:
            errors.append(f"concept coverage {label} has no role")
            continue
        if role in seen_roles:
            errors.append(f"duplicate concept coverage role: {role}")
        seen_roles.add(role)

        status = record.get("status")
        if status not in COVERAGE_STATUSES:
            errors.append(f"concept coverage {role} has unsupported status: {status}")
            continue
        required = bool(record.get("required", False))
        if required and status == "missing" and not record.get("linkedTask"):
            errors.append(f"required missing concept role has no expansion task: {role}")
        if required and status == "deferred" and not str(record.get("note", "")).strip():
            errors.append(f"required deferred concept role has no reason: {role}")
        if status == "live" and not record.get("screenIds"):
            warnings.append(f"live concept role has no screen ID provenance: {role}")
        if status == "artifact_only" and not record.get("artifactPaths"):
            warnings.append(f"artifact-only concept role has no artifact path: {role}")
    return errors, warnings


def command_init(args: argparse.Namespace) -> int:
    path = journal_path(args.repo_root)
    if path.exists() and not args.replace:
        raise JournalError(f"journal already exists: {path}; reuse it or pass --replace")
    journal = new_journal(
        args.run_id,
        args.project_title,
        args.required_capability,
        args.optional_capability,
    )
    save_journal(args.repo_root, journal)
    print(path)
    return 0


def command_adopt(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    adopt_project(journal, args.project_id, args.source, args.title)
    save_journal(args.repo_root, journal)
    return 0


def command_register_reference(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    register_reference_project(journal, args.project_id, args.source, args.title)
    save_journal(args.repo_root, journal)
    return 0


def command_prepare(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    project_id = args.project_id or (journal.get("activeProject") or {}).get("id")
    if not project_id:
        raise JournalError("project ID is required before preparing an operation")
    prepare_operation(
        journal,
        args.operation_id,
        args.kind,
        project_id,
        args.screen_role,
        args.baseline_screen_id,
        args.replacement_for,
    )
    save_journal(args.repo_root, journal)
    return 0


def command_transition(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    transition_operation(
        journal,
        args.operation_id,
        args.status,
        args.failure_class,
        args.new_screen_id,
        args.note,
    )
    save_journal(args.repo_root, journal)
    return 0


def command_capability(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    set_capability(journal, args.name, args.scope, args.availability)
    save_journal(args.repo_root, journal)
    return 0


def command_audit(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    errors, warnings, info = audit_journal(journal)
    metadata_path = args.repo_root / ".stitch/metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        coverage_errors, coverage_warnings = audit_concept_coverage(
            metadata.get("conceptCoverage", [])
        )
        errors.extend(coverage_errors)
        warnings.extend(coverage_warnings)
    for item in errors:
        print(f"ERROR: {item}")
    for item in warnings:
        print(f"WARNING: {item}")
    for item in info:
        print(f"INFO: {item}")
    return 1 if errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init")
    init.add_argument("--repo-root", type=Path, default=Path.cwd())
    init.add_argument("--run-id", required=True)
    init.add_argument("--project-title", required=True)
    init.add_argument("--required-capability", action="append", default=[])
    init.add_argument("--optional-capability", action="append", default=[])
    init.add_argument("--replace", action="store_true")
    init.set_defaults(func=command_init)

    adopt = subparsers.add_parser("adopt-project")
    adopt.add_argument("--repo-root", type=Path, default=Path.cwd())
    adopt.add_argument("--project-id", required=True)
    adopt.add_argument("--source", choices=sorted(PROJECT_SOURCES), required=True)
    adopt.add_argument("--title")
    adopt.set_defaults(func=command_adopt)

    reference = subparsers.add_parser("register-reference-project")
    reference.add_argument("--repo-root", type=Path, default=Path.cwd())
    reference.add_argument("--project-id", required=True)
    reference.add_argument(
        "--source",
        choices=sorted(PROJECT_SOURCES - {"created_current_run"}),
        required=True,
    )
    reference.add_argument("--title")
    reference.set_defaults(func=command_register_reference)

    prepare = subparsers.add_parser("prepare-operation")
    prepare.add_argument("--repo-root", type=Path, default=Path.cwd())
    prepare.add_argument("--operation-id", required=True)
    prepare.add_argument("--kind", choices=sorted(OPERATION_KINDS), required=True)
    prepare.add_argument("--project-id")
    prepare.add_argument("--screen-role", required=True)
    prepare.add_argument("--baseline-screen-id", action="append", default=[])
    prepare.add_argument("--replacement-for")
    prepare.set_defaults(func=command_prepare)

    transition = subparsers.add_parser("transition")
    transition.add_argument("--repo-root", type=Path, default=Path.cwd())
    transition.add_argument("--operation-id", required=True)
    transition.add_argument("--status", choices=sorted(TRANSITIONS), required=True)
    transition.add_argument(
        "--failure-class", choices=sorted(FAILURE_CLASSES), default="none"
    )
    transition.add_argument("--new-screen-id", action="append", default=[])
    transition.add_argument("--note")
    transition.set_defaults(func=command_transition)

    capability = subparsers.add_parser("set-capability")
    capability.add_argument("--repo-root", type=Path, default=Path.cwd())
    capability.add_argument("--name", required=True)
    capability.add_argument(
        "--scope", choices=["required", "optional", "not_in_scope"], required=True
    )
    capability.add_argument(
        "--availability", choices=["unknown", "ready", "unavailable"], required=True
    )
    capability.set_defaults(func=command_capability)

    audit = subparsers.add_parser("audit")
    audit.add_argument("--repo-root", type=Path, default=Path.cwd())
    audit.set_defaults(func=command_audit)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (JournalError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
