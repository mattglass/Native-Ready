# App Maturity Model

## Purpose
Give the engine a practical sense of how the app should behave at each stage so it can balance speed, hardening, and evidence correctly.

## Stages
### Prototype
Focus on:
- believable UX
- source-of-truth memory
- design translation quality
- lightweight service seams
- proving the primary flow
- visual-spine fidelity on the screens that define the product

Engine bias:
- move quickly
- prefer coherent vertical slices over tiny isolated changes
- take large enough early strokes that users can judge the product experience,
  not only individual controls
- do not over-inject hardening work
- delay release hardening until the core feature and visual identity are both believable

### Dogfood / internal testing
Focus on:
- persistence reliability
- error feedback
- shared-state continuity
- local/dev integrations
- core trust surfaces feeling believable

Engine bias:
- start injecting persistence, reliability, and local integration tasks
- tighten evidence expectations from light to standard

### Beta / active tester phase
Focus on:
- regression discipline
- analytics or event instrumentation where needed
- performance hotspots
- memory / lifecycle issues
- stronger integration behavior

Engine bias:
- inject regression, performance, and observability tasks when feature work raises blast radius
- prefer standard-to-strong evidence

### Release candidate
Focus on:
- error-state completeness
- environment/config hardening
- crash-risk reduction
- observability
- polish on high-value flows

Engine bias:
- favor hardening work over exploratory expansion
- treat missing regression evidence as significant risk

### Production
Focus on:
- reliability
- operational clarity
- long-tail bug reduction
- disciplined release behavior
- service resilience

Engine bias:
- prioritize regression, observability, and resilience tasks earlier
- treat weak evidence or repeated drift as follow-up work, not minor notes

## Transition signals
Move the app upward when one or more are true:
- multiple core flows are believable and repeatedly validated
- core screens pass the prototype visual exit gate when the app is design-first
- real testers or stakeholders are now depending on the build
- live integrations are present or imminent
- release quality matters more than feature novelty

## Prototype visual exit gate
For design-first apps, the prototype stage cannot advance to dogfood,
user-testing, beta, or release-readiness only because the app builds, navigates,
and contains the requested features.

The engine must run a visual exit audit before promotion when Stitch,
screenshots, exported HTML, or screen packets define the product's look and
feel. The audit should cover the core screens that make the app recognizable,
usually onboarding/app shell, discovery/home, primary detail, creation or
capture flow, history/log, reward/trust moments, and settings or guidance.

A core screen passes the prototype visual gate only when:
- its screen packet names the relevant Stitch screenshot or HTML evidence
- product-critical source artwork from `.stitch/intake/assets/` is used, or a
  clear product reason explains why it is unsuitable or intentionally deferred
- simulator screenshots exist for the native surface
- the comparison records layout, artwork, color energy, component personality,
  motifs, and interaction gaps
- remaining visual gaps are non-blocking for the current maturity goal, or a
  ready baton exists to fix them before promotion

`Same product family` is useful early progress, but it is not enough by itself
for a product-builder prototype exit when Stitch contains strong custom
artwork, image-forward layouts, or a user explicitly asks to match the designs
closely. Generated substitute artwork cannot satisfy the gate when usable
Stitch source artwork exists unless the roadmap records the substitution as a
product decision.

When the user asks for a named screen to match Stitch exactly, the parity target
for that screen becomes `exact_reference`. Do not mark that target complete
until a requirement-by-requirement comparison proves it, or the remaining
mismatches are documented as an explicit product decision.

## Autonomous transition rule
When a closeout or regression task proves the current maturity stage is
coherent, the engine must evaluate whether the next maturity stage should become
the active target before it writes any no-next-task baton.

If the next stage is justified and its first tasks are already known, the engine
should advance roadmap state autonomously. An item marked `icebox until dogfood`
is not a permanent pause condition after prototype closeout; it is a maturity
gate waiting to be re-evaluated.

Ask the user only when the transition changes product intent, introduces a new
external dependency, or activates a scope the user explicitly deferred.

## Operating rule
The engine should not use the same task-injection behavior for every stage.
It should adapt roadmap growth, evidence expectations, and regression scope to the current app maturity.
