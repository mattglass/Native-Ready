# Native Naming Contract

The native scaffold must make product identity explicit before Swift implementation starts.

## Name Types

- Display name: user-facing product name, spaces allowed.
- Target name: Xcode target, scheme, and Swift module name. Use PascalCase letters and numbers only.
- Test target: target name plus `Tests`. Never inherit a test-target name from another repository or global instruction file.
- App entry type: target name plus `App`.
- Bundle id: reverse-DNS lowercase identifier.
- Project container: target name plus `App`.
- Source root: project container plus target name.

## Derivation Rules

When the user does not provide a target name:

1. Split the display name into alphanumeric tokens.
2. PascalCase each token.
3. Remove punctuation and spaces.
4. Prefix with `App` if the result starts with a number.
5. Avoid keeping generic names such as `MyApp`, `App`, `TestApp`, or `UntitledApp`.

Examples:

- `H2O Habit Tracker` -> `H2OHabitTracker`
- `Focus Ledger` -> `FocusLedger`
- `Trail Notes` -> `TrailNotes`

Derived test target examples:

- `H2OHabitTracker` -> `H2OHabitTrackerTests`
- `TrailNotes` -> `TrailNotesTests`

When the user does not provide a bundle id:

1. Use `com.example.` as the safe default prefix for scaffold experiments.
2. Lowercase the target name.
3. Remove characters that are not letters or numbers.

Example:

- `TrailNotes` -> `com.example.trailnotes`

## Memory Paths

Use paths relative to the repo root:

- project path: `{TargetName}App/{TargetName}.xcodeproj`
- source root: `{TargetName}App/{TargetName}/`
- app shell: `{TargetName}App/{TargetName}/Features/AppShell/`
- onboarding: `{TargetName}App/{TargetName}/Features/Onboarding/`
- design system: `{TargetName}App/{TargetName}/Shared/DesignSystem/`
- persistence: `{TargetName}App/{TargetName}/Shared/Persistence/`

Replace active `MyApp/` destination paths in repo memory with the real source root before `ios-app-director` begins delivery.
