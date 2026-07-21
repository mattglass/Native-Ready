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
- required concept coverage is reconciled as `live`, adequately
  `artifact_only`, `missing`, `deferred`, or `not_needed`
- a `stitch_art_expansion` is not complete until the generated output is
  verified in the proven project or saved with adequate artifact provenance
- an invalid argument is not accepted/submitted evidence, and an ambiguous
  timeout remains recovery work rather than completion evidence

If the work translates Stitch or screenshot evidence into native UI:
- compare the simulator screenshot against the relevant Stitch screenshot
- record whether visual identity was strongly adopted, partially adopted, deferred, or rejected
- verify product-critical artwork, image-forward cards, background treatment,
  color energy, and component personality are implemented or explicitly tracked
  by a ready follow-up task
- if the task claims prototype completion, dogfood readiness, user-testing
  readiness, or exact Stitch parity, perform a requirement-by-requirement
  comparison against the screen packet and reference screenshot before marking
  the claim done
- treat `same product family` as progress, not proof of prototype exit, when
  Stitch contains product-defining artwork or the user asked for close/exact
  visual matching
- do not count generated substitute artwork as visual adoption when usable
  Stitch source artwork exists unless the roadmap records the substitution as an
  explicit product decision
- do not let release-readiness work outrun unresolved visual-fidelity gaps on
  core screens
- do not pass a dependent visual gate while its required concept role remains
  `missing`; keep a linked expansion or explicit deferral decision instead

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
