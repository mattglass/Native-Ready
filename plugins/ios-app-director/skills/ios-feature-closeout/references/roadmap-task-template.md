# Roadmap Task Template

## Standard shape
```md
## Task TASK-ID
- status: ready | in_progress | blocked | done | icebox
- priority: critical | high | medium | low
- task_type: native_feature | design_translation | stitch_art_expansion | service_contract | integration | debug_fix | performance | release_readiness | product_refinement
- feature: feature-name
- screen: screen-or-surface
- mode: native | concept | concept_then_native | concept_art_then_native | native_plus_service | service_planning | release_hardening
- destination: `path/or/module`
- reference_screens:
  - Stitch screen title/path/id when design-first evidence exists
- visual_fidelity:
  - none | light | required | deferred-with-task
- visual_parity_target:
  - none | same_product_family | prototype_visual_gate | exact_reference
- prototype_exit_gate:
  - not_applicable | required | blocked | passed
- source_assets:
  - `.stitch/intake/assets/...` when Stitch HTML provides usable product-critical artwork
- stitch_expansion:
  - none | needed | submitted | polling | ambiguous_timeout | replacement_authorized | completed | intentionally_deferred
- stitch_operation_id:
  - operation journal ID when a Stitch mutation has been prepared or submitted
- app_maturity: prototype | dogfood | beta | release_candidate | production
- evidence_expectation: light | standard | strong
- regression_scope: none | local | adjacent | feature_family | critical_path
- architecture_review: none | note_only | review_after_closeout
- risk_level: low | medium | high
- summary: One-sentence task statement.
- success_criteria:
  - criterion 1
  - criterion 2
  - criterion 3
  - visual/design parity criterion when Stitch provides product-critical visual direction
- depends_on:
  - optional dependency
- unlocked_by:
  - optional trigger
- notes:
  - what changed
  - what was validated
  - remaining risk, follow-up, or architectural implication
```

## Writing rules
- `summary` should describe one coherent unit of work.
- `app_maturity` should match the stage that justifies the task.
- `evidence_expectation` and `regression_scope` should reflect product risk.
- `architecture_review` should be `review_after_closeout` when the task is likely to affect shared patterns.
- `unlocked_by` should explain why the task exists now.
- `notes` should record reality after the task changes state.
- `reference_screens` should name the Stitch/screenshots used for design-first tasks.
- `visual_fidelity` should be `required` when artwork, image treatment, composition,
  or mood is core to the user experience. If it is deferred, create or reference
  the follow-up task before closing the current task.
- `visual_parity_target` should be `prototype_visual_gate` for core screens that
  must support prototype exit, and `exact_reference` only when the user or task
  explicitly requires close matching to a named Stitch screen.
- `prototype_exit_gate` should be `required` or `blocked` when a task is needed
  before moving to dogfood, user testing, beta, or release readiness.
- `source_assets` should name extracted Stitch artwork when available. If
  generated substitutes are used instead, explain why in `notes`.
- Use `task_type: stitch_art_expansion` and `mode: concept_art_then_native` when
  the native app needs additional Stitch-consistent artwork, variants, or
  screen states before implementation can meet the visual parity target.
- `stitch_expansion` should be `needed` when current assets are insufficient and
  another Stitch screen/state would likely improve native alignment.
- Move `stitch_expansion` through submitted/polling/recovery states from tool
  evidence. Do not convert a timed-out operation into a generic blocker or lose
  the operation ID while dependency-safe work continues.
