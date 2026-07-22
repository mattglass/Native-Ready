#!/usr/bin/env python3
"""Maintain a small local safety journal for Stitch mutations.

The journal protects project identity and ambiguous-operation recovery. It does
not decide what an app should contain or how a Stitch prompt should be written.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1
JOURNAL_RELATIVE_PATH = Path(".stitch/operations/current.json")
DEFAULT_MAX_REPLACEMENT_ATTEMPTS = 1
DEFAULT_DECOMPOSITION_THRESHOLD = 2
DEFAULT_REPLACEMENT_MODE = "autonomous"
LEGACY_REPLACEMENT_MODE = "manual"
REPLACEMENT_MODES = {"autonomous", "manual"}
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
    "prepared": {"submitted", "failed", "abandoned"},
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
UNRESOLVED_STATUSES = {
    "prepared",
    "submitted",
    "polling",
    "ambiguous_timeout",
    "replacement_authorized",
}


class JournalError(ValueError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def journal_path(repo_root: Path) -> Path:
    return repo_root / JOURNAL_RELATIVE_PATH


def validate_recovery_policy(
    max_replacement_attempts: int,
    decomposition_threshold: int,
    replacement_mode: str,
) -> None:
    if max_replacement_attempts < 0:
        raise JournalError("max replacement attempts must be zero or greater")
    if decomposition_threshold < 2:
        raise JournalError("decomposition threshold must be two or greater")
    if replacement_mode not in REPLACEMENT_MODES:
        raise JournalError(f"unsupported replacement mode: {replacement_mode}")


def recovery_policy(journal: dict[str, Any]) -> dict[str, Any]:
    policy = journal.get("recoveryPolicy") or {}
    try:
        max_replacement_attempts = int(
            policy.get(
                "maxReplacementAttempts", DEFAULT_MAX_REPLACEMENT_ATTEMPTS
            )
        )
        decomposition_threshold = int(
            policy.get("decompositionThreshold", DEFAULT_DECOMPOSITION_THRESHOLD)
        )
    except (TypeError, ValueError) as error:
        raise JournalError("recovery policy values must be integers") from error
    # Journals created before recoveryPolicy existed required a user decision.
    # Keep that behavior until the journal is explicitly configured or replaced.
    replacement_mode = str(policy.get("replacementMode", LEGACY_REPLACEMENT_MODE))
    validate_recovery_policy(
        max_replacement_attempts, decomposition_threshold, replacement_mode
    )
    return {
        "maxReplacementAttempts": max_replacement_attempts,
        "decompositionThreshold": decomposition_threshold,
        "replacementMode": replacement_mode,
    }


def set_recovery_policy(
    journal: dict[str, Any],
    max_replacement_attempts: int | None = None,
    decomposition_threshold: int | None = None,
    replacement_mode: str | None = None,
) -> None:
    if (
        max_replacement_attempts is None
        and decomposition_threshold is None
        and replacement_mode is None
    ):
        raise JournalError("at least one recovery policy value is required")
    current = recovery_policy(journal)
    updated_max = (
        current["maxReplacementAttempts"]
        if max_replacement_attempts is None
        else max_replacement_attempts
    )
    updated_threshold = (
        current["decompositionThreshold"]
        if decomposition_threshold is None
        else decomposition_threshold
    )
    updated_mode = (
        current["replacementMode"]
        if replacement_mode is None
        else replacement_mode
    )
    validate_recovery_policy(updated_max, updated_threshold, updated_mode)
    journal["recoveryPolicy"] = {
        "maxReplacementAttempts": updated_max,
        "decompositionThreshold": updated_threshold,
        "replacementMode": updated_mode,
        "updatedAt": now_iso(),
    }


def new_journal(
    run_id: str,
    project_title: str,
    required_capabilities: list[str] | None = None,
    optional_capabilities: list[str] | None = None,
    max_replacement_attempts: int = DEFAULT_MAX_REPLACEMENT_ATTEMPTS,
    decomposition_threshold: int = DEFAULT_DECOMPOSITION_THRESHOLD,
    replacement_mode: str = DEFAULT_REPLACEMENT_MODE,
) -> dict[str, Any]:
    validate_recovery_policy(
        max_replacement_attempts, decomposition_threshold, replacement_mode
    )
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
        "recoveryPolicy": {
            "maxReplacementAttempts": max_replacement_attempts,
            "decompositionThreshold": decomposition_threshold,
            "replacementMode": replacement_mode,
            "updatedAt": now_iso(),
        },
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


def operation_roles(operation: dict[str, Any]) -> list[str]:
    request = operation.get("request") or {}
    roles = request.get("requestedScreenRoles") or [operation.get("screenRole")]
    return [
        str(role).strip()
        for role in roles
        if role is not None and str(role).strip()
    ]


def normalize_requested_roles(
    screen_role: str, requested_screen_roles: list[str] | None
) -> list[str]:
    roles: list[str] = []
    for role in requested_screen_roles or [screen_role]:
        normalized = str(role).strip()
        if normalized and normalized not in roles:
            roles.append(normalized)
    if not roles:
        raise JournalError("at least one requested screen role is required")
    return roles


def prompt_sha256(prompt: str) -> str:
    return hashlib.sha256(prompt.encode("utf-8")).hexdigest()


def replacement_ancestor_ids(
    journal: dict[str, Any], operation: dict[str, Any]
) -> set[str]:
    ancestors: set[str] = set()
    replacement_for = operation.get("replacementFor")
    while replacement_for:
        if replacement_for in ancestors:
            raise JournalError("replacement lineage contains a cycle")
        ancestors.add(replacement_for)
        replacement_for = find_operation(journal, replacement_for).get(
            "replacementFor"
        )
    return ancestors


def prepare_operation(
    journal: dict[str, Any],
    operation_id: str,
    kind: str,
    project_id: str,
    screen_role: str,
    baseline_screen_ids: list[str] | None = None,
    replacement_for: str | None = None,
    prompt: str | None = None,
    requested_screen_roles: list[str] | None = None,
) -> dict[str, Any]:
    if kind not in OPERATION_KINDS:
        raise JournalError(f"unsupported operation kind: {kind}")
    if any(item.get("id") == operation_id for item in journal.get("operations", [])):
        raise JournalError(f"operation already exists: {operation_id}")
    ensure_project_allowed(journal, project_id)
    if prompt is None or not prompt.strip():
        raise JournalError("the exact mutation prompt must be persisted")

    roles = normalize_requested_roles(screen_role, requested_screen_roles)
    roles_set = set(roles)
    policy = recovery_policy(journal)
    replacement_attempt = 0
    replacement_root = operation_id
    replacement_strategy: str | None = None
    ignored_ancestor_ids: set[str] = set()

    if replacement_for:
        original = find_operation(journal, replacement_for)
        if original.get("status") != "replacement_authorized":
            raise JournalError("replacement target is not authorized")
        if original.get("projectId") != project_id or original.get("kind") != kind:
            raise JournalError("replacement must preserve project and operation kind")
        original_roles = set(operation_roles(original))
        if not roles_set.issubset(original_roles):
            raise JournalError("replacement roles must be covered by the original request")
        original_recovery = original.get("recovery") or {}
        replacement_attempt = int(original_recovery.get("replacementAttempt", 0)) + 1
        if replacement_attempt > policy["maxReplacementAttempts"]:
            raise JournalError(
                "replacement budget exhausted; reconcile, defer, or explicitly reconfigure recovery"
            )
        replacement_root = str(
            original_recovery.get("replacementRoot") or original.get("id")
        )
        if (
            policy["replacementMode"] == "autonomous"
            and original_recovery.get("decompositionRecommended")
            and roles_set == original_roles
        ):
            raise JournalError(
                "autonomous recovery must decompose a compound request into focused roles"
            )
        if roles_set < original_roles:
            replacement_strategy = "decomposed"
        elif prompt_sha256(prompt) == (original.get("request") or {}).get(
            "promptSha256"
        ):
            replacement_strategy = "same_request"
        else:
            replacement_strategy = "revised_request"
        ignored_ancestor_ids = replacement_ancestor_ids(journal, original)
        ignored_ancestor_ids.add(str(original.get("id")))
        if any(
            item.get("status") == "succeeded"
            and (item.get("recovery") or {}).get("replacementRoot")
            == replacement_root
            and int(
                (item.get("recovery") or {}).get("replacementAttempt", 0)
            )
            == replacement_attempt
            and set(operation_roles(item)) & roles_set
            for item in journal.get("operations", [])
        ):
            raise JournalError(
                "replacement lineage already produced the requested screen roles"
            )

    unresolved = [
        item
        for item in journal.get("operations", [])
        if item.get("projectId") == project_id
        and item.get("kind") == kind
        and item.get("status") in UNRESOLVED_STATUSES
        and set(operation_roles(item)) & roles_set
        and item.get("id") not in ignored_ancestor_ids
    ]
    if unresolved:
        blocker = unresolved[0]
        raise JournalError(
            f"unresolved operation {blocker.get('id')} already covers requested roles; "
            "reconcile it before another mutation"
        )

    operation = {
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
        "request": {
            "prompt": prompt,
            "promptSha256": prompt_sha256(prompt),
            "requestedScreenRoles": roles,
        },
        "recovery": {
            "pollCount": 0,
            "finalReconciliation": None,
            "replacementAttempt": replacement_attempt,
            "replacementRoot": replacement_root,
            "replacementStrategy": replacement_strategy,
            "decompositionRecommended": len(roles)
            >= policy["decompositionThreshold"],
            "decisionStatus": "not_required",
            "decisionRequiredAt": None,
            "decisionResolvedAt": None,
        },
    }
    journal.setdefault("operations", []).append(operation)
    return operation


def transition_operation(
    journal: dict[str, Any],
    operation_id: str,
    status: str,
    failure_class: str = "none",
    new_screen_ids: list[str] | None = None,
    note: str | None = None,
) -> dict[str, Any]:
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
    recovery = operation.setdefault(
        "recovery",
        {
            "pollCount": 0,
            "finalReconciliation": None,
            "replacementAttempt": 0,
            "replacementRoot": operation_id,
            "replacementStrategy": None,
            "decompositionRecommended": False,
            "decisionStatus": "not_required",
            "decisionRequiredAt": None,
            "decisionResolvedAt": None,
        },
    )
    if status == "submitted" and operation.get("replacementFor"):
        original = find_operation(journal, operation["replacementFor"])
        if original.get("status") != "replacement_authorized":
            raise JournalError(
                "replacement target is no longer authorized; abandon the prepared replacement"
            )
    if status == "replacement_authorized":
        policy = recovery_policy(journal)
        poll_count = int(recovery.get("pollCount", 0))
        if poll_count < 1:
            raise JournalError(
                "replacement authorization requires at least one recorded poll"
            )
        final_reconciliation = recovery.get("finalReconciliation") or {}
        if final_reconciliation.get("outcome") != "no_matching_output":
            raise JournalError(
                "replacement authorization requires final same-project "
                "reconciliation evidence with no matching output"
            )
        if not final_reconciliation.get("responseComplete"):
            raise JournalError(
                "replacement authorization requires a complete, untruncated "
                "final reconciliation response"
            )
        if final_reconciliation.get("projectId") != operation.get("projectId"):
            raise JournalError(
                "final reconciliation evidence does not match the active operation project"
            )
        next_attempt = int(recovery.get("replacementAttempt", 0)) + 1
        if next_attempt > policy["maxReplacementAttempts"]:
            raise JournalError(
                "replacement budget exhausted; reconcile, defer, or explicitly reconfigure recovery"
            )

    operation["status"] = status
    operation["failureClass"] = effective_failure
    operation["updatedAt"] = now_iso()
    if status == "polling":
        recovery["pollCount"] = int(recovery.get("pollCount", 0)) + 1
        recovery["finalReconciliation"] = None
    if status == "ambiguous_timeout":
        recovery["finalReconciliation"] = None
        recovery["decisionStatus"] = (
            "final_reconciliation_required"
            if int(recovery.get("pollCount", 0)) > 0
            else "polling_required"
        )
        recovery["decisionRequiredAt"] = now_iso()
        recovery["decisionResolvedAt"] = None
    elif status == "replacement_authorized":
        recovery["decisionStatus"] = "replacement_authorized"
        recovery["decisionResolvedAt"] = now_iso()
    elif status in {"succeeded", "abandoned"}:
        recovery["decisionStatus"] = status
        recovery["decisionResolvedAt"] = now_iso()
    if new_screen_ids:
        operation["newScreenIds"] = sorted(
            set(operation.get("newScreenIds", []) + new_screen_ids)
        )
    if note:
        operation.setdefault("notes", []).append(note)
    return operation


def record_final_reconciliation(
    journal: dict[str, Any],
    operation_id: str,
    observed_screen_ids: list[str] | None,
    observed_project_updated_at: str,
    outcome: str,
    response_complete: bool,
    matching_screen_ids: list[str] | None = None,
    note: str | None = None,
) -> dict[str, Any]:
    operation = find_operation(journal, operation_id)
    if operation.get("status") != "ambiguous_timeout":
        raise JournalError(
            "final reconciliation can only be recorded for an ambiguous timeout"
        )
    recovery = operation.get("recovery") or {}
    if int(recovery.get("pollCount", 0)) < 1:
        raise JournalError(
            "final reconciliation requires at least one recorded poll"
        )
    project_updated_at = observed_project_updated_at.strip()
    if not project_updated_at:
        raise JournalError(
            "final reconciliation requires the observed project update time"
        )

    observed = sorted(set(observed_screen_ids or []))
    matching = sorted(set(matching_screen_ids or []))
    if outcome not in {"matching_output", "no_matching_output"}:
        raise JournalError(f"unsupported final reconciliation outcome: {outcome}")
    if outcome == "no_matching_output" and not response_complete:
        raise JournalError(
            "a truncated final reconciliation is inconclusive and cannot "
            "record no matching output"
        )
    if matching and outcome != "matching_output":
        raise JournalError(
            "matching screen IDs require a matching_output outcome"
        )
    if not set(matching).issubset(observed):
        raise JournalError(
            "matching screen IDs must be present in the observed screen list"
        )

    recovery["finalReconciliation"] = {
        "recordedAt": now_iso(),
        "projectId": operation.get("projectId"),
        "observedProjectUpdatedAt": project_updated_at,
        "observedScreenIds": observed,
        "responseComplete": response_complete,
        "matchingScreenIds": matching,
        "outcome": outcome,
    }
    if note:
        operation.setdefault("notes", []).append(note)

    if outcome == "matching_output":
        return transition_operation(
            journal,
            operation_id,
            "succeeded",
            new_screen_ids=matching,
        )

    policy = recovery_policy(journal)
    attempts_remaining = (
        policy["maxReplacementAttempts"]
        - int(recovery.get("replacementAttempt", 0))
    )
    recovery["decisionStatus"] = (
        "autonomous_recovery_ready"
        if policy["replacementMode"] == "autonomous" and attempts_remaining > 0
        else "required"
    )
    operation["updatedAt"] = now_iso()
    return operation


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
    try:
        policy = recovery_policy(journal)
    except JournalError as error:
        errors.append(str(error))
        policy = {
            "maxReplacementAttempts": DEFAULT_MAX_REPLACEMENT_ATTEMPTS,
            "decompositionThreshold": DEFAULT_DECOMPOSITION_THRESHOLD,
            "replacementMode": DEFAULT_REPLACEMENT_MODE,
        }

    for operation in journal.get("operations", []):
        operation_id = operation.get("id")
        if operation.get("projectId") != active_id:
            errors.append(
                f"operation {operation_id} targets a non-active project"
            )
        request = operation.get("request") or {}
        prompt = request.get("prompt")
        digest = request.get("promptSha256")
        if not isinstance(prompt, str) or not prompt.strip():
            warnings.append(f"operation {operation_id} has no persisted prompt")
        elif digest != prompt_sha256(prompt):
            errors.append(f"operation {operation_id} prompt digest does not match")

        recovery = operation.get("recovery") or {}
        replacement_attempt = int(recovery.get("replacementAttempt", 0))
        if replacement_attempt > policy["maxReplacementAttempts"]:
            errors.append(f"operation {operation_id} exceeds replacement budget")
        if (
            recovery.get("decompositionRecommended")
            and operation.get("status") in UNRESOLVED_STATUSES
        ):
            warnings.append(
                f"operation {operation_id} requests multiple screen roles; "
                "prefer focused operations before mutation or replacement"
            )
        if operation.get("status") == "ambiguous_timeout":
            remaining = max(
                policy["maxReplacementAttempts"] - replacement_attempt, 0
            )
            roles = ", ".join(operation_roles(operation)) or "unknown roles"
            poll_count = int(recovery.get("pollCount", 0))
            final_reconciliation = recovery.get("finalReconciliation") or {}
            reconciled = (
                final_reconciliation.get("outcome") == "no_matching_output"
                and bool(final_reconciliation.get("responseComplete"))
            )
            autonomous = (
                policy["replacementMode"] == "autonomous"
                and bool(remaining)
                and reconciled
            )
            if poll_count < 1:
                prefix = "POLLING REQUIRED:"
                suffix = "record at least one same-project poll before final reconciliation"
            elif not reconciled:
                prefix = "FINAL RECONCILIATION REQUIRED:"
                suffix = (
                    "record one final same-project screen list and project update time "
                    "before any replacement authorization"
                )
            else:
                suffix = (
                    "perform one bounded policy-authorized recovery replacement"
                    if autonomous
                    else (
                        "offer a bounded authorized replacement"
                        if remaining
                        else "replacement budget exhausted; do not submit another mutation"
                    )
                )
                if recovery.get("decompositionRecommended") and remaining:
                    suffix += (
                        "; decompose the compound request into focused roles"
                        if autonomous
                        else "; recommend decomposing the compound request"
                    )
                prefix = (
                    "AUTONOMOUS RECOVERY:"
                    if autonomous
                    else "IMMEDIATE RECOVERY DECISION:"
                )
            warnings.append(
                f"{prefix} operation {operation_id} remains "
                f"ambiguous after {poll_count} polls for "
                f"{roles}; {suffix}"
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
        args.max_replacement_attempts,
        args.decomposition_threshold,
        args.replacement_mode,
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
    prompt = args.prompt_file.read_text(encoding="utf-8")
    operation = prepare_operation(
        journal,
        args.operation_id,
        args.kind,
        project_id,
        args.screen_role,
        args.baseline_screen_id,
        args.replacement_for,
        prompt,
        args.requested_screen_role,
    )
    save_journal(args.repo_root, journal)
    recovery = operation["recovery"]
    if recovery["decompositionRecommended"]:
        print(
            "WARNING: compound screen request detected; prefer one focused "
            "operation per requested role"
        )
    if recovery["replacementStrategy"] == "same_request":
        print(
            "WARNING: replacement repeats the original prompt; reconsider a "
            "revised or decomposed request before submitting"
        )
    return 0


def command_transition(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    operation = transition_operation(
        journal,
        args.operation_id,
        args.status,
        args.failure_class,
        args.new_screen_id,
        args.note,
    )
    save_journal(args.repo_root, journal)
    if operation["status"] == "ambiguous_timeout":
        _, warnings, _ = audit_journal(journal)
        for warning in warnings:
            if warning.startswith(
                (
                    "POLLING REQUIRED:",
                    "FINAL RECONCILIATION REQUIRED:",
                    "AUTONOMOUS RECOVERY:",
                    "IMMEDIATE RECOVERY DECISION:",
                )
            ):
                print(warning)
    return 0


def command_final_reconciliation(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    operation = record_final_reconciliation(
        journal,
        args.operation_id,
        args.observed_screen_id,
        args.observed_project_updated_at,
        args.outcome,
        args.response_complete,
        args.matching_screen_id,
        args.note,
    )
    save_journal(args.repo_root, journal)
    if operation["status"] == "ambiguous_timeout":
        _, warnings, _ = audit_journal(journal)
        for warning in warnings:
            if warning.startswith(
                ("AUTONOMOUS RECOVERY:", "IMMEDIATE RECOVERY DECISION:")
            ):
                print(warning)
    return 0


def command_recovery_policy(args: argparse.Namespace) -> int:
    journal = load_journal(args.repo_root)
    set_recovery_policy(
        journal,
        args.max_replacement_attempts,
        args.decomposition_threshold,
        args.replacement_mode,
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
    init.add_argument(
        "--max-replacement-attempts",
        type=int,
        default=DEFAULT_MAX_REPLACEMENT_ATTEMPTS,
    )
    init.add_argument(
        "--decomposition-threshold",
        type=int,
        default=DEFAULT_DECOMPOSITION_THRESHOLD,
    )
    init.add_argument(
        "--replacement-mode",
        choices=sorted(REPLACEMENT_MODES),
        default=DEFAULT_REPLACEMENT_MODE,
    )
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
    prepare.add_argument("--requested-screen-role", action="append", default=[])
    prepare.add_argument("--prompt-file", type=Path, required=True)
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

    reconcile = subparsers.add_parser("record-final-reconciliation")
    reconcile.add_argument("--repo-root", type=Path, default=Path.cwd())
    reconcile.add_argument("--operation-id", required=True)
    reconcile.add_argument("--observed-screen-id", action="append", default=[])
    reconcile.add_argument("--observed-project-updated-at", required=True)
    reconcile.add_argument(
        "--outcome",
        choices=["matching_output", "no_matching_output"],
        required=True,
    )
    response = reconcile.add_mutually_exclusive_group(required=True)
    response.add_argument(
        "--response-complete", dest="response_complete", action="store_true"
    )
    response.add_argument(
        "--response-truncated", dest="response_complete", action="store_false"
    )
    reconcile.add_argument("--matching-screen-id", action="append", default=[])
    reconcile.add_argument("--note")
    reconcile.set_defaults(func=command_final_reconciliation)

    configure = subparsers.add_parser("configure-recovery")
    configure.add_argument("--repo-root", type=Path, default=Path.cwd())
    configure.add_argument("--max-replacement-attempts", type=int)
    configure.add_argument("--decomposition-threshold", type=int)
    configure.add_argument("--replacement-mode", choices=sorted(REPLACEMENT_MODES))
    configure.set_defaults(func=command_recovery_policy)

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
    except (JournalError, json.JSONDecodeError, OSError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
