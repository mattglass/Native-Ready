# READY - Autonomous iOS App Development Engine

## Purpose
READY is an autonomous, roadmap-driven iOS app development engine designed and
built entirely with Codex CLI and the Codex desktop app, using GPT-5.5 and
GPT-5.6. It bundles 10 specialized skills in the `ios-app-director` plugin
with a reusable app scaffold, persistent project memory, design-first planning,
native SwiftUI delivery, and live validation loops.

Once an app is bootstrapped and a goal is active, READY can keep the build
moving: select the next roadmap task, explore or interpret Stitch concepts,
implement native features, validate them with XcodeBuildMCP, capture evidence,
update the baton, and continue until a real blocker or product decision needs a
human. The result is meant to feel less like prompting a code generator and
more like directing an AI-powered product team that remembers where it is going.

## Execution model
“Autonomous” describes how the development loop behaves inside an active Codex
session with the permissions and tools the developer provides. READY is not a
detached background daemon: Codex supplies the reasoning and execution surface,
XcodeBuildMCP supplies native build and simulator feedback, Stitch supplies the
visual concept loop, and Cloudflare tooling can extend the app into real service
work when the product needs it.

It is designed to support:

- roadmap-driven native iOS delivery
- Stitch-to-SwiftUI concept translation
- service seam evolution
- simulator-backed validation loops
- maturity-aware behavior
- anticipatory roadmap intelligence
- regression discipline
- evidence rigor
- cross-feature coherence reviews

## Requirements

READY's complete native loop requires a compatible Mac and Xcode installation,
an iOS Simulator runtime, Codex Desktop or Codex CLI, one active copy of the 10
READY skills, and XcodeBuildMCP. The automatic design-first path also requires
a Google account with Stitch access plus an authenticated Stitch MCP
connection. Cloudflare and Apple Developer Program access are conditional on
the app's backend and distribution needs.

See [SETUP.md](SETUP.md) for the current prerequisite matrix, quick checks,
tool authentication, and the distinction between required and optional
capabilities.

## Core layers
### Global engine layer
The shared intelligence can be installed globally as the complete 10-skill
READY suite:

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

The bundled `ios-app-director` plugin packages these same 10 skills for
installation, testing, and distribution. It is an alternate skill source, not
a separate workflow tier. These 10 skills are the complete READY workflow:
prompt enhancement, semantic design-system synthesis, product-aware visual
direction, and Stitch generation/edit routing are owned by the relevant skills
in the bundle rather than delegated to external design wrappers.

### Repo-local operating layer
Each app repo should establish:
- `AGENTS.md`
- `docs/app-build-spec.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- `.stitch/metadata.json`

### Runtime validation layer
Use XcodeBuildMCP to:
- build
- run
- inspect UI
- validate flows
- satisfy regression scope
- verify persistence and integration behavior

## Operating system capabilities
This framework includes:
- app maturity modeling
- task injection heuristics
- regression strategy
- evidence discipline
- architecture review loop
- baton schema
- roadmap task template
- metadata evidence schema

## Current framework emphasis
- maturity-aware, production-minded roadmap advancement
- stronger regression, evidence, and cross-feature coherence discipline
- design-first setup with visual-spine planning and native scaffold automation before implementation begins

## Repo layout
```text
repo-root/
  AGENTS.md
  SETUP.md
  .agents/
    plugins/
      marketplace.json
      marketplace.opt-in-ios-app-director.json
  .codex/
    config.toml
  .stitch/
    APP.md
    DESIGN.md
    intake/
      intake-manifest.json
      intake-manifest.md
      image-asset-manifest.json
      image-asset-manifest.md
      assets/
    ROADMAP.md
    next-prompt.md
    metadata.json
    evidence/
    designs/
    prompts/
    screen-packets/
  docs/
    ai-app-development-engine-spec.md
    app-build-spec.md
    bootstrap-prompt.md
    design-first-setup-prompt.md
    bootstrap-receipt.md  # generated after bootstrap
    definition-of-done.md
    example-build-spec.md
    native-scaffold.md  # generated after native scaffold
  plugins/
    ios-app-director/
  workers/
