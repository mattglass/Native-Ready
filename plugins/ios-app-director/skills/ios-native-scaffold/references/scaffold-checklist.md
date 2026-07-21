# Native Scaffold Checklist

## Before Scaffold

- App name is known.
- Platform is known: iPhone or iPhone and iPad.
- `.stitch/APP.md` section 9 is usable.
- `.stitch/DESIGN.md` is app-specific.
- `.stitch/ROADMAP.md` has an APP-001 scaffold/build task or equivalent.
- `.stitch/next-prompt.md` points at the first native task.
- `.stitch/metadata.json` records app, Stitch, roadmap, and maturity state.

## Scaffold Output

Required files:

- `{TargetName}App/{TargetName}.xcodeproj/project.pbxproj`
- `{TargetName}App/{TargetName}.xcodeproj/project.xcworkspace/contents.xcworkspacedata`
- `{TargetName}App/{TargetName}/{TargetName}App.swift`
- `{TargetName}App/{TargetName}/ContentView.swift`
- `{TargetName}App/{TargetName}/Features/AppShell/RootTabView.swift`
- `{TargetName}App/{TargetName}/Features/Onboarding/OnboardingView.swift`
- `{TargetName}App/{TargetName}/Shared/DesignSystem/DesignTokens.swift`
- `{TargetName}App/{TargetName}/Assets.xcassets/Contents.json`

Required memory updates:

- `AGENTS.md` names the real main app target.
- `.stitch/metadata.json` records project path, source root, bundle id, target, and app entry type.
- `.stitch/APP.md`, `.stitch/ROADMAP.md`, and `.stitch/next-prompt.md` use real native paths.
- `docs/native-scaffold.md` records the generated scaffold.

## Validation

- `rg "MyApp/|nativeTarget.*MyApp|Main app target:.*MyApp|Build target:.*MyApp|App target:.*MyApp" AGENTS.md docs .stitch` returns no active native target or path references.
- XcodeBuildMCP can list the generated scheme.
- First build/run reaches at least tier1 compile and launch.
