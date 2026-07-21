# Evidence Discipline

## Purpose
Make completion claims proportionate to the proof captured.

## Evidence expectation values
- `light`
- `standard`
- `strong`

## Recommended defaults
- prototype concept work: light
- prototype native feature work: standard
- dogfood core flows: standard
- beta or release-candidate trust flows: strong

## What counts as evidence
- successful build or launch
- simulator interaction proof
- service request/response proof
- screenshot or UI note
- log snippet or validation note
- explicit statement of what remains unverified

## By task type
### design_translation
Record:
- source concept
- adoption outcome
- native plausibility note

### native_feature
Record:
- validation tier reached
- flow exercised
- any persistence/regression checks

### service / integration
Record:
- maturity level reached
- request/response proof or route exercise
- important assumptions / remaining gaps

### debug_fix
Record:
- issue observed or reproduced
- fix validation path
- regression confidence note when relevant

## Completion rule
If the evidence expectation is `strong` and the task lacks meaningful proof, do not call it done.
Instead, mark it blocked, partially complete, or create a follow-up task.

## Remaining risk rule
Any non-trivial remaining risk should appear in roadmap notes, metadata, or both.
If the risk materially affects a trust surface, consider creating a follow-up task immediately.
