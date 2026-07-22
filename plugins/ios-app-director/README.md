# iOS App Director Plugin

`iOS App Director` packages the autonomous, roadmap-driven NATIVE READY engine into a
staged Codex plugin bundle. The framework was designed and iterated in Codex
CLI and the Codex desktop app with GPT-5.5 and GPT-5.6.

## Execution model
Autonomous means the live workflow can keep advancing from goal to roadmap to
baton to implementation and validation with minimal hand-holding. It can choose
the next actionable task, build, inspect the result, update persistent project
memory, and continue until it reaches a genuine blocker or decision boundary.

The engine runs inside an active Codex session rather than as a detached
background daemon. Codex supplies reasoning and execution, XcodeBuildMCP closes
the native build-and-simulator loop, Stitch drives visual exploration, and
Cloudflare MCP can support backend and service delivery when needed.

## What the framework adds
- maturity-aware behavior
- anticipatory roadmap intelligence
- regression discipline
- stronger evidence rigor
- periodic cross-feature architecture review
- more production-minded roadmap growth

## What it bundles
- a master orchestration skill for iOS app delivery
- one public bootstrap skill that owns setup through first simulator launch and receipt
- an explicit/internal design-first setup coordinator used by bootstrap when needed
- a Stitch iOS concept builder for generating first-pass concept screens
- a Stitch iOS intake skill for collecting screens, screenshot evidence, HTML exports, source image assets, design-system signals, and stable intake manifests
- an iOS feature-map skill for turning screenshots/notes into `.stitch/APP.md` section 9
- an iOS visual-spine skill for comparing Stitch references with native simulator screenshots and preserving product-critical artwork, image treatment, mood, and component personality
- an iOS native scaffold skill for creating the initial SwiftUI Xcode project and replacing `MyApp` placeholders
- a feature closeout skill for repeatable validation and handoff
- the roadmap-driven `stitch-loop-ios` skill
- the AI app development engine specs
- a definition-of-done reference
- the repo-root starter pack files used for new app setup
- optional MCP wiring in `.mcp.json` for:
  - XcodeBuildMCP
  - Cloudflare MCP
  - Stitch MCP

## Bundled skills
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

## Plugin intent
This plugin is meant to help a coding agent:
1. bootstrap a new iOS app repo through a real Xcode project, first simulator launch, validated baton, and non-blocking receipt
2. start from Stitch concepts and screenshot evidence when that is the strongest product seed
3. establish repo-local memory and source-of-truth docs
4. create a native SwiftUI Xcode scaffold without a manual Xcode step
5. maintain a roadmap + baton loop
6. use Stitch for concept work when helpful
7. implement and validate SwiftUI features with XcodeBuildMCP
8. wire Cloudflare-backed service layers where needed
9. keep development moving through live debug cycles with stronger regression and evidence discipline

## Requirements

Complete NATIVE READY bootstrap requires a compatible Mac and Xcode installation, an
iOS Simulator runtime, Codex Desktop or Codex CLI, XcodeBuildMCP, and one active
copy of the 10 NATIVE READY skills. Automatic Stitch concept generation additionally
requires a Google account with Stitch access and a Stitch API key exposed to
Codex as `STITCH_API_KEY`. Cloudflare and Apple Developer Program access are
conditional on backend and distribution scope.

The packaged starter's `SETUP.md` contains the prerequisite matrix and current
verification commands.

## Included resources
- `references/ai-app-development-engine-spec.md`
- `../../docs/definition-of-done.md`
- `../../README.md`
- `../../AGENTS.md`
- `../../.stitch/`
- `../../docs/`
- `../../workers/`

## Install behavior
Install the packaged plugin globally from the public NATIVE READY marketplace:

```bash
codex plugin marketplace add mattglass/Native-Ready --ref main
codex plugin list
codex plugin add ios-app-director@repo-local-plugins
```

Start a new Codex task after installation. Authentication is deferred until a connection is used, so installation does not require optional Cloudflare or Stitch credentials. Use `.agents/plugins/marketplace.opt-in-ios-app-director.json` only for isolated local package testing, and avoid activating it alongside the global plugin or manual copies of the same skills.

## Connect Google Stitch

Stitch uses API-key authentication for the quick personal setup. Codex's generic
**Authenticate** action starts an OAuth registration flow, which is not the
setup path for the Stitch MCP endpoint. If that button produces no browser
window, create and supply a Stitch API key instead:

