---
name: ios-app-bootstrap
description: Single public entry point for starting or repairing a READY iOS app workspace. Use when a user provides a new app idea, asks what to do first, asks to bootstrap or kick off an app, or needs a missing native project created. Coordinates product memory, design evidence, feature mapping, native SwiftUI scaffolding, first simulator build/launch, and a non-blocking bootstrap receipt before delivery begins.
---

# iOS App Bootstrap

Turn a raw app idea or copied READY template into a runnable, roadmap-driven iOS workspace. Keep this skill as the user-facing setup entry point in both Codex and Codex CLI. Delegate internally to the other READY skills without asking the user to choose another setup front door.

## Required references

Read:

- `templates/ai-app-engine/README.md`
- `templates/ai-app-engine/docs/app-build-spec.md`
- `references/bootstrap-questionnaire.md`
- `references/bootstrap-scaffold-rules.md`
- `references/bootstrap-completion-contract.md`
- `references/app-maturity-model.md`
- `references/roadmap-task-template.md`
- `references/baton-schema.md`
- `references/metadata-evidence-schema.md`

When a delegated phase applies, read that READY skill before executing it:

- `stitch-ios-concept-builder`
- `stitch-ios-intake`
- `ios-feature-map`
- `ios-visual-spine`
- `ios-native-scaffold`
- `ios-setup-orchestrator` only as an internal coordinator when its full pipeline is useful

## Completion boundary

Bootstrap is complete only when the repository has coherent operating memory, a real native Xcode project, a discovered scheme, an attempted first simulator build/launch, a valid active baton, and `docs/bootstrap-receipt.md` describing the actual result.

Do not stop after documentation or Stitch generation alone. Do not begin product-feature delivery after the receipt unless the user also asked to build the app, supplied an active `/goal`, or explicitly asked to continue into `ios-app-director` delivery.

## Workflow

### 0. Deploy or repair the READY base

Do not assume the app repository already contains the READY starter files or a
local `plugins/ios-app-director/` source checkout. Resolve
`<ios-app-bootstrap-skill-dir>` as the directory containing this active
`SKILL.md`, then run:

```text
python3 <ios-app-bootstrap-skill-dir>/scripts/deploy_ready_template.py --repo-root /absolute/path/to/app-repo
```

Run this before the Xcode preflight so a new or blocked workspace still receives
the operating memory and receipt surfaces. The default merge creates missing
files, leaves identical files alone, and preserves differing existing files.
Review preserved conflicts; use `--overwrite` only when replacing those exact
files is intentional. The embedded app template is the deployment source of
truth. Do not copy the plugin package itself into a generated app repository.

### 1. Preflight the environment

Classify each capability as `required`, `optional`, or `not_in_scope`:

- Codex workspace access
- Xcode and an installed target simulator runtime
- XcodeBuildMCP
- Stitch MCP and account access
- Cloudflare or other backend tooling

Xcode and XcodeBuildMCP are required for READY bootstrap completion. Stitch is required when the user makes Stitch a hard requirement; otherwise unavailable Stitch is a degraded design-input path, not a reason to skip the native scaffold. Cloudflare is optional unless the first runnable slice needs it.

Run `xcodebuild -version` before native scaffold generation. Xcode 16 is the firm minimum supported toolchain. If Xcode is missing or its major version is below 16, classify the capability as `unsupported_toolchain`, write or refresh the blocked bootstrap receipt, and stop before generating the native project. Do not downgrade the project format, Swift language mode, or deployment target to accommodate Xcode 15. Run the current XcodeBuildMCP doctor after the version gate and keep any independent doctor failure explicit.

Before the first Stitch call, check whether `STITCH_API_KEY` is available to the current Codex process without printing or exposing its value. If it is absent:

