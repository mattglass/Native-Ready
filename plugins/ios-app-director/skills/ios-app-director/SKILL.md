---
name: ios-app-director
description: Master delivery and recovery skill for roadmap-driven READY iOS apps after bootstrap. Use when an app has an active baton or delivery goal and needs native SwiftUI implementation, Stitch-to-native iteration, service integration, XcodeBuildMCP validation, feature closeout, or roadmap advancement. For a new app or missing native project, use ios-app-bootstrap first.
---

# iOS App Director

Coordinate the roadmap-driven iOS app build.

## Purpose

Turn product intent into a repeatable execution loop that can:

1. bootstrap repo-local memory
2. establish a design and source-of-truth hierarchy
3. choose the next roadmap task intelligently
4. drive concept work when needed
5. implement native features
6. wire service/backend support with maturity awareness
7. validate, regress, and debug live behavior
8. update memory, evidence, and risk state
9. advance the loop without losing cross-feature coherence

## Required references

Before starting, read:

- `references/ai-app-development-engine-spec.md`
- `references/template-pack-readme.md`
- `references/orchestration-policy.md`
- `references/roadmap-governance.md`
- `references/definition-of-done-matrix.md`
- `references/validation-ladder.md`
- `references/design-intake-policy.md`
- `references/service-maturity-model.md`
- `references/production-readiness-ladder.md`
- `references/app-maturity-model.md`
- `references/task-injection-heuristics.md`
- `references/regression-strategy.md`
- `references/evidence-discipline.md`
- `references/architecture-review-loop.md`
- `references/native-implementation-guardrails.md`
- `references/baton-schema.md`
- `references/roadmap-task-template.md`
- `references/metadata-evidence-schema.md`
- `../stitch-ios-concept-builder/references/stitch-operation-policy.md`

If the repo already has local memory files, also read those before making assumptions.
If the repo declares older schema versions, preserve useful context but migrate active roadmap, baton, and metadata work toward the current references.

## Operating modes

### 1. Bootstrap mode

Use this only to route a new, underspecified, or missing-native-project repo to
`ios-app-bootstrap`.

Do not recreate a partial bootstrap inside this skill. Follow
`ios-app-bootstrap` through native scaffold creation, first simulator
build/launch, baton validation, and `docs/bootstrap-receipt.md`. Enter delivery
mode afterward only when the user requested implementation or activated a
delivery goal.

### 2. Delivery mode

Use this when the repo already has working memory and a roadmap.

In delivery mode:
- read the roadmap
- assess app maturity
- choose the highest-priority actionable task
- implement or debug the work
- validate the changed flow and regression scope
- update task state, evidence, and risk
- write the next baton

### 3. Recovery mode

Use this when the project is mid-stream but inconsistent.

In recovery mode:
- reconcile current implementation with the docs
- repair stale roadmap, evidence, risk, or baton state
- update source-of-truth files
- restart the loop from the best current task

## Toolchain roles

- **XcodeBuildMCP**: build, run, inspect logs, inspect UI, verify native behavior
- **Stitch MCP**: concept generation, editing, reference inspection, design exploration
- **Cloudflare MCP**: service/API work, edge endpoints, orchestration, backend evolution
- **Repo-local memory**: persistent product context across sessions

## Companion skills

Use these companion skills when the task matches their specialty.

### iOS and SwiftUI

- **`ios-app-bootstrap`**: bootstrap a new or underspecified iOS repo into a runnable, roadmap-driven starting point
- **`build-ios-apps:ios-debugger-agent`**: run the simulator debug loop, inspect logs, capture screenshots, and verify broken flows end to end
- **`build-ios-apps:swiftui-ui-patterns`**: shape new SwiftUI screens, navigation flows, and reusable view composition patterns
- **`build-ios-apps:swiftui-view-refactor`**: clean up long SwiftUI views, split responsibilities, and stabilize data flow
- **`build-ios-apps:swiftui-liquid-glass`**: adopt or refine Liquid Glass treatments for iOS 26+ SwiftUI UI
- **`build-ios-apps:swiftui-performance-audit`**: review SwiftUI rendering, invalidation, and layout performance issues
- **`build-ios-apps:ios-ettrace-performance`**: capture and compare simulator performance traces for launch and runtime hotspots
- **`build-ios-apps:ios-memgraph-leaks`**: investigate leaks, retain cycles, and memory growth with memgraph workflows

### Stitch and design workflow

- **`stitch-ios-concept-builder`**: plan screen sets and produce complete,
  native-iOS Stitch generation, variant, and edit prompts
