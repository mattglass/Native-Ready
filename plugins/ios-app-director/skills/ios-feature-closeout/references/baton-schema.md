# Baton Schema

## Purpose
Define a structured active-task baton with explicit maturity, regression, and evidence requirements.

## Required frontmatter fields
- `platform`
- `roadmap_task`
- `task_type`
- `feature`
- `screen`
- `mode`
- `device`
- `app_maturity`

## Required for implementation tasks
- `destination`
- `validation_tier`

## Recommended frontmatter fields
- `destination`
- `validation_tier`
- `service_maturity`
- `design_input`
- `reference_screens`
- `screen_packets`
- `visual_fidelity`
- `visual_parity_target`
- `prototype_exit_gate`
- `asset_strategy`
- `source_assets`
- `stitch_expansion`
- `stitch_operation_id`
- `stitch_recovery_state`
- `replacement_for`
- `depends_on`
- `unlocked_by`
- `regression_scope`
- `evidence_expectation`
- `architecture_review`
- `risk_level`
- `phase`

## Body sections
A baton should usually include:
1. concise task statement
2. source-of-truth section
3. goals
4. validation requirements
5. regression requirements
6. evidence to capture
7. current seams or destination files
8. cross-feature coherence notes when relevant
9. non-goals / do-not section
10. successor hints when helpful

## Task-type guidance
### native_feature
Emphasize destination, regression scope, evidence expectation, and the exact flow to validate.

### service_contract
Emphasize contract boundary, service maturity, integration proof, and remaining risk.

### design_translation
Emphasize concept sources, screen packets, visual-fidelity target, adoption
rules, source asset decisions, prototype visual exit gate status, evidence
expectation, and native plausibility. If `visual_parity_target` is
`exact_reference`, require a requirement-by-requirement comparison before
closeout.

### stitch_art_expansion
Emphasize the existing Stitch project, source screens to stay consistent with,
the missing artwork or screen state, the native fidelity gap being unblocked,
the intake/asset extraction handoff, and the follow-up SwiftUI destination.
Name the active operation ID and recovery state when generation has been
submitted. `ambiguous_timeout` remains an actionable recovery state, not a
generic design blocker; surface replacement authorization promptly when it
blocks the task chain.

### debug_fix
Emphasize reproduction path, regression scope, and confidence level.

### release_readiness
Emphasize the quality dimension being improved, required evidence, and affected critical paths.
