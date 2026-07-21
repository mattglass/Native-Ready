# iOS App Director — Definition of Done

A feature is not done because code exists.

A feature is done when the relevant scope has reached the appropriate level of closure for the current maturity stage, the task-type-specific done criteria were satisfied, and the evidence captured matches the task's risk.

## Core rules
For most roadmap items, completion should mean:
1. the implementation or concept output exists
2. the correct validation tier was reached
3. the required regression scope was satisfied
4. evidence quality matches the task's expectation
5. relevant project memory was updated
6. roadmap state reflects reality
7. the next baton is clear and current
8. remaining risk is noted when appropriate

## Native feature closeout
Prefer all of the following:
- destination file(s) updated
- app builds successfully
- feature flow was run or inspected in Simulator when practical
- persistence or shared-state continuity checked when relevant
- regression scope matched the task's blast radius
- roadmap notes record what changed, what was validated, and what remains risky

## Design / concept closeout
If the work is conceptual rather than implemented:
- concept artifacts are saved locally when they exist
- adoption outcome is recorded: adopted, partially adopted, deferred, or rejected
- native plausibility is assessed
- cross-feature coherence is considered when the concept changes recurring patterns
- roadmap status reflects whether the work is done, deferred, or blocked

## Backend / service closeout
If the work includes a service layer:
- app-facing contract is defined or updated
- current service maturity level is clear
- endpoint or proxy behavior was tested at the intended maturity level
- response shape is known
- regression impact on connected surfaces was considered
- relevant env/config knowledge is documented

## Strong-evidence rule
If a task expects `strong` evidence and that proof is missing, the task should not be marked done.

## Risk rule
If meaningful residual risk exists on a trust surface, record it explicitly and consider creating a follow-up task immediately.
