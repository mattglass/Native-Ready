# Stitch Operation Policy

## Purpose

Keep Stitch exploration autonomous while making project identity and mutation
recovery predictable. These rules constrain external-operation safety, not
creative judgment. Agents remain free to choose screen sets, prompts, art
direction, variants, and roadmap sequencing from product evidence.

## Project Identity Invariants

1. Resolve one active Stitch mutation project for the current visual world
   before generating or editing screens. Provenance-registered secondary
   projects may remain read-only design references.
2. Accept project identity only from explicit user input, repo metadata, an
   exact discovery match that the agent has intentionally adopted, or the
   successful result of the current setup run's `create_project` call.
3. Record a successful `create_project` result immediately. Once an active
   project exists, an invalid argument, timeout, empty screen list, design-system
   failure, or unrelated MCP failure must not cause another project to be
   created.
4. Do not call a project-specific read or mutation with an example, stale, or
   otherwise unproven project ID. Listing projects for discovery is allowed.
   Register secondary reference projects before reading them; mutations must
   target the active mutation project.
5. Create an additional project only when the user requests a fork or product
   evidence intentionally calls for a distinct visual world. Record that as a
   separate design decision/run; never use it as error recovery. Treat cleanup
   of accidental projects as a separate destructive action requiring explicit
   approval.

Use
`<stitch-ios-concept-builder-skill-dir>/scripts/stitch_operation_journal.py`
from the active skill when available to persist these invariants under
`.stitch/operations/current.json`.

## Mutation Preflight

Before a generation, edit, variant, or design-system mutation:

1. Read the current tool schema; do not reuse optional fields or enum values
   from an old transcript or example.
2. Prefer the smallest valid payload for the first call. Add optional model or
   design-system parameters only when the current schema and discovered project
   state support them.
3. Snapshot the active project update time and screen IDs.
4. Write the exact prompt to a durable local prompt file, normally
   `.stitch/operations/prompts/<operation-id>.md`. Do not include API keys,
   tokens, or other secrets in a Stitch prompt.
5. Prepare a journal operation using the prompt file and containing the project
   ID, operation kind, intended screen role, every requested screen role, and
   baseline screen IDs. The helper persists the repo-relative prompt-file path,
   prompt text, and digest in the journal before the external mutation begins.
   Operational audit verifies that the durable file still exists under
   `.stitch/operations/prompts/` and matches the digest.
6. Verify that the project ID matches the journal's active project.

Initialize recovery with the helper defaults unless the user or active tool
contract justifies another policy: `autonomous` replacement mode, one
replacement attempt per lineage, and a decomposition warning at two requested
screen roles. Configure different values with the journal's `init` options or
`configure-recovery` command. Do not raise a replacement limit merely because
the current limit was exhausted. A journal created before `recoveryPolicy`
existed retains legacy `manual` behavior; migrate it deliberately with
`configure-recovery --replacement-mode autonomous` rather than silently
changing an unresolved operation's recovery contract.

Schema correction is normal autonomous work. It must not be implemented by
creating another project or by trying an unrelated project ID.

## Result Classification

Classify the tool result before choosing recovery behavior:

- `success`: record returned or newly discovered screens and continue.
- `invalid_argument`: the requested mutation did not start. Correct the payload
  against the current schema; keep the same project.
- `timeout_or_connection`: outcome is unknown. Do not immediately repeat the
  mutation; enter polling against the same project.
- `api_key_required`: no `STITCH_API_KEY` reached the current Codex process.
  Direct the user to `https://stitch.withgoogle.com/settings` and the plugin's
  secure setup helper without requesting the key in chat. Restart Codex Desktop
  after setup. Block only the Stitch-dependent phase when Stitch is required;
  record and bypass it when optional.
- `auth_required`: when `STITCH_API_KEY` is present, treat this as key validity
  or process-propagation trouble. Do not use generic OAuth or change projects.
- `not_found`: reconcile the active project from user input, repo metadata, and
  discovery. Never substitute an example ID.
- `rate_limited` or `server_error`: preserve the operation and use bounded
  backoff appropriate to the tool contract.

Never describe a mutation as accepted, generating, or completed after an
invalid argument. A timeout may be described only as outcome unknown until
project evidence confirms success.

## Request Sizing

Default `generate_screen_from_text` to one requested screen role per operation.
Preserve a coherent multi-screen flow by sequencing focused prompts against the
same project and design system, not by requiring one compound mutation.

If a small compound request is justified by the active tool contract, record
each requested role during preflight. The journal flags requests at or above
the configured decomposition threshold without prohibiting them. Reconsider
that warning before submitting. It provides a safe decomposition map if the
compound outcome later becomes ambiguous.

## Timeout Recovery