```

## How to use this template
1. Clone, copy or unzip this READY template into a new app folder/repo.
2. Read `SETUP.md` and complete the required Xcode, Codex, skill, MCP, and account preflight.
3. Open Codex Desktop or Codex CLI at the copied repo root and make the complete app brief the first message.
4. Use `docs/bootstrap-prompt.md` and `$ios-app-bootstrap` as the single public setup entry point. `docs/design-first-setup-prompt.md` adds advanced Stitch inputs to that same entry point.
5. Let bootstrap inspect or create design evidence, generate the feature map, create the native SwiftUI scaffold, run the first simulator build/launch, validate the baton, and write `docs/bootstrap-receipt.md`.
6. After a `ready_for_delivery` receipt, use the documented `/goal` prompt and `ios-app-director` for autonomous delivery.
7. Use `ios-feature-closeout` to reconcile roadmap, baton, evidence, risk, and next-step handoff after meaningful work.

## Optional bundled plugin install
READY works without installing the repo-local plugin when the matching global skills are available. The default `.agents/plugins/marketplace.json` is intentionally empty so a copied app repo does not silently activate duplicate `ios-app-*` skills.

Developers who intentionally want the packaged local copy can use `.agents/plugins/marketplace.opt-in-ios-app-director.json`. That marketplace points at `plugins/ios-app-director/` and keeps the bundled plugin an explicit install choice.

The bundled plugin manifest is skills-only by default. The plugin includes `.mcp.json` as optional wiring for XcodeBuildMCP, Cloudflare MCP, and Stitch MCP, but that file is not enabled automatically by `plugin.json`. Enable those MCP servers only after the developer has the needed local tools and Cloudflare/Stitch auth ready.

## Design-first workflow
The default bootstrap is also the design-first path. Use
`docs/design-first-setup-prompt.md` when the first message needs richer Stitch
inputs; it still starts with `$ios-app-bootstrap`. The bootstrap may use the
internal setup coordinator and other READY specialists to provide:
- concept generation from bootstrap answers when no Stitch project exists yet
- one provenance-backed active Stitch mutation project per visual world, without
  fallback projects after payload errors, timeouts, or empty reads
- a local Stitch operation journal for truthful mutation state and explicit
  ambiguous-timeout recovery
- Stitch screen and screenshot intake
- stable queued save/download and intake manifest generation for refreshed screenshots and HTML
- source artwork extraction from Stitch HTML into `.stitch/intake/assets/`
- screenshot-to-feature-map synthesis
- product-driven concept coverage so required missing screens remain actionable
  expansion work without imposing a fixed screen set or count
- quality-controlled `.stitch/APP.md` section 9 generation before roadmap and baton creation
- visual-spine planning and screen-level implementation packets so native work preserves the creative identity from Stitch
- automated native SwiftUI Xcode scaffolding with app-specific target/module/scheme naming
- placeholder cleanup so `MyApp` does not leak into implementation destinations
- refresh mode when new Stitch screens should update APP.md, DESIGN.md, metadata, roadmap, or baton
- maturity-transition audit so prototype closeout can advance into dogfood tasks instead of stopping prematurely
- a bounded concept acceptance loop so material clipping, overflow, generic
  treatment, and weak product identity receive edit/variant attempts without
  making perfect Stitch output a scaffold blocker
- a non-blocking bootstrap receipt with Stitch identity, native target/scheme,
  first build result, active task, baton validation, risks, and the exact next
  prompt

## Roadmap / baton expectations
- roadmap items should use the current task template
- the active baton should use the current baton schema
- metadata should record evidence, maturity, risk, and task-injection history when relevant
- placeholder values such as `[PRIMARY_PLATFORM]` are expected only in the untouched source template
- after bootstrap, validate the baton normally so unresolved placeholders fail; use `--allow-placeholders` only when validating the distributable source template itself

## Local plugin note
This template ships a bundled repo-local plugin copy for developers who intentionally want to install the packaged framework. Keep the default marketplace empty unless the repo intentionally opts into that local plugin surface.
