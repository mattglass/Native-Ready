# Task Injection Heuristics

## Purpose
Make autonomous roadmap growth more predictive, disciplined, and production-minded.

## General rule
Create a new task only when a specific trigger exists. Avoid speculative roadmap spam.

## Trigger families
### 1. Maturity trigger
When app maturity advances, inject work that fits the new stage.

Examples:
- Prototype -> Dogfood: persistence, error feedback, local integration, shared-state reliability
- Dogfood -> Beta: regression packs, analytics, performance hotspots, observability
- Beta -> Release candidate: crash-risk reduction, environment hardening, edge-case polish

When current-stage work is complete, explicitly test whether the next maturity
stage should now activate. Do not leave a task iceboxed for `dogfood`, `beta`,
or `release_candidate` if the app has just produced the evidence that satisfies
that gate. Reclassify the smallest coherent next-stage task as ready, or inject a
maturity-transition task that updates metadata, roadmap notes, and baton state.

### 2. Regression trigger
Create a regression task when:
- a change touched shared state or navigation
- a contract change affects multiple surfaces
- a high-trust flow now has wider blast radius than the active task can safely close out

### 3. Architecture trigger
Create an architecture/coherence task when:
- the same seam appears in 2+ places
- duplicate state ownership patterns appear
- multiple features are drifting visually or structurally
- a repeated pattern should become a shared abstraction

### 4. Evidence trigger
Create a follow-up task when:
- a task closed with material remaining risk
- required evidence could not be captured
- validation depth was intentionally partial but the surface is important

### 5. Service trigger
Create a next-step service task when:
- a maturity level was reached and the next level is now clear
- the UI is blocked on a known backend seam
- integration assumptions should be made explicit before further UI work

### 6. Readiness trigger
Create readiness tasks when the current app maturity and product stakes justify them.

### 7. Roadmap exhaustion trigger
Create a task when the roadmap has no dependency-safe `ready` item but current
app memory still contains buildable unmet scope.

This trigger is especially important after a regression or prototype-closeout
task. A closeout task may raise confidence in the current implementation, but
it does not prove the app has exhausted the feature map.

Audit APP.md, design intake, metadata, and current implementation before
pausing. Inject a next task when you find:
- a visible feature from Stitch or screenshots that is not implemented
- an inferred local-first requirement that is needed for dogfood or a credible prototype
- a privacy/data control implied by local stored data
- an accessibility or empty/error-state gap on a built flow
- changed or newly added Stitch screens not yet reflected in roadmap tasks
- an iceboxed item whose maturity gate is now satisfied
- a current-stage closeout that should promote the app to the next maturity target

### 8. User-directed scope trigger
Create, amend, or reorder a task when the user gives a new creative prompt,
feature idea, product requirement, design refinement, acceptance decision, or
deferral decision that changes what the app should become.

Classify the prompt before coding:
- product capability or user outcome: refresh `.stitch/APP.md` section 9 and
  then seed or amend roadmap work
- visual world, artwork, screen mood, component style, or fidelity expectation:
  refresh `.stitch/DESIGN.md`, `.stitch/visual-spine-plan.md`, or screen packets
  and then seed or amend design-translation work
- service, AI, data, privacy, persistence, or backend expectation: update the
  relevant product/service memory and create a maturity-appropriate contract or
  implementation task
- explicit accept, reject, defer, or priority decision: record the decision in
  roadmap notes, metadata, and baton context, then continue from the new scope

If the prompt is a one-off clarification that does not change future work,
capture it in the current task notes. If it should guide future agents, promote
it into repo memory before implementing.

## Injection rules
- Prefer adding the smallest justified coherent task, not a broad umbrella task.
- In prototype and early dogfood, coherent may mean a vertical slice spanning
  multiple related screens when that is required to prove the product
  experience, visual spine, and first success moment.
- Record the trigger in the task's `unlocked_by` or notes.
- Give the task an app maturity stage and regression scope that match the reason it exists.
- If a new task would be purely hypothetical, do not add it yet.
- Do not write a `NONE_READY` or pause baton until the roadmap exhaustion trigger
  and maturity trigger have been checked and either produced a task or produced
  an explicit audit trail explaining why each remaining gap is deferred,
  blocked, or requires user scope.

## Suggested injected task families
- persistence hardening
- regression pack / retest lane
- architecture coherence review
- design-system reconciliation
- service hardening / observability
- error-state polish
- performance / lifecycle audit
