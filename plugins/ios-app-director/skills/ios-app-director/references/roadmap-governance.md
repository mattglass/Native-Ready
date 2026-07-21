# Roadmap Governance

## Purpose
Make autonomous roadmap growth trustworthy and dependency-aware.

## Supported statuses
- `ready`
- `in_progress`
- `blocked`
- `done`
- `icebox`

At most one task should normally hold the active baton.

## Task quality standard
Every task should clearly state:
- status
- priority
- feature
- screen or surface
- mode
- destination
- summary
- success criteria

Completed tasks should also include concise notes about:
- what changed
- what was validated
- what remains deferred or unlocked

## Dependency ordering rules
Prefer work that:
1. strengthens the app's primary goals
2. unblocks other roadmap items
3. improves shared architecture or reuse
4. reduces product or validation ambiguity

Avoid pulling in lower-value work before:
- the current primary flow is believable
- obvious architecture gaps are closed
- hidden dependencies are surfaced
- the design-first visual spine is believable for apps where Stitch generated
  distinctive artwork or a highly specific look and feel

## Early maturity stroke-size policy

In prototype and early dogfood, prefer larger coherent vertical-slice tasks over
tiny isolated polish tasks. A useful early task should often implement an entire
user-visible slice such as onboarding plus app shell, discovery plus recipe
detail, or photo capture plus generated result, including the core design
language needed for that slice to feel like the Stitch concept.

Do not split visual identity, artwork, and primary interaction into disconnected
late polish unless there is a technical blocker. Early feature work should
carry enough of the visual system that validation can judge the product, not
just the data model.

## Autonomous task creation rules
Only add a task when it is justified by:
- product intent from `APP.md`
- implementation gaps discovered during coding
- runtime findings discovered during validation
- service dependencies exposed by feature work
- design findings that deserve a real implementation unit
- production-readiness needs that are now timely
- visual-fidelity gaps between Stitch reference screenshots and simulator
  screenshots on core product screens

## User-directed scope changes

When the user introduces a new feature idea, creative direction, product
requirement, design refinement, acceptance decision, or deferral decision that
is not already represented in the active roadmap, do not treat it as an
isolated implementation request.

First reconcile the request against repo memory:
- update `.stitch/APP.md` section 9 when the prompt changes product
  capability, user outcomes, requirements, roadmap scope, data needs, or
  service expectations
- update `.stitch/DESIGN.md`, `.stitch/visual-spine-plan.md`, or the relevant
  `.stitch/screen-packets/` when the prompt changes visual language, artwork
  direction, component personality, screen composition, motion, or visual
  fidelity expectations
- amend the best matching roadmap task, or inject the smallest justified new
  task, when the prompt creates implementation work
- record explicit accept, reject, defer, or priority decisions in roadmap notes,
  metadata, and baton context when those decisions affect future agents

Then update `.stitch/ROADMAP.md`, `.stitch/next-prompt.md`,
`.stitch/metadata.json`, and any evidence or design notes needed for the next
agent to continue without rediscovering the decision.

Do not bury reusable product or design direction only in the chat transcript.
If it should guide future implementation, it belongs in repo memory before or
alongside code changes.

When adding a task, include in notes or baton context:
- trigger: what caused the task to exist
- dependency: what it depends on or what it unblocks
- sequencing reason: why it belongs now instead of later

When the trigger is missing or weak product-specific artwork, consider a
`stitch_art_expansion` task before a native polish task. If an existing Stitch
project already defines the app's visual world, add a screen, state, or variant
there, rerun intake and asset extraction, then implement from the stronger
source evidence.

## Recommended task types
Use task language that implies one of these patterns:
- native_feature
- design_translation
- stitch_art_expansion
- service_contract
- integration
- debug_fix
- performance
- release_readiness
- product_refinement

## Successor task policy
When closing a task, decide whether it naturally unlocks:
- a direct successor in the same feature
- a follow-on integration task
- a cleanup/refactor task
- a readiness task

