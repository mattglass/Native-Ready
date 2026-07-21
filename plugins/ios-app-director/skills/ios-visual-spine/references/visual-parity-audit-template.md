# Visual Parity Audit Template

Use this template for `.stitch/visual-parity-audit.md` when a design-first app
is trying to leave prototype, enter user testing, or satisfy exact Stitch
matching on a named screen.

```md
# Visual Parity Audit

Date: YYYY-MM-DD
App maturity target: prototype | dogfood | beta | release_candidate | production
Audit reason: prototype_exit | user_testing_readiness | beta_readiness | exact_reference_request | regression_check

## Summary
- overall_status: pass | blocked | in_progress_not_verified_exact | intentionally_deferred
- decision: promote_maturity | continue_visual_spine_work | ask_product_decision
- blocking_screens:
  - screen name or none

## Core Screen Matrix

| Screen | Stitch reference | Source assets | Native destination | Simulator evidence | Parity target | Status | Blocking gaps |
|---|---|---|---|---|---|---|---|
| Onboarding/App Shell | title/id/path | assets or none | SwiftUI file | evidence path | same_product_family/prototype_visual_gate/exact_reference | pass/blocked/in_progress_not_verified_exact/deferred | gap notes |

## Source Artwork Decisions

- `asset path or manifest id`
  - used_in_native: yes | no
  - native asset name:
  - decision: used | unsuitable | intentionally_deferred | generated_substitute
  - reason:

## Requirement-by-Requirement Notes

### Screen Name
- artwork:
- first viewport composition:
- color energy:
- component personality:
- motifs:
- primary actions:
- content specificity:
- accessibility/readability:
- remaining mismatch:
- follow-up task:

## Promotion Decision

Prototype visual exit gate:
- pass | blocked

Rationale:
- concise explanation

Next baton:
- TASK-ID and task title
```

## Rules

- Use `same_product_family` for early progress, not prototype exit.
- Use `prototype_visual_gate` when a screen must support maturity promotion.
- Use `exact_reference` only when the user or task asks to match a named Stitch
  screen closely.
- If usable Stitch source artwork exists and native uses a generated substitute,
  mark the screen blocked unless a product decision accepts the substitution.
- If evidence does not prove exact matching, use
  `in_progress_not_verified_exact` and keep or create a follow-up task.
