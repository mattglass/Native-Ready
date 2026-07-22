---
name: ios-setup-orchestrator
description: Internal READY coordinator for the complete design-first setup pipeline. Use explicitly or when ios-app-bootstrap delegates a complex Stitch-first setup that needs concept generation, intake, feature mapping, visual-spine planning, native scaffolding, and first launch validation. Do not present this as a competing public bootstrap entry point.
---

# iOS Setup Orchestrator

Use this skill as an internal coordinator for complex design-first setup. Keep
`ios-app-bootstrap` as the public entry point for new READY apps.

It does not replace `ios-app-director`. It prepares a better repo-local operating memory package so `ios-app-director` has richer, cleaner inputs.

## Read First

Read:
- `references/design-first-pipeline.md`
- `../stitch-ios-concept-builder/references/stitch-operation-policy.md`
- `SETUP.md`
- `AGENTS.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/metadata.json`
- `docs/app-build-spec.md`
- `docs/bootstrap-prompt.md`
If the native Xcode project is missing, also read the `ios-native-scaffold` skill before delivery begins.
If Stitch produced distinctive visual concepts, also read the `ios-visual-spine` skill before seeding implementation tasks.

## Guardrails

- Use global skills by default.
- Do not install or activate `plugins/ios-app-director` during normal setup.
- Treat the bundled plugin as optional packaging for a developer who intentionally wants the local plugin copy.
- Do not edit Swift files until app memory, design memory, feature map, roadmap, metadata, and baton are coherent.
- Do not let `MyApp` become the real native target unless the user explicitly chooses that name.
- Preserve the design-first source path: Stitch evidence first, feature map second, bootstrap/director third.
- Return control to `ios-app-bootstrap` for completion-state classification and
  `docs/bootstrap-receipt.md` rendering.

## Workflow

### 1. Establish The Project Frame

Confirm:
- repo root
- app name
- target user
- purpose
- platform
- maturity stage
- Stitch project name or ID
- backend and Cloudflare scope
- native Xcode project location, if already created

Classify Stitch, XcodeBuildMCP, Cloudflare, and other external capabilities as
`required`, `optional`, or `not_in_scope` for this setup. An unavailable
optional or out-of-scope capability is non-blocking and must not trigger an
alternate project, service, or architecture.

Ask only for missing decisions that block setup.

### 2. Run Design Intake

If no Stitch project or screen set exists yet, use `stitch-ios-concept-builder` to generate the first concept screens from bootstrap answers.

Resolve one active Stitch project and retain it throughout setup. Follow the
shared Stitch operation policy for project provenance, mutation preflight,
truthful result reporting, timeout recovery, and replacement authorization.
Never recover from an invalid tool payload or an empty screen list by creating
another project.

Then use `stitch-ios-intake` to inspect Stitch project data or manual design artifacts.

If setup already ran but the Stitch project has new screens, use `stitch-ios-intake` in refresh mode before changing roadmap or Swift files.

Expected output:
- `.stitch/intake/design-intake.md`
- `.stitch/intake/intake-manifest.json` and `.stitch/intake/intake-manifest.md`
- `.stitch/intake/image-asset-manifest.json` and `.stitch/intake/image-asset-manifest.md` when HTML contains product-critical source artwork
- updated `.stitch/metadata.json` Stitch project and reference screen fields
- unresolved design/product questions
- concept coverage that classifies requested or product-required screen roles
  as live, artifact-only, missing, deferred, or not needed

### 3. Build The Feature Map

Use `ios-feature-map` to synthesize section 9 of `.stitch/APP.md`.

Expected output:
- quality-controlled `## 9. App Feature Inventory & Requirements Map`
- concise updates to `docs/app-build-spec.md`
- candidate roadmap seeds

### 4. Bootstrap Or Repair Repo Memory

Use `ios-app-bootstrap` when the repo is new or under-specified.