- **`stitch-ios-intake`**: turn Stitch evidence into durable intake artifacts and
  synthesize the repo's semantic `.stitch/DESIGN.md`
- **`ios-feature-map`**: translate visible concepts and product evidence into a
  quality-controlled feature inventory and requirements map
- **`stitch-loop-ios`**: choose generation, edit, variant, or inspection work and
  keep the iterative Stitch-to-native loop aligned with the active baton
- **`ios-visual-spine`**: apply a product-aware taste and fidelity audit, preserve
  artwork/mood/component identity, and create or implement visual-spine work

### Cloudflare and backend workflow

- **`cloudflare`**: general Cloudflare platform guidance for Workers, storage, networking, and edge architecture
- **`workers-best-practices`**: review or author Workers code with production-minded patterns and guardrails
- **`wrangler`**: use Wrangler correctly for local dev, configuration, deployment, secrets, and resource management
- **`durable-objects`**: design and implement stateful coordination or workflow logic with Durable Objects
- **`agents-sdk`**: build stateful AI-backed agent or orchestration behavior on Cloudflare Workers when the app needs it
- **`cloudflare-email-service`**: wire transactional or routed email behavior when the product requires email flows
- **`sandbox-sdk`**: implement secure code execution or isolated runtime workflows when backend features need sandboxing

Treat these as focused specialist guides. Use the most relevant companion skill instead of reinventing its workflow inside this skill.

## Core execution loop

### 0. Intake

Understand:
- app purpose
- target user
- primary platform
- first must-have features
- design references
- backend needs

Ask only a few focused questions if critical details are missing.

### 1. Read the repo state

Inspect any existing:
- `AGENTS.md`
- `docs/app-build-spec.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/intake/intake-manifest.json` or `.stitch/intake/intake-manifest.md` when Stitch artifacts matter
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- `.stitch/metadata.json` when design references, evidence, risk, or native destination history matter

Use `references/metadata-evidence-schema.md` when updating structured evidence.

### 2. Choose the work mode and assess app maturity

Decide whether the repo needs:
- bootstrap
- delivery
- recovery

Then identify the current app maturity using `references/app-maturity-model.md`.

### 3. Govern the roadmap before coding

Use `references/roadmap-governance.md` and `references/task-injection-heuristics.md` before selecting or creating work.

If the user introduces a new creative direction, feature idea, product
requirement, design refinement, or acceptance/deferral decision, treat it as a
scope reconciliation event before coding. Update the relevant repo memory first:
`.stitch/APP.md` for product capability and requirements, `.stitch/DESIGN.md`
or screen packets for visual/artwork direction, `.stitch/ROADMAP.md` and
`.stitch/next-prompt.md` for implementation work, and `.stitch/metadata.json`
for decisions or evidence state that future agents must retain.

Prefer this order:
1. the best existing `in_progress` baton
2. the highest-priority dependency-safe `ready` task
3. a split task when the active task is too large or mixed-mode
4. a newly inserted task only when product goals, implementation gaps, runtime evidence, maturity change, or architecture/reliability needs justify it

When creating a new task, record:
- why it exists now
- what unlocked it
- what it depends on
- why it is sequenced where it is
- app maturity
- evidence expectation
- regression scope

Before writing a baton that says there is no next task, run the no-ready-task
audit in `references/roadmap-governance.md`. Compare roadmap status against
APP.md section 9, design intake, metadata risks/service maturity, and any new
Stitch screen evidence. If buildable current-maturity scope remains, inject the
smallest justified coherent task instead of pausing. Prototype closeout is a
checkpoint, not a hard stop. Also run the maturity-transition audit: if
prototype closeout or another stage checkpoint satisfies the next maturity gate,
promote the maturity target and activate the smallest coherent next-stage task
instead of writing `NONE_READY`.

For design-first apps, prototype maturity cannot advance only because features
exist and the app builds. Run the prototype visual exit audit in
`references/roadmap-governance.md` before dogfood, user-testing, beta, release
readiness, or exact-parity claims. If a core Stitch-backed screen is still
`same_family_only`, `partially_adopted`, `generic_substitute`, or
`parity_unproven`, create or activate the smallest visual-spine task instead of
promoting maturity.

### 3a. Keep the roadmap and baton schema disciplined

Use `references/baton-schema.md` when writing or repairing `.stitch/next-prompt.md`.
Use `references/roadmap-task-template.md` when writing or reshaping roadmap items.
After writing `.stitch/next-prompt.md`, run
`python3 <ios-app-director-skill-dir>/scripts/validate_baton_frontmatter.py --repo-root .`
when practical, where `<ios-app-director-skill-dir>` contains this active
`SKILL.md`. Fix malformed frontmatter before ending the turn; do not assume the
app repo contains the validator.

