---
name: ios-feature-closeout
description: Close out a roadmap item with a repeatable definition of done. Use when a feature, fix, concept pass, or service change needs final validation, roadmap updates, documentation updates, and a clean next-step handoff.
allowed-tools:
  - "Read"
  - "Write"
  - "XcodeBuildMCP:*"
---

# iOS Feature Closeout

Use this skill at the end of a meaningful unit of work.

Its job is to turn “the code changed” into “the work is actually closed out.”

## Required references

Read:
- `references/definition-of-done.md`
- `references/validation-ladder.md`
- `references/regression-strategy.md`
- `references/evidence-discipline.md`
- `references/native-implementation-guardrails.md`
- `references/app-maturity-model.md`
- `references/roadmap-task-template.md`
- `references/baton-schema.md`
- `references/metadata-evidence-schema.md`
- `references/closeout-checklist.md`
- `references/ai-app-development-engine-spec.md`
- `../stitch-ios-concept-builder/references/stitch-operation-policy.md`

If present, also read:
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- `.stitch/metadata.json`
- `docs/app-build-spec.md`

## Closeout workflow

### 1. Confirm what changed

Identify:
- the roadmap item or feature area
- the task type
- the app maturity stage
- files changed
- whether the work was native, conceptual, service-related, or mixed

### 2. Apply the right done criteria

Use `references/definition-of-done.md` and confirm the task satisfies the correct closeout standard for its type and maturity.

### 3. Validate to the required tier

Use `references/validation-ladder.md`.

If native code changed:
- confirm XcodeBuildMCP defaults when needed
- build and run when practical
- verify the affected flow
- include persistence or integration checks when the task requires them

If service work changed:
- verify the relevant request/response path at the intended maturity level

### 4. Satisfy regression scope

Use `references/regression-strategy.md`.

If the task's blast radius is wider than the work you validated, either:
- widen validation now, or
- create a follow-up regression or hardening task explicitly

### 5. Reconcile roadmap state with current notes

Update `.stitch/ROADMAP.md` so the task reflects reality:
- `done`
- `blocked`
- or back to `ready`

Use the current task template shape and record:
- what changed
- what was validated
- remaining risk
- any architectural implication or unlocked follow-up

### 6. Reconcile baton state in current format

Update `.stitch/next-prompt.md` so it either:
- points at the next best task, or
- clearly reflects the follow-up needed for blocked work

After writing or repairing `.stitch/next-prompt.md`, validate frontmatter with
`../ios-app-director/scripts/validate_baton_frontmatter.py --repo-root .` when
available. Do not close a task with malformed baton frontmatter.

Before writing a no-next-task or decision-handoff baton, run a roadmap growth
audit. Compare completed roadmap state against `.stitch/APP.md` section 9,
design intake, metadata risks/service maturity, and any new Stitch screen
evidence. If current-maturity buildable scope remains, inject the smallest
justified coherent task and write that baton. Treat prototype closeout as a
checkpoint, not a hard stop. Also run a maturity-transition audit; if closeout
evidence satisfies the next maturity gate, promote the maturity target and
activate the smallest coherent next-stage task instead of pausing.

For design-first apps, prototype closeout also requires the prototype visual
exit audit. Do not promote to dogfood, user testing, beta, or release-readiness
when core Stitch-backed screens are only `same_family_only`,
`partially_adopted`, `generic_substitute`, or `parity_unproven`. Inject or
activate a visual-spine task instead, and require source-artwork decisions plus
simulator screenshot comparison evidence.

Before recording any design-first maturity promotion, run the active
`ios-visual-spine/scripts/validate_visual_exit.py` with `--repo-root .` and the
matching `--claim`. Resolve the script from the installed skill directory, not
from the app repository. A nonzero result blocks promotion and must be reflected
in the roadmap and baton. Do not rewrite the evidence merely to satisfy the
validator; repair the visual implementation, evidence, or product decision.

Before closing a `stitch_art_expansion` task, reconcile the operation journal,
live project screen list, saved artifacts, and `conceptCoverage`. A submitted or
timed-out mutation is not completion evidence. The task may be `done` only when
the needed output is verified and intake/coverage is updated, or when the user
explicitly changes or defers the requirement. Keep `ambiguous_timeout` as an
actionable recovery state and run configured autonomous recovery promptly.

Before closing a dependent native or design task, confirm that each required
concept role it relies on is `live`, adequately `artifact_only`, or explicitly
`deferred` with a linked task or product decision. If it is still `missing`, do
not hide the gap with a generic substitute or mark the dependent visual gate as
passed. Continue unrelated dependency-safe roadmap work when available.

### 7. Update structured evidence and risk when needed

Use `references/evidence-discipline.md` and `references/metadata-evidence-schema.md`.

If the task created meaningful validation, risk, design-adoption, Stitch
operation, or concept-coverage evidence, update `.stitch/metadata.json`. Keep
detailed mutation history in `.stitch/operations/current.json` and the durable
handoff summary in `stitchOperations`.

### 8. Update source-of-truth docs

If the work changed project understanding, update the smallest relevant docs:
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `docs/app-build-spec.md`
- service notes or architecture notes

### 9. Produce a clean handoff

Before finishing, summarize:
- what is now true
- what was validated
- what regression confidence exists
- what risk remains next
