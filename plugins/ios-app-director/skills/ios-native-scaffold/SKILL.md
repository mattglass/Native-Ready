---
name: ios-native-scaffold
description: Create or repair the initial native SwiftUI Xcode project for a design-first iOS app repo, derive app-safe target/module names, replace MyApp placeholders, update repo memory with native project paths, and prepare XcodeBuildMCP build validation before ios-app-director starts implementation.
allowed-tools:
  - "Read"
  - "Write"
  - "XcodeBuildMCP:*"
---

# iOS Native Scaffold

Use this skill after design-first repo memory is coherent and before feature implementation begins.

It turns the old manual Xcode project step into an automated bridge:

1. derive a stable native naming contract
2. create a minimal SwiftUI Xcode project
3. update repo-local memory so destinations point at the real source tree
4. verify no active `MyApp` placeholders remain in operating files
5. hand the repo to `ios-app-director` for the first build/run loop

## Read First

Read only what is needed:

- `references/naming-contract.md` before choosing target/module names
- `references/scaffold-checklist.md` before creating or repairing the project
- repo memory: `AGENTS.md`, `.stitch/metadata.json`, `.stitch/ROADMAP.md`, `.stitch/next-prompt.md`, `.stitch/APP.md`, `.stitch/DESIGN.md`, `docs/app-build-spec.md`

## Guardrails

- Run only after app memory, design memory, feature map, roadmap, metadata, and baton are coherent.
- Do not install the bundled plugin globally during scaffold work.
- Do not edit unrelated app repos.
- Do not keep `MyApp` as the native target unless the user explicitly chooses that name.
- Prefer a generated target/module name from the app name when the user has not chosen one.
- Keep the initial shell small: app entry, onboarding gate, tab shell, design tokens, persistence folder, and feature folders.
- Do not implement product-specific features in this skill. `ios-app-director` handles delivery after the scaffold builds.

## Workflow

### 1. Choose Names

Use the naming contract to derive:

- display name
- target/module/scheme name
- app entry type
- bundle identifier
- planned test-target name derived as `{TargetName}Tests`
- native project container
- source root

Example:

- display name: `H2O Habit Tracker`
- target/module/scheme: `H2OHabitTracker`
- app entry type: `H2OHabitTrackerApp`
- project: `H2OHabitTrackerApp/H2OHabitTracker.xcodeproj`
- source root: `H2OHabitTrackerApp/H2OHabitTracker/`
- planned test target: `H2OHabitTrackerTests`

### 2. Render The Project

Use the bundled script from the skill directory:

```sh
python3 scripts/render_ios_native_scaffold.py \
  --repo-root /path/to/app/repo \
  --app-name "App Name" \
  --target-name AppName \
  --bundle-id com.example.appname \
  --platform iphone-and-ipad
```

Omit `--target-name` and `--bundle-id` when they can be safely derived.

### 3. Inspect The Result

Confirm:

- `.xcodeproj/project.pbxproj` exists
- app entry Swift file exists
- `ContentView.swift` exists
- feature folders exist
- `.stitch/metadata.json` records `nativeProjectStatus: created`
- metadata and `AGENTS.md` record the app-derived test-target name for later test creation
- active repo memory no longer points at `MyApp/...`

Use this as the final active-placeholder check:

```sh
rg "MyApp/|nativeTarget.*MyApp|Main app target:.*MyApp|Build target:.*MyApp|App target:.*MyApp" AGENTS.md docs .stitch
```

Explanatory prompt text that says not to use `MyApp` is acceptable. Active target names and destination paths are not.

### 4. Prepare Validation

Before build/run/test work, follow XcodeBuildMCP session rules:

1. call `session_show_defaults`
2. set defaults when needed with project path, scheme, simulator, and bundle id
3. use `build_run_sim` for the first launch validation

### 5. Hand Off

End with:

- native project path
- scheme/target
- planned test target
- bundle id
- first build/run result
- any remaining setup risk
- active roadmap/baton destination for `ios-app-director`
