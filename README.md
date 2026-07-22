# NATIVE READY - Autonomous iOS App Development Engine

## Purpose
NATIVE READY is an autonomous, roadmap-driven iOS app development engine designed and
built entirely with Codex CLI and the Codex desktop app, using GPT-5.5 and
GPT-5.6. It bundles 10 specialized skills in the `ios-app-director` plugin
with a reusable app scaffold, persistent project memory, design-first planning,
native SwiftUI delivery, and live validation loops.

Once an app is bootstrapped and a goal is active, NATIVE READY can keep the build
moving: select the next roadmap task, explore or interpret Stitch concepts,
implement native features, validate them with XcodeBuildMCP, capture evidence,
update the baton, and continue until a real blocker or product decision needs a
human. The result is meant to feel less like prompting a code generator and
more like directing an AI-powered product team that remembers where it is going.

## Execution model
“Autonomous” describes how the development loop behaves inside an active Codex
session with the permissions and tools the developer provides. NATIVE READY is not a
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

NATIVE READY's complete native loop requires a compatible Mac, Xcode 16 or newer,
an iOS Simulator runtime, Codex Desktop or Codex CLI, one active copy of the 10
NATIVE READY skills, and XcodeBuildMCP. The automatic design-first path also requires
a Google account with Stitch access plus a Stitch API key supplied to Codex as
`STITCH_API_KEY`. Cloudflare and Apple Developer Program access are conditional
on the app's backend and distribution needs.

See [SETUP.md](SETUP.md) for the current prerequisite matrix, quick checks,
tool authentication, and the distinction between required and optional
capabilities.

## Core layers
### Global engine layer
The shared intelligence can be installed globally as the complete 10-skill
NATIVE READY suite:

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
a separate workflow tier. These 10 skills are the complete NATIVE READY workflow:
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
  plugins/                 # full NATIVE READY source checkout only
    ios-app-director/
  workers/
```

## How to use this template
1. Create a new app folder/repo. Either clone, copy, or unzip this template, or start with an empty folder and the globally installed plugin.
2. Open Codex Desktop or Codex CLI at that repo root and make the complete app brief the first message.
3. Use `$ios-app-bootstrap` as the single public setup entry point. From an empty folder, the installed skill safely deploys its embedded READY starter pack before preflight; it does not copy the plugin source into the app repo.
4. Read `SETUP.md` and complete the required Xcode, Codex, skill, MCP, and account preflight. `docs/bootstrap-prompt.md` is available after deployment, and `docs/design-first-setup-prompt.md` adds advanced Stitch inputs to that same entry point.
5. Let bootstrap inspect or create design evidence, generate the feature map, create the native SwiftUI scaffold, run the first simulator build/launch, validate the baton, and write `docs/bootstrap-receipt.md`.
6. After a `ready_for_delivery` receipt, use the documented `/goal` prompt and `ios-app-director` for autonomous delivery.
7. Use `ios-feature-closeout` to reconcile roadmap, baton, evidence, risk, and next-step handoff after meaningful work.

## Install iOS App Director globally
The NATIVE READY source repository publishes the complete 10-skill suite through its standard Codex marketplace. Add the public GitHub repository as a marketplace, confirm that Codex can see the package, and install it:

```bash
codex plugin marketplace add mattglass/Native-Ready --ref main
codex plugin list
codex plugin add ios-app-director@repo-local-plugins
```

Start a new Codex task after installation so the bundled skills are loaded. Do not also install manual copies of the same `ios-app-*` and `stitch-ios-*` skills; choose the plugin or the individual global skills as the single active source.

To refresh an existing installation after a new release, run `codex plugin marketplace upgrade repo-local-plugins`, then reinstall `ios-app-director@repo-local-plugins` and start a new task.

### Local bundled-plugin testing
Developers working from the full NATIVE READY source checkout can use `.agents/plugins/marketplace.opt-in-ios-app-director.json` for isolated local packaging tests. The source repository's standard `.agents/plugins/marketplace.json` is the GitHub-installable catalog and points at the same `plugins/ios-app-director/` package.

App repos produced from the bundled bootstrap template intentionally receive an empty standard marketplace, so they do not advertise a second local plugin after a global installation. Their opt-in marketplace remains available for isolated testing when the local `plugins/ios-app-director/` package is also present.

The plugin manifest registers its included `.mcp.json` for XcodeBuildMCP, Cloudflare MCP, and Stitch MCP. Cloudflare is bundled but disabled by default; enable and authenticate it only when the app needs Cloudflare services. Stitch reads `STITCH_API_KEY`; the generic OAuth **Authenticate** action is not its setup path. See [SETUP.md](SETUP.md) for the Cloudflare opt-in flow, direct Stitch Settings link, and secure macOS/CLI setup.

## Design-first workflow
The default bootstrap is also the design-first path. Use
`docs/design-first-setup-prompt.md` when the first message needs richer Stitch
inputs; it still starts with `$ios-app-bootstrap`. The bootstrap may use the
internal setup coordinator and other NATIVE READY specialists to provide:
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
The NATIVE READY source repository ships a bundled repo-local plugin copy and a standard marketplace entry for global installation from GitHub. The generated-app template keeps its standard marketplace empty. Its separate opt-in marketplace remains available for isolated local packaging tests when the bundled package is present.

## License
The NATIVE READY orchestration engine, its root documentation, and the embedded engine template are available under the Apache License 2.0, Copyright 2026 Matt Glass. The source repository carries the full terms in its root `LICENSE` and attribution in `NOTICE`. Generated app templates preserve those materials in `LICENSES/NATIVE-READY-APACHE-2.0.txt` and `LICENSES/NATIVE-READY-NOTICE.txt`.

The separately packaged `ios-app-director` plugin remains available under the MIT License, except for its embedded `skills/ios-app-bootstrap/templates/ai-app-engine/` subtree, which remains Apache-2.0-licensed NATIVE READY engine material. The source repository and plugin package each include a `LICENSING.md` map for the exact file boundaries.

Applications and other output created with NATIVE READY are not automatically licensed under Apache 2.0 or MIT. Their authors choose the license for their own work, subject to applicable third-party terms and preservation of the Apache 2.0 license and NOTICE when NATIVE READY source files or substantial portions are redistributed.

Neither license grants permission to use the NATIVE READY name or logos in a way that implies endorsement, sponsorship, or official origin.
