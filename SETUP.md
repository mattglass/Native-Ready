# NATIVE READY iOS App Setup

NATIVE READY turns a copied template and an app idea into coherent project memory, design evidence, a native SwiftUI Xcode project, a first simulator launch, and a roadmap baton for autonomous delivery.

Use the same public entry point in Codex Desktop and Codex CLI: `ios-app-bootstrap`.

## 1. Requirements

### Required for a complete bootstrap

| Requirement | Why NATIVE READY needs it | Check |
| --- | --- | --- |
| A Mac that supports the installed Xcode version | Native iOS builds and Simulator require macOS and Xcode | Compare your Mac/Xcode combination with [Apple's Xcode requirements](https://developer.apple.com/xcode/system-requirements/) |
| Xcode with the intended iOS SDK and at least one iPhone Simulator runtime | NATIVE READY creates, builds, launches, and inspects a real SwiftUI app | Open Xcode once and finish any component/runtime installation |
| Codex Desktop or Codex CLI, signed in | Codex supplies the reasoning and execution session | Start Codex in the copied NATIVE READY repo root |
| Workspace trust and write permission for the copied repo | Bootstrap must update memory, generate the Xcode project, and capture evidence | Allow the repo path when Codex asks |
| One active copy of the 10 NATIVE READY skills | The skills define the bootstrap, design, scaffold, delivery, and closeout contracts | Use either the global skills or the bundled plugin—not both |
| XcodeBuildMCP | NATIVE READY uses it for scheme discovery, simulator build/run, screenshots, logs, and UI checks | Run its doctor or confirm `session_show_defaults` is available in Codex |

XcodeBuildMCP currently documents macOS 14.5+, Xcode 16+, and Node.js 18+ for its npm/npx installation path. A Homebrew installation does not require Node.js. Follow the current [XcodeBuildMCP installation guide](https://www.xcodebuildmcp.com/docs/installation) when those requirements change.

This template targets iOS 26 by default, so use an Xcode release that includes the iOS 26 SDK and install an iOS 26 Simulator runtime. If you retarget the template, use the matching SDK/runtime instead.

### Required for automatic Stitch design generation

- a Google account with access to [Stitch](https://stitch.withgoogle.com/)
- access to the intended Stitch project, or permission to create one
- Stitch MCP configured and authenticated for that account
- internet access while generating, editing, or retrieving Stitch artifacts

Follow Google's current [Stitch MCP setup guide](https://stitch.withgoogle.com/docs/mcp/setup/). This template's `.codex/config.toml` sends the `X-Goog-Api-Key` header from the `STITCH_API_KEY` environment variable. Keep the real key outside the repo, make it available to the environment that launches Codex Desktop or Codex CLI, and restart Codex after changing it. Never commit the key or paste it into `.codex/config.toml`.

Stitch is the preferred concept path for the full design-first experience. If Stitch is unavailable and the user did not make it a hard requirement, bootstrap should continue from screenshots, notes, or a product brief, create the native scaffold, and report the degraded design path in `docs/bootstrap-receipt.md`.

### Required only for devices or later distribution

- no Apple Developer Program membership is required for Simulator-only bootstrap
- an Apple Account and signing configuration may be needed for physical-device development
- Apple Developer Program membership is needed for TestFlight and App Store distribution
- a final reverse-domain bundle identifier is needed before distribution; `com.example.*` is simulator-only and must remain labeled provisional

### Optional services

- Cloudflare access and authenticated Cloudflare tooling are needed only when the app actually requires Workers, storage, APIs, or other Cloudflare services.
- Git, GitHub, CI, and a changelog are recommended for shipping software but are not prerequisites for copying or locally testing NATIVE READY.
- The bundled local plugin is optional when the matching global skills are installed.

### Quick local checks

```bash
xcode-select -p
xcodebuild -version
node --version
npm --version
codex --version
codex mcp list
```

`node`, `npm`, and `codex` may be absent when using the Homebrew XcodeBuildMCP path and Codex Desktop instead of Codex CLI. For the npm/npx path, run:

```bash
npx --package xcodebuildmcp@latest xcodebuildmcp-doctor
```

## 2. Copy The Template

Copy or unzip `APP-TEMPLATE-FOR-AI-BUILD-NATIVE-READY` into a new app folder:

```text
/Users/you/Sites/MYAPP/
```

The copied folder is always the operating repo root. The generated Xcode project will normally live in a nested app container:

```text
MYAPP/
  MyRealTargetApp/
    MyRealTarget.xcodeproj
    MyRealTarget/
```

Keep Codex opened at `MYAPP/`, where `AGENTS.md`, `docs/`, `.stitch/`, and `plugins/` live. Do not start the task from the nested Swift source folder.

## 3. Choose One NATIVE READY Skill Source

The complete NATIVE READY suite contains exactly these 10 skills:

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

### Recommended: install the global plugin

Install the complete suite once from the public NATIVE READY repository:

```bash
codex plugin marketplace add mattglass/Native-Ready --ref main
codex plugin list
codex plugin add ios-app-director@repo-local-plugins
```

Start a new Codex task after installation. If the marketplace was already added, refresh it with `codex plugin marketplace upgrade repo-local-plugins`, reinstall the plugin, and start another new task.

Use only one copy of each skill. If the same 10 skills were installed manually at user scope, remove or disable those copies before using the plugin.

### Bundled plugin: packaging or isolated testing

The NATIVE READY source repository packages the same 10 skills in:

```text
plugins/ios-app-director/
```

The source repository's standard `.agents/plugins/marketplace.json` exposes this package for the global installation commands above. App repos produced from the bundled bootstrap template intentionally receive an empty standard marketplace, so they do not advertise another local copy after a global installation.

Use `.agents/plugins/marketplace.opt-in-ios-app-director.json` only for isolated local packaging tests in a checkout that also contains `plugins/ios-app-director/`, and do not activate it alongside a global installation.

The bundled plugin is skills-only by default; `plugins/ios-app-director/.mcp.json` is reference wiring rather than automatically enabled configuration.

## 4. Configure The Tool Connections

The bundled MCP reference defines:

- `xcodebuildmcp` through `npx`
- `stitch` through Google's Stitch MCP endpoint
- `cloudflare-api` through Cloudflare's MCP endpoint

Prefer already configured global MCP connections. If you intentionally use plugin-local wiring, add `"mcpServers": "./.mcp.json"` to the plugin manifest, reinstall/reload the plugin, and authenticate the services you need.

Before bootstrap:

1. Confirm XcodeBuildMCP starts and exposes `session_show_defaults` and `build_run_sim`.
2. If Stitch is in scope, confirm the Stitch connection can list or access projects.
3. Treat Cloudflare authentication as optional unless the first runnable slice depends on it.
4. Restart Codex after changing global skill or MCP configuration.

## 5. Start The Same Way In Codex Desktop Or CLI

Open a fresh task at the copied repo root and make the complete product brief the first message. Use [docs/bootstrap-prompt.md](docs/bootstrap-prompt.md), or start with this compact form:

```md
Use $ios-app-bootstrap as the single NATIVE READY setup entry point for this repo.

App name: [APP_NAME]
App idea: [SHORT_PRODUCT_IDEA]
Target users: [WHO_IT_IS_FOR]
Platform: [IPHONE_ONLY or IPHONE_AND_IPAD]
Must-have features:
- [FEATURE_1]
- [FEATURE_2]
- [FEATURE_3]
Visual tone: [DESIGN_FEEL]
Stitch project: [PROJECT_NAME_OR_ID or NONE_YET]
Stitch role: [PRIMARY / REFERENCE / NOT_IN_SCOPE]
Cloudflare needed now: [YES or NO]
Bundle identifier: [FINAL_ID or PROVISIONAL]

Complete bootstrap through a generated native Xcode project, first simulator build/launch, validated active baton, and docs/bootstrap-receipt.md. Keep optional Stitch or service gaps visible without letting them block independent native setup. Stop after the receipt unless this prompt also explicitly authorizes product-feature delivery.
```

Do not begin with a separate “What should I do?” turn and paste the product brief later. Giving the product frame in the first message produces the same routing context in both Codex surfaces.

`ios-app-bootstrap` may internally coordinate the other NATIVE READY skills. You should not need to choose `ios-setup-orchestrator` as a second front door.

## 6. Bootstrap Completion Contract

Bootstrap should progress through:

1. environment preflight
2. app identity and build specification
3. Stitch concepts or an explicitly degraded design path
4. design intake, feature map, and visual spine
5. roadmap, metadata, and valid baton
6. native SwiftUI Xcode scaffold
7. scheme discovery and first simulator build/launch
8. `docs/bootstrap-receipt.md`

The receipt records:

- Stitch project/status
- generated target, scheme, project path, and bundle identifier
- first build/launch result and evidence
- active roadmap task
- baton validation result
- unresolved setup risks
- exact next prompt

The receipt is informational. Missing optional evidence or an imperfect Stitch result should produce a `partial` receipt and actionable follow-up—not erase completed work or block a dependency-safe scaffold.

Expected repository outputs include:

- product-specific `AGENTS.md` and `docs/app-build-spec.md`
- `.stitch/APP.md`, `.stitch/DESIGN.md`, `.stitch/ROADMAP.md`, `.stitch/next-prompt.md`, and `.stitch/metadata.json`
- Stitch intake manifests, screenshots, HTML, source artwork, and screen packets when available
- a generated app-specific `.xcodeproj`
- first build/run evidence when capture is available
- `docs/native-scaffold.md`
- `docs/bootstrap-receipt.md`

No active target, source path, scheme, or test target should retain `MyApp` or another unrelated template name.

## 7. Begin Autonomous Delivery

After the receipt reports `ready_for_delivery`, start the delivery loop with:

```md
/goal Build autonomously toward the v1 app until the planned features work, the roadmap is reconciled, validation evidence is captured, and the app is ready for real user testing.

Use $ios-app-director to continue from the active baton.

Keep implementing, validating with XcodeBuildMCP, updating evidence and repo memory, and advancing the roadmap until a real blocker or product decision requires me.
```

Bootstrap and delivery can be requested together in one message, but the two-phase flow is easier to inspect: first obtain a runnable scaffold and receipt, then activate the delivery goal.

## 8. Refresh Design Evidence Later

When Stitch screens change after bootstrap, use `stitch-ios-intake` in refresh mode, then `ios-feature-map` and `ios-visual-spine` as needed. Preserve completed build evidence, refresh the stable intake manifests, and update roadmap/baton state only when the new evidence changes implementation scope or priority.

Use `stitch-loop-ios` when a delivery task needs another bounded generation, edit, or variant pass before native implementation.

## 9. Troubleshooting

- **No Xcode project appeared:** resume `$ios-app-bootstrap`; memory-only output is not complete bootstrap.
- **A Stitch mutation timed out:** record the ambiguous operation, avoid an untracked replacement, and continue independent native setup when possible.
- **A missing optional screen became the active blocker:** move it to a dependency-correct roadmap task and activate the best executable native task.
- **A legacy Stitch wrapper appeared:** retire or disable its implicit global invocation; it is not part of the 10-skill NATIVE READY bundle.
- **A generic or unrelated target/test target appeared:** remove stale global/project instructions and derive names from the current app.
- **Cloudflare auth failed in a local-only app:** classify Cloudflare as optional or not in scope and continue.
- **Desktop and CLI differ:** verify the same Codex version, model/effort, first-turn prompt, workspace root, skill source, permissions, and MCP availability before comparing results.
