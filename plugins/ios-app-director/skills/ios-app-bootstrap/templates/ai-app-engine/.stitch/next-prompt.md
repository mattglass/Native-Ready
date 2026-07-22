---
platform: "[PRIMARY_PLATFORM]"
roadmap_task: APP-001
task_type: native_scaffold
feature: app-shell-and-native-project
screen: App shell
destination: "[NATIVE_SOURCE_ROOT] native project scaffold and feature folders"
mode: native
device: universal
validation_tier: tier1_compile
app_maturity: prototype
design_input: .stitch/DESIGN.md
service_maturity: level0_placeholder
depends_on: repo-local operating memory coherent
unlocked_by: READY setup memory complete enough to create native project files
regression_scope: none
evidence_expectation: light
architecture_review: note_only
risk_level: medium
phase: prototype
---

Create the first native SwiftUI app shell for `[APP_NAME]`.

**SOURCE OF TRUTH (REQUIRED):**
- Follow `AGENTS.md`
- Follow `docs/app-build-spec.md`
- Follow `.stitch/APP.md` and `.stitch/DESIGN.md`
- Treat Stitch as semantic design evidence, not literal layout export

**TASK:**
Create or confirm the native iOS project scaffold, derive the real target/module/scheme name from `[APP_NAME]`, replace active placeholder native paths, and build/run the first app shell.

**GOALS:**
1. Create the native SwiftUI Xcode project.
2. Establish the app entry type, app shell, and initial feature folders.
3. Update `.stitch/metadata.json`, `.stitch/APP.md`, `.stitch/ROADMAP.md`, and this baton with real native paths.
4. Validate the generated project with XcodeBuildMCP.

**VALIDATION REQUIREMENTS:**
- Reach `tier1_compile`.
- Confirm the generated scheme with XcodeBuildMCP.
- Build and launch on an iOS Simulator.
- Capture build/run evidence when practical.

**DO NOT:**
- implement product feature code before scaffold validation
- add backend or Cloudflare services
- copy Stitch HTML directly into SwiftUI
- keep `MyApp` as the target unless explicitly chosen