Follow the active Stitch tool's timeout instructions. When no screen ID is
returned, poll the same project's screen list and update time using the
preflight baseline. The current `generate_screen_from_text` and
`generate_variants` contracts require one poll every 30 seconds, up to 10
attempts. If a later active tool contract differs, its explicit budget governs
and must be recorded during operation preparation.

Record every observation with the helper's `record-poll` command, including the
observed project update time, full visible screen ID list, response
completeness, and any matching screen IDs. A counter-only `polling` transition
is not evidence and is rejected. These evidence-bearing records survive
handoff.

During polling:

- a new matching screen or project update resolves the operation as success
- unchanged or unmatched evidence keeps the operation in `polling`
- a complete matching observation resolves the operation immediately; the
  remaining poll budget is not required after success
- only exhausting the recorded polling budget yields `ambiguous_timeout`

An ambiguous timeout does not freeze unrelated dependency-safe work, but
recover its design dependency before moving on when recovery is available.
Transition to `ambiguous_timeout` and act on the journal's recovery mode in the
same loop iteration as the final poll.

In default `autonomous` mode:

1. Verify that the journal contains the complete prescribed polling budget as
   evidence-bearing poll records.
2. Reconcile the same project one final time immediately before replacement.
   Record its full observed screen ID list and project update time with
   `record-final-reconciliation`, explicitly classifying both the outcome and
   whether the response was complete. Treat a truncated response as
   inconclusive; it cannot support `no_matching_output`.
3. If matching output appeared, record it as matching, adopt it, and stop
   recovery.
4. Only when the final evidence records `no_matching_output`, transition to
   `replacement_authorized` under the recorded policy.
5. Prepare one linked replacement using the persisted prompt and requested
   roles, then continue without asking the user.
6. For a compound request, create focused child operations for disjoint roles;
   autonomous recovery must not repeat the compound mutation.

Use `manual` mode only when the user requests per-mutation control. In that
mode, surface the replacement choice as soon as polling is exhausted.

If the original output appears after replacement preparation but before
submission, adopt it and abandon the prepared replacement. If the bounded
replacement also becomes ambiguous, stop mutations for those roles, continue
dependency-safe work, and escalate the exhausted recovery. Never silently
start a second retry.

## Concept Coverage Audit

Track requested or product-required screen roles without imposing a universal
screen count. Classify each role as:

- `live`: discoverable in the active Stitch project
- `artifact_only`: saved evidence exists but the live project does not expose it
- `missing`: required evidence does not exist
- `deferred`: intentionally postponed with a recorded reason or task
- `not_needed`: intentionally excluded by product scope

Missing evidence is normal only as a transient Stitch-loop recovery state. It
is never evidence-neutral or implementation-ready. Setup may continue through
work that is genuinely independent of the missing design role, such as native
project scaffolding or an unrelated service contract. It must not implement the
dependent SwiftUI surface, issue its screen packet, or describe the concept set
as complete unless every required role is `live`, `artifact_only` with adequate
provenance, or explicitly `deferred` with user-accepted native fallback. Create
or retain an actionable `stitch_art_expansion` task for each blocking gap.

When a required role is `missing` and no unresolved journal operation covers
it, generate it autonomously in the active project. This is routine Stitch-loop
work, not a routine reason to ask the user what to do and not permission to
continue the dependent native surface without evidence.

During delivery, `stitch_expansion: needed` is an instruction to perform the
expansion, not merely document it. Generate in the active project unless a
prior operation for that role is still polling or ambiguously timed out. Poll
or recover that operation immediately; do not treat its unresolved state as a
reason to leave the required screen missing.

## Native Design Handoff Gate

Planning and intake may preserve a partial concept set so the gap remains
visible and actionable. Before design-dependent SwiftUI implementation begins,
run:

```bash
python3 <stitch-ios-concept-builder-skill-dir>/scripts/stitch_operation_journal.py audit \
  --repo-root . \
  --gate native-design-handoff \
  --screen-role "<dependent concept role>"
```

A nonzero result blocks only design-dependent implementation. Return to the
active project's generate, poll, reconcile, or recovery loop. The gate requires
required concept roles to have live screen provenance or existing artifact
provenance, rejects unresolved operations for those roles, and accepts a
deferred native fallback only when the record includes an explicit reason and
`userAcceptedNativeFallback: true`.

Pass each role required by the current native surface with another
`--screen-role`. Omit the option for a global readiness or closeout audit. This
keeps an unrelated missing role from freezing dependency-safe work without
weakening the handoff for the surface being implemented.

## Capability Scoping

At setup start, classify external capabilities as `required`, `optional`, or
`not_in_scope` from the product frame. A failed required capability blocks only
the dependent phase. A failed optional or out-of-scope capability is recorded
and ignored; it must not trigger alternate projects, services, or architecture.
