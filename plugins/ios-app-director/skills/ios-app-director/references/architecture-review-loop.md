# Architecture Review Loop

## Purpose
Prevent locally good feature work from turning into globally messy app structure.

## When to run
Run an architecture review when one or more are true:
- 3 to 5 roadmap items have been completed since the last review
- a seam or pattern now exists in multiple features
- the app maturity stage advanced
- a repeated UI or navigation pattern is drifting
- shared state or services became more central to the app

## Review checklist
Inspect:
- navigation coherence
- state ownership patterns
- service boundary clarity
- repeated component or layout patterns
- design-system drift
- naming and folder structure drift
- duplicate logic worth extracting

## Valid outputs
- no-op note: architecture is still coherent
- follow-up cleanup task
- shared abstraction task
- design-system update task
- service boundary clarification task

## Recording
When a meaningful review occurs, record it in structured metadata if available:
- date or relative point in the roadmap
- surfaces reviewed
- main finding
- whether a follow-up task was created

## Rule
Do not over-extract.
Architecture review should tighten coherence, not introduce abstract layers with no near-term product value.