1. Sign in at [Google Stitch](https://stitch.withgoogle.com/).
2. Open [Stitch Settings](https://stitch.withgoogle.com/settings), choose **API Keys**, select **Create key**, and copy the new key.
3. Make the key available as `STITCH_API_KEY` to the process that launches Codex.
4. Fully quit and reopen Codex Desktop, or start a new Codex CLI process, then open a new task.

Google's detailed instructions are in the [Stitch MCP setup guide](https://stitch.withgoogle.com/docs/mcp/setup/). A Google AI Studio key is a Gemini API credential; it is not the documented replacement for a key created in Stitch Settings.

Never paste the key into a Codex conversation, commit it, or put the literal
value in `.mcp.json` or `.codex/config.toml`.

On macOS, a NATIVE READY source checkout includes a hidden-input helper that
makes the key available to Codex Desktop for the current login session:

```bash
./plugins/ios-app-director/scripts/configure-stitch-api-key-macos.sh
```

To clear it later:

```bash
./plugins/ios-app-director/scripts/configure-stitch-api-key-macos.sh --clear
```

For Codex CLI, keep the key only in the terminal session that launches Codex:

```bash
read -rs "STITCH_API_KEY?Paste your Stitch API key: "
printf '\n'
export STITCH_API_KEY
codex
unset STITCH_API_KEY
```

## MCP wiring

The plugin manifest registers the included `.mcp.json`. It provides:

- XcodeBuildMCP through `npx`
- Cloudflare MCP, whose **Authenticate** action opens the supported OAuth flow
- Google Stitch MCP, whose `X-Goog-Api-Key` header is read from `STITCH_API_KEY`

Before using the MCP tools, confirm:

- XcodeBuildMCP can run locally through `npx`.
- Cloudflare MCP OAuth or bearer-token auth is configured when Cloudflare is in scope.
- `STITCH_API_KEY` is configured for the target Google/Stitch account when Stitch is in scope.

Cloudflare remains optional unless the app needs backend work. Stitch remains
optional when bootstrap can proceed from screenshots, notes, or a product brief.

## Design-first workflow
`ios-app-bootstrap` is the public front door for the design-first path. It may
use the internal setup coordinator and the same 10 NATIVE READY skills whether they
come from global installs or the opt-in bundled plugin copy. It can:
- generate first-pass Stitch screens from bootstrap answers
- keep one active Stitch project identity through setup and later art expansion,
  with a local operation journal for provenance and timeout recovery
- inspect a live Stitch project and capture screenshot evidence
- save Stitch screenshot/HTML URLs through one stable queued command and rebuild `.stitch/intake/intake-manifest.*` so new filenames do not require path-specific shell approvals
- extract source artwork from saved Stitch HTML into `.stitch/intake/assets/` and `.stitch/intake/image-asset-manifest.*`
- turn screenshots, prompt notes, and Google Docs into a quality-controlled feature map
- run a visual-spine audit so early native tasks preserve the concept's product-critical artwork, image-forward cards, motifs, and same-product-family feel
- write that feature map into `.stitch/APP.md` before roadmap and baton creation
- generate the native SwiftUI Xcode project with a real target/module/scheme name before implementation starts
- replace active `MyApp` destination placeholders in app memory
- refresh repo memory when a Stitch project gains new screens after setup
- audit APP.md, design intake, metadata, and new Stitch evidence before treating prototype closeout as a no-next-task stopping point
- audit requested concept coverage so missing required screens remain active
  Stitch expansion work instead of silently disappearing at handoff
- run a bounded core-concept acceptance loop without making perfect Stitch
  output a prerequisite for native scaffolding
- render `docs/bootstrap-receipt.md` with the first build result, active task,
  baton validation, unresolved risks, and exact delivery prompt

## Repo-local staging
This bundle is staged as a repo-local plugin at:
- `plugins/ios-app-director/`

## Notes
- The bundled plugin copy should stay aligned with the global `ios-app-director` engine.
- The current framework uses the current roadmap, baton, evidence, and maturity schemas.

## Validation
Run the dependency-free script tests from the NATIVE READY repo root:

```bash
python3 -m unittest discover -s plugins/ios-app-director/tests -v
```

## License
The `ios-app-director` plugin is available under the MIT License, Copyright (c) 2026 Matt Glass. Its manifest remains identified as `MIT`; see this package's `LICENSE`.

The embedded NATIVE READY engine template at `skills/ios-app-bootstrap/templates/ai-app-engine/` is an explicit exception. That subtree remains licensed under Apache 2.0 and carries its own license and attribution files under `LICENSES/`. See `LICENSING.md` for the exact package boundary.

Applications and other output created with the plugin are not automatically licensed under MIT or Apache 2.0. Their authors choose the license for their own work, subject to applicable third-party terms and preservation of the Apache 2.0 license and NOTICE when NATIVE READY source files or substantial portions are redistributed.