- classify Stitch as `api_key_required`, not as a generic OAuth or account failure
- direct the user to [Stitch Settings](https://stitch.withgoogle.com/settings) and the plugin's secure macOS helper; never ask them to paste the key into the conversation
- tell Codex Desktop users to fully quit and reopen Codex after setting the key
- when Stitch is optional, continue the independent native path and record the exact resume action in the receipt
- when Stitch is required, pause only the Stitch-dependent phase

If the key is present but Stitch still returns `auth_required`, classify that as a key-propagation or key-validity problem and preserve the same project identity. Do not start the generic OAuth **Authenticate** flow for Stitch.

Ask only for a missing product decision or credential that prevents meaningful progress. Record tool/account problems precisely in the receipt.

### 2. Establish the project frame

Gather or infer:

- app name, purpose, platform, and target users
- three to five must-have capabilities
- visual tone and available design evidence
- app maturity, defaulting to `prototype`
- backend scope
- app-specific target, scheme, source-root, and bundle-identifier plan

Never retain `MyApp` or another unrelated app's target/test names. Derive test target names from the native target. A `com.example.*` bundle identifier is acceptable only as an explicitly provisional simulator value and must be labeled that way in memory and the receipt.

### 3. Fill or repair repo memory

Create or update:

- `AGENTS.md`
- `docs/app-build-spec.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/metadata.json`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`

Reconcile `AGENTS.md` with the actual native identity after scaffold creation. Keep global Codex guidance generic; app-specific target, scheme, test-target, and tool names belong in this repository.

### 4. Build the design evidence path

When Stitch is in scope and usable:

1. Use `stitch-ios-concept-builder` in one provenance-backed Stitch project.
2. Define product-driven required concept roles rather than a fixed screen count.
3. Inspect every required core result for hierarchy, clipping, overflow, generic treatment, and product-specific visual identity.
4. Use edit or variant operations for material defects, with at most two corrective attempts per core role during bootstrap.
5. Keep the strongest usable result and record remaining visual gaps as roadmap work.
6. Use `stitch-ios-intake`, `ios-feature-map`, and `ios-visual-spine` to preserve the design system, artwork, feature requirements, and implementation packets.

An ambiguous Stitch mutation prevents an untracked replacement of that same operation; it does not prevent independent intake, memory repair, native scaffolding, or build validation. Never make an optional missing concept the active baton when a dependency-safe native task can proceed.

When Stitch is unavailable or not in scope, use user-provided screenshots/notes or establish a concise native design direction from the product brief. Report the degraded design path honestly.

### 5. Create the first roadmap and baton

Use the current roadmap and baton schemas. The active baton must point to exactly one dependency-safe executable task.

- Before scaffold creation, the native scaffold task may be active.
- After scaffold validation, activate the first native visual/product slice.
- Keep unresolved optional concepts, reports, and service work in the roadmap or risk register rather than using them to deadlock the baton.

Resolve `<ios-app-director-skill-dir>` as the directory containing the active
`ios-app-director/SKILL.md`, then run
`python3 <ios-app-director-skill-dir>/scripts/validate_baton_frontmatter.py --repo-root .`
after writing the baton. Fix malformed or unresolved active placeholders. Do
not assume that script lives inside the app repository.

### 6. Create and validate the native scaffold

If a real Xcode project is missing:

1. Use `ios-native-scaffold`.
2. Derive an app-specific target, module, scheme, source root, app entry type, and test-target name.
3. Replace active placeholder native paths in repo memory.
4. Confirm XcodeBuildMCP defaults when needed.
5. Discover the generated scheme.
6. Run `build_run_sim` for the first simulator build/launch.
7. Make the Simulator visible with XcodeBuildMCP's `open_simulator` when available, or `open -a Simulator` as a local fallback. Xcode itself does not need to open for command-line builds.
8. Capture a screenshot or equivalent launch evidence when practical.

Do not infer a successful launch from a successful build, app installation, a booted device, or a Simulator spinner. Require the app process or visible app UI. If build or launch fails, diagnose and repair setup defects before handing off. Stop only for a concrete tool, signing, platform, or product blocker supported by evidence.

### 7. Write the non-blocking receipt

Run:

```text
python3 <ios-app-bootstrap-skill-dir>/scripts/render_bootstrap_receipt.py --repo-root . --toolchain-status <supported|unsupported_toolchain|unavailable|unknown> --scheme-discovered <yes|no|unknown> --first-build-result <succeeded|failed|not_run|unknown> --first-launch-result <succeeded|failed|not_run|unknown> --baton-validation <passed|failed|not_run|unknown>
```

Add `--stitch-status`, `--build-evidence`, `--launch-evidence`, and repeatable `--note` values when useful. Keep build and launch results independent: a successful compile does not turn a failed launch into success. The renderer reports state and always leaves remediation visible; receipt completeness is never itself a gate.

The receipt must name:

- app and repository identity
- Stitch project/status
- generated native project, target, scheme, and bundle identifier
- first build/launch result and evidence
- active roadmap task
- baton validation result
- unresolved setup risks
- exact next prompt

### 8. Hand off cleanly

End in one of three truthful states:

- `ready_for_delivery`: native project exists, its scheme was discovered, first build/launch succeeded, and the validated baton identifies the next delivery task
- `partial`: useful setup exists but a named validation or optional design capability remains incomplete
- `blocked`: no meaningful native continuation is possible without a concrete external action or user decision

For `ready_for_delivery`, recommend the documented `/goal` prompt. Continue directly only when the user's current request already authorizes delivery.