If yes, add or advance that task explicitly instead of relying on memory.

## No-ready-task audit
Before writing a baton that says there is no next task, the engine must audit
the roadmap against the app memory and design evidence.

Do not conclude `NONE_READY`, `prototype complete`, `waiting_for_product_scope`,
or similar handoff states from roadmap status alone.

First compare:
- `.stitch/APP.md` section 9 feature inventory and requirement matrix
- `.stitch/intake/design-intake.md` when present
- `.stitch/metadata.json` reference screens, risk register, service maturity, and task injection history
- current implementation evidence and completed roadmap notes
- any new or changed Stitch screens not yet mapped into APP.md or ROADMAP.md

If this audit finds unmet visible requirements, inferred local-first product
requirements, quality-control gaps, data/privacy gaps, accessibility gaps, or
new Stitch screen evidence, inject the smallest justified coherent task instead
of pausing.

## Maturity-transition audit
Before any `NONE_READY`, prototype-complete, or decision-handoff baton, also
ask whether the current maturity checkpoint has been satisfied enough to advance
the app to the next stage.

Run this audit especially when:
- the current-stage roadmap is complete or only contains iceboxed future-stage work
- the app has repeated build/run evidence for multiple core flows
- the remaining iceboxed task is explicitly gated by the next maturity stage
- closeout evidence shows the product is coherent enough for daily internal use

If the transition signals in `app-maturity-model.md` are satisfied, do not treat
future-stage icebox labels as stop conditions. Instead:
- record the maturity transition in roadmap notes and metadata
- promote the app maturity target, for example `prototype` -> `dogfood`
- reclassify or clone the smallest coherent next-stage task as `ready`
- write a baton for that task

For example, `APP-005 reminders` being `icebox until dogfood` should become a
dogfood activation candidate once prototype closeout is validated. It should
not remain a reason to stop unless dogfood itself is a product decision the user
has explicitly declined.

A decision handoff is allowed only when all of these are true:
- no dependency-safe prototype or current-maturity task remains
- no maturity transition is justified by the current evidence
- remaining work is explicitly blocked, iceboxed behind an unsatisfied gate, or requires a product/maturity decision
- the handoff names the audit inputs checked
- the handoff lists the deferred surfaces and why each was not activated
- `.stitch/metadata.json` records the pause reason or remaining scope decision

Prototype closeout is not a hard stop. It is a regression/evidence checkpoint.
After it passes, run the no-ready-task audit and maturity-transition audit, then
either continue roadmap growth or write a decision handoff with the audit trail.

## Prototype visual exit audit

For design-first apps, run this audit before promoting from prototype to
dogfood, user-testing, beta, or release-readiness.

Check:
- `.stitch/screen-packets/` for core-screen implementation packets
- `.stitch/visual-spine-plan.md` when present
- `.stitch/intake/image-asset-manifest.*` for source artwork candidates
- simulator evidence under `.stitch/evidence/`
- roadmap notes for any `partially_adopted`, `generic_substitute`,
  `same_family_only`, or `parity_unproven` status on core screens

Do not promote maturity when a core screen still has product-defining Stitch
artwork or composition that is missing from native UI, unless the user has
explicitly accepted that tradeoff. Instead, create or activate a
`design_translation` or `product_refinement` task with:
- `visual_parity_target: prototype_visual_gate` or `exact_reference`
- reference Stitch screenshots and source assets
- simulator evidence requirement
- acceptance criteria that compares artwork, layout, color energy, component
  personality, motifs, and interaction behavior

If the current task only proves `same product family`, close it as progress but
do not use it as prototype-exit proof for screens where Stitch quality is a
core product requirement.

## Release-readiness sequencing gate

Before promoting to beta/release-candidate or creating App Store/submission
tasks, audit whether core screens have enough visual fidelity to the design
source. If onboarding, discovery, primary detail, creation/capture, or the main
daily-use flow still looks generic compared with Stitch, create or activate a
visual-fidelity task before release-readiness work.
