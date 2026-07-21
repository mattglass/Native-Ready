# Project Context

## Overview

- App name: `[APP_NAME]`
- Platform focus: `[PRIMARY_PLATFORM]`
- App purpose: `[APP_PURPOSE]`
- Primary target user: `[TARGET_USER]`
- Current phase: `[PHASE: prototype / dogfood / beta / release_candidate / production]`

## Product Priorities

Prioritize:

- `[PRIORITY_1]`
- `[PRIORITY_2]`
- `[PRIORITY_3]`

## Architecture

- Main app target: `[MAIN_TARGET_NAME]`
- Test target: `[TEST_TARGET_NAME]`
- Native project path: `[NATIVE_PROJECT_PATH]`
- Native source root: `[NATIVE_SOURCE_ROOT]`
- Scheme: `[NATIVE_SCHEME]`
- Bundle identifier: `[BUNDLE_IDENTIFIER]`
- Preferred architecture: `[ARCHITECTURE_STYLE]`
- UI framework: `[UI_FRAMEWORK]`
- Data/storage notes: `[LOCAL_STORAGE_AND_MODEL_NOTES]`
- Navigation notes: `[NAVIGATION_PATTERN]`

## Build and Validation

- Preferred build tool: `[BUILD_TOOL]`
- Primary validation environment: `[SIMULATOR_OR_DEVICE_TARGET]`
- Use real build/run loops before claiming completion
- Treat successful build as necessary but not sufficient
- Match validation depth to task type, regression scope, and current app maturity

## Design Direction

- Brand / visual tone: `[VISUAL_TONE]`
- Design system source of truth: `[DESIGN_SOURCE_OF_TRUTH]`
- Stitch usage: `[NOT_IN_SCOPE / CONCEPT_ONLY / MIXED / PRIMARY]`
- Use Stitch semantically, not as literal layout authority

## Backend / Services

- Backend strategy: `[NONE / CLOUDFLARE / OTHER]`
- Key services: `[SERVICE_LIST]`
- App-facing API notes: `[API_NOTES]`
- Current service maturity target: `[LEVEL_0_TO_5]`

## Repo Memory

Treat these as persistent working memory when present:

- `AGENTS.md`
- `docs/app-build-spec.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- `.stitch/metadata.json`
- `.stitch/operations/current.json` when Stitch mutations are active or unresolved

## Plugin / Skill Surface

This repo can be used with global Codex skills or the bundled local plugin copy.
`AGENTS.md` documents the expected surface, but plugin activation still depends
on the Codex session and marketplace configuration.

- Default marketplace file: `.agents/plugins/marketplace.json`
- Optional local plugin marketplace file: `.agents/plugins/marketplace.opt-in-ios-app-director.json`
- Bundled local plugin path: `plugins/ios-app-director/`
- Global skill path when installed: `$CODEX_HOME/skills/` or `~/.codex/skills/`

READY-related skills:

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

For a new app, missing native project, or “what do I do first?” request, use
`ios-app-bootstrap` as the single public setup entry point. It owns setup through
the first simulator launch and `docs/bootstrap-receipt.md`. Treat
`ios-setup-orchestrator` as an explicit/internal coordinator, not a competing
front door. Begin `ios-app-director` delivery only when the user also requested
implementation or activated a delivery goal.

When this repo is the app template source of truth, prefer the bundled local
plugin skill files under `plugins/ios-app-director/skills/` for framework
behavior. Keep global skill copies synced from READY before relying on them in
fresh Codex sessions.

## Debug mode

When the user reports an issue and says `debug mode`, immediately begin the end-to-end debugging cycle for that issue. Do not ask whether to begin or request permission to make ordinary, in-scope code changes.

Inspect and reproduce the problem, trace the relevant code and live behavior, implement the necessary changes, and continue until the issue is verified as fixed or a concrete blocker prevents further progress.

Use this loop:

1. Reproduce and diagnose.
2. Patch the implementation.
3. Rebuild and rerun with XcodeBuildMCP.
4. Use `session_show_defaults` before build, run, or test work when needed.
5. Use `build_run_sim` for the main validation loop.
6. Use `snapshot_ui`, screenshots, logs, and UI automation when they materially help.
7. Retest the exact affected feature end to end.
8. Repeat until the behavior is verified.

Do not stop after analysis or after merely producing a plausible fix.

Completion requires either:

- the exact feature working end to end; or
- a specific blocker supported by errors, logs, or other evidence, together with what is needed to unblock it.

After verification, perform any directly implied validation or closeout step. Do not expand into unrelated work.

Make necessary, reversible changes within the user-designated workspace, including source edits, development configuration changes, API testing, and required commands, while respecting higher-priority instructions, security boundaries, and available tools.

## Agent Rules

- Prefer incremental, validated changes
- Debug live behavior instead of stopping at analysis
- Preserve the design-first source path: Stitch, screenshots, and assets -> feature map -> roadmap and baton -> SwiftUI
- Preserve one active Stitch project identity per design world. Do not create a
  fallback project or use an unproven project ID to recover from a tool error,
  timeout, empty result, or design-system failure.
- Keep creative Stitch exploration autonomous while recording mutation state
  truthfully. Missing required screens remain actionable expansion work, and
  ambiguous timeouts must surface recovery promptly.
- Do not flatten product-critical Stitch artwork or image-forward layouts into generic cards or plain SF Symbols
- Keep service contracts separate from UI placeholders; do not imply live backend, AI, upload, account, sync, or sharing behavior unless it exists and was validated
- Update roadmap, baton, and evidence-bearing project memory as the work evolves
- Do not assume conceptual designs outrank the live implementation
- Ask only the most important missing questions before starting work
- Consider app maturity before injecting release-readiness, refactor, or regression tasks
- Trigger cross-feature architecture review when reusable patterns or seams begin to drift
- During an active delivery goal, when you have nothing else to worry about, keep building
- During bootstrap, stop after the first validated launch and receipt unless the current request also authorizes product-feature delivery
- Never inherit `MyApp` or another repository's target, scheme, test-target, or tool names; derive app-specific values and keep them repo-local

## Workspace Boundaries

- Treat this directory as the app’s operating repository root, even when the Xcode project is nested below it.
- Do not modify global Codex configuration, global skills, or installed plugins unless the user explicitly asks.
- Before implementation, read the active roadmap task and baton together with the relevant product and design memory.