Fill or repair:
- `AGENTS.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- `.stitch/metadata.json`
- `docs/app-build-spec.md`

When app metadata exists, reconcile `AGENTS.md` with the real app name,
platform, native project path, source root, target, scheme, and bundle
identifier. Keep these changes repo-local; do not modify global Codex
configuration, skills, or plugins unless the user explicitly asks.

### 4a. Seed The Visual Spine

When Stitch produced distinctive artwork, image-forward cards, custom motifs,
or a strong mood, use `ios-visual-spine` before finalizing the first roadmap.

Expected output:
- product-critical visual signatures named in `.stitch/APP.md` or `.stitch/DESIGN.md`
- reference Stitch screens attached to early tasks
- asset/drawing strategy for hero media and core cards
- source artwork candidates from `.stitch/intake/assets/` before generated substitutes
- visual fidelity acceptance criteria for onboarding, app shell, primary
  discovery/detail, and the first creation flow
- at least one early visual-spine roadmap task when the native app would
  otherwise start from generic symbols or placeholder gradients

### 5. Create The First Roadmap And Baton

The first tasks should come from:
1. critical trust/safety/setup work
2. design spine work that makes onboarding/app shell feel like the Stitch concept
3. onboarding or first activation flow
4. primary daily-use flow
5. required service contract before UI implies live behavior

When Stitch generates distinctive artwork, image-forward cards, or a highly
specific mood, include visual translation requirements in the first design
tasks. The first implementation wave should not merely create functional
placeholders; it should make the app recognizable as the Stitch concept and
define whether each core surface is targeting `same_product_family`,
`prototype_visual_gate`, or `exact_reference` fidelity.

Do not seed a roadmap where prototype exit can be claimed before the core
Stitch-backed screens pass the prototype visual exit gate. If source artwork is
available in `.stitch/intake/assets/`, tasks should prefer it or record the
reason for a substitute.

If the first native tasks need artwork or content variants that the current
Stitch project does not contain, seed a `stitch_art_expansion` task before the
native implementation task. That task should add screens/states/variants to the
existing Stitch project, refresh intake, extract image assets, and update screen
packets before SwiftUI uses generated substitutes.

Each task needs:
- task type
- feature
- screen
- mode
- destination
- validation tier
- evidence expectation
- regression scope
- maturity stage
- reference Stitch screen(s) when design-first evidence exists
- visual fidelity acceptance criteria when the screen depends on artwork,
  imagery, custom component style, or a distinctive mood

After writing `.stitch/next-prompt.md`, validate baton frontmatter with
`python3 <ios-app-director-skill-dir>/scripts/validate_baton_frontmatter.py --repo-root .`,
where `<ios-app-director-skill-dir>` is the directory containing the active
`ios-app-director/SKILL.md`. Do not assume the script lives in the app repo.

### 6. Create Or Confirm The Native Scaffold

If the repo does not already contain a native Xcode project:
- use `ios-native-scaffold`
- derive the target/module/scheme from the app name
- create the SwiftUI project before product feature implementation starts
- update `AGENTS.md`, `.stitch/metadata.json`, `.stitch/APP.md`, `.stitch/ROADMAP.md`, `.stitch/next-prompt.md`, and `docs/app-build-spec.md` with the real native paths
- run a final `MyApp` placeholder check against active operating memory
- prepare XcodeBuildMCP defaults for first build/run validation

Expected output:
- generated `.xcodeproj`
- app entry type
- source root and feature folders
- `docs/native-scaffold.md`
- metadata with `nativeProjectStatus: created`

### 7. Hand Off To Delivery

Only after memory is coherent:
- use XcodeBuildMCP for first build/run validation
- return to `ios-app-bootstrap` to render the bootstrap receipt
- identify `ios-app-director` as the delivery successor
- use `stitch-loop-ios` for concept-then-native screen work
- use `ios-feature-closeout` after meaningful work

End setup with a clean handoff that names:
- active roadmap task
- active baton
- first native destination and source root
- generated target/scheme/bundle id
- visual-spine status and first visual-fidelity gate
- remaining setup risks
- unresolved Stitch operations and missing required concept roles
- what not to build yet

Do not begin product-feature implementation unless the user's active request
also authorizes delivery or includes an active `/goal`.

During long Stitch generation or intake runs, give progress updates after each
major phase: project/screen discovery, artifact queue/save, feature map,
visual-spine plan, native scaffold, and first build validation. Do not stay
silent through a multi-minute setup unless a tool call is actively running.