### 4. Design intentionally

Use `references/design-intake-policy.md` when pulling from Stitch or any concept source.

Do not copy conceptual UI literally into native code.
Do not flatten a distinctive Stitch concept into generic SwiftUI either. If the
concept's value depends on custom artwork, image-forward cards, playful
backgrounds, distinctive component styling, or a specific mood, preserve that
visual spine through native drawing, bundled/generated assets, or an explicit
visual-fidelity task.

If the native implementation needs more product-specific artwork, content
variants, or screen states than the current Stitch intake provides, create or
activate a `stitch_art_expansion` task. Add the needed screen/state/variant to
the existing Stitch project when possible, rerun intake and image extraction,
then continue native implementation from the stronger design evidence.

A dependency-safe `stitch_art_expansion` task is executable design work, not a
documentation-only blocker. Follow the shared Stitch operation policy and
attempt the missing screen/state in the active project unless the same role has
an operation that is still polling or ambiguously timed out. If prescribed
polling is exhausted, preserve independent delivery progress but surface the
replacement decision promptly; do not defer that decision until unrelated work
is exhausted.

When Stitch screens or local intake artifacts have changed, refresh and read the stable intake manifest before changing APP.md, DESIGN.md, roadmap, or SwiftUI. Prefer the `stitch-ios-intake` manifest script or directory-level discovery, not shell commands that name each newly added screenshot or HTML file.

Prefer:
- stronger hierarchy
- clearer trust signals
- plausible SwiftUI translation
- app-specific tone over generic templates
- simulator screenshots that meet the task's stated visual parity target:
  `same_product_family` for early progress, `prototype_visual_gate` before
  maturity promotion, or `exact_reference` when the user asks to match a named
  Stitch screen

### 5. Implement natively

When changing app code:
- preserve the repo's current architecture unless intentionally changing it
- use the app's source-of-truth design system
- keep changes incremental and reviewable
- prefer reusable seams when a concern will likely expand across screens
- follow `references/native-implementation-guardrails.md`, especially stable
  fixture identity, iOS 26 SwiftUI text/style hygiene, safe-area overlays, and
  regression checks for shared content families

### 6. Wire services with maturity awareness

Use `references/service-maturity-model.md` when a feature requires remote behavior.

When a feature requires service work:
- define the app-facing contract first
- identify the current service maturity level
- move only one maturity step at a time unless the user clearly wants deeper integration now
- test the end-to-end data flow for the maturity level you implemented
- update docs if the contract or environment assumptions changed

### 7. Validate, regress, and capture evidence before claiming completion

Use `references/validation-ladder.md`, `references/regression-strategy.md`, and `references/evidence-discipline.md`.

For meaningful native changes:
- confirm XcodeBuildMCP defaults when needed
- build and run
- inspect logs or UI state when relevant
- verify the affected flow end to end
- verify persistence, integration, or regression tiers when the task requires them
- capture evidence quality that matches the task's expectation

For service changes:
- test the endpoint or integration path
- verify the app uses the response correctly
- record remaining maturity gaps if the service is not production-ready yet

### 8. Close the task with the right done criteria

Use `references/definition-of-done-matrix.md` before marking work complete.

A task should only move to `done` when:
- the task-type-specific done criteria are satisfied
- the relevant validation tier was completed
- the required regression scope was respected
- the evidence expectation was met
- roadmap notes reflect what changed and what was verified
- the next baton is clearer than before

### 9. Run architecture review when the engine has earned it

Use `references/architecture-review-loop.md` when:
- multiple tasks have been completed since the last review
- shared seams are proliferating
- visual or structural drift is appearing across features
- app maturity advanced

Create explicit coherence tasks only when the review finds something material.

### 10. Update project memory and keep the engine moving

Before finishing:
- update roadmap state
- update baton state
- update structured evidence, risk, or task injection history when relevant
- update source-of-truth docs if they changed
- leave concise notes when a concept was adopted, partially adopted, deferred, or rejected
- add successor, regression, architecture, or readiness tasks when the work naturally unlocked them

## Definition of success

A task is not done because the code looks correct.

A task is done when:
- the implementation or concept outcome exists
- the relevant flow was validated
- the needed regression scope was respected
- the evidence captured matches the task's maturity and risk
- project memory reflects reality
- cross-feature coherence did not silently degrade
- the next step is clearer than before
- the repo is in a more operational state than when you started
