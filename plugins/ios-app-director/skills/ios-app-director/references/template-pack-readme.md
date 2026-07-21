# READY Template Pack Reference

This reference summarizes how `APP-TEMPLATE-FOR-AI-BUILD-READY` is meant to be used by `ios-app-director`.

## Purpose

READY is a repo-local operating workspace for roadmap-driven iOS app development.

It gives a fresh app repo:

- project instructions
- app/product memory
- Stitch design memory
- feature-map and roadmap structure
- baton handoff structure
- optional local plugin packaging
- native SwiftUI scaffold automation
- XcodeBuildMCP validation expectations

## Current Setup Shape

Prefer this sequence:

1. use `ios-app-bootstrap` as the single public setup entry point
2. establish repo root, product frame, and capability preflight
3. inspect or create Stitch concepts when design is in scope
4. run `stitch-ios-intake`, `ios-feature-map`, and `ios-visual-spine`
5. fill or repair repo-local memory, roadmap, metadata, and baton
6. use `ios-native-scaffold` to create the initial SwiftUI Xcode project and replace placeholder native paths
7. validate the first scheme and simulator build/launch with XcodeBuildMCP
8. write `docs/bootstrap-receipt.md`
9. hand off to `ios-app-director` delivery mode only when delivery is authorized
10. close out meaningful work with `ios-feature-closeout`

Do not ask the user to manually open Xcode unless automated native scaffold is genuinely blocked.

## Repo Root Contract

The repo root is the folder containing:

- `AGENTS.md`
- `docs/`
- `.stitch/`

A generated SwiftUI project may live inside a nested app container:

```text
repo-root/
  AppTargetApp/
    AppTarget.xcodeproj
    AppTarget/
```

Do not treat the nested Swift source folder as the operating workspace root.

## Important Files

- `SETUP.md` — current setup instructions and legacy workflow note
- `README.md` — high-level template pack overview
- `AGENTS.md` — repo operating rules and project context
- `.stitch/APP.md` — product memory and feature inventory
- `.stitch/DESIGN.md` — semantic design system
- `.stitch/intake/design-intake.md` — Stitch/screenshot intake evidence when available
- `.stitch/intake/intake-manifest.json` and `.stitch/intake/intake-manifest.md` — stable inventory for screenshots, HTML, notes, and intake records
- `.stitch/ROADMAP.md` — living task queue
- `.stitch/next-prompt.md` — active baton
- `.stitch/metadata.json` — project, design, native, evidence, risk, and maturity metadata
- `.stitch/operations/current.json` — active Stitch project provenance and
  mutation/recovery journal when Stitch operations are in flight
- `docs/app-build-spec.md` — product build brief
- `docs/bootstrap-prompt.md` — stable global-skill setup prompt
- `docs/design-first-setup-prompt.md` — advanced Stitch inputs for the same stable bootstrap entry point
- `docs/native-scaffold.md` — generated after native scaffold
- `docs/bootstrap-receipt.md` — generated setup result, risks, and exact next prompt
- `workers/README.md` — backend/service planning starter

## Skill Sources And Setup Paths

The complete READY suite contains these 10 skills:

- `ios-app-bootstrap`
- `ios-app-director`
- `ios-feature-closeout`
- `ios-setup-orchestrator`
- `stitch-ios-concept-builder`
- `stitch-ios-intake`
- `ios-feature-map`
- `ios-visual-spine`
- `ios-native-scaffold`
- `stitch-loop-ios`

The stable default uses the globally installed copies and
`docs/bootstrap-prompt.md`. The bundled local plugin is optional packaging of
the same skills; it does not add a separate workflow tier. Do not install or
activate it unless the user intentionally wants to test or share the packaged
copy. Use `docs/design-first-setup-prompt.md` when the same bootstrap needs
richer design-first inputs. `ios-setup-orchestrator` remains an explicit/internal
coordinator rather than another public front door. The 10 READY skills are
self-contained: their internal contracts cover
Stitch prompt quality, semantic design-system synthesis, product-aware visual
direction, and generation/edit iteration.

## Native Naming Contract

Do not let `MyApp` become the real app target unless the user explicitly chooses that name.

Derive app-safe native names from the product name:

- display name: `H2O Habit Tracker`
- target/module/scheme: `H2OHabitTracker`
- planned test target: `H2OHabitTrackerTests`
- app entry type: `H2OHabitTrackerApp`
- project path: `H2OHabitTrackerApp/H2OHabitTracker.xcodeproj`
- source root: `H2OHabitTrackerApp/H2OHabitTracker/`

After native scaffold, active operating memory should not contain `MyApp/` destination paths.

## Design Evidence Order

Prefer sources in this order:

1. live native implementation
2. explicit user decisions
3. live Stitch MCP project data
4. exported Stitch screenshots and HTML
5. Google Docs or pasted feature plans
6. older speculative notes

Treat Stitch as semantic design evidence. Do not copy conceptual HTML literally into SwiftUI.

## Refresh After Stitch Changes

If a Stitch project gains new screens after setup:

1. run `stitch-ios-intake` in refresh mode
2. update `.stitch/intake/design-intake.md`
3. save or reference new screenshots and HTML under `.stitch/intake/`, preferably with `save_stitch_screen_artifacts.py` when URLs need downloading
4. rebuild `.stitch/intake/intake-manifest.json` and `.stitch/intake/intake-manifest.md`
5. use the save script and manifest as the artifact surfaces instead of shell commands that name each new file
6. update `.stitch/metadata.json` reference screens and design adoption records
7. run `ios-feature-map`
8. refresh `.stitch/APP.md` section 9 and `.stitch/DESIGN.md` when warranted
9. add or adjust roadmap/baton only if the new evidence changes scope or priority

Preserve completed native build evidence and completed roadmap history.

## Setup Done Criteria

Setup is complete when:

- `AGENTS.md` names the app and current target assumptions
- `docs/app-build-spec.md` summarizes purpose, scope, design inputs, and service notes
- `.stitch/APP.md` has a useful section 9 feature inventory
- `.stitch/DESIGN.md` is app-specific
- `.stitch/metadata.json` records Stitch and native project facts
- requested/product-required concept roles have a recorded coverage status and
  missing roles remain actionable
- unresolved Stitch timeouts or replacement decisions are named in the handoff
  rather than hidden behind a generic blocker
- `.stitch/ROADMAP.md` has maturity-appropriate tasks
- `.stitch/next-prompt.md` points at the next concrete task
- the native scaffold exists or deferral is explicitly recorded
- XcodeBuildMCP validation has run when native code exists

## First Delivery Handoff

When setup is done, hand off with:

- active roadmap task
- active baton
- target/scheme/bundle id
- native project path and source root
- primary Stitch project and reference screen IDs
- build/run evidence
- remaining setup risks
- clear non-goals

## Roadmap Growth After Closeout

Prototype closeout and regression tasks are checkpoints, not hard stops.

Before writing a no-next-task handoff, the director must audit `.stitch/APP.md`
section 9, design intake, metadata risks/service maturity, and any new Stitch
screen evidence against the completed roadmap. If current-maturity buildable
scope remains, inject the smallest justified coherent task and keep the baton moving.

The director must also audit maturity transition before stopping. If prototype
closeout proves the app is ready for dogfood, or another stage checkpoint proves
the next maturity target is justified, promote the maturity target and activate
the smallest coherent next-stage task. Future-stage icebox labels are gates to
re-evaluate, not permanent stop signs.

Only pause when remaining work is explicitly blocked, iceboxed behind an
unsatisfied gate, or requires a product/maturity decision, and record the audit
trail in the handoff.
