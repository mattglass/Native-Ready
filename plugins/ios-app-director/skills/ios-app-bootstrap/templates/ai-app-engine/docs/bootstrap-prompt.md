# Stable Bootstrap Prompt

Use this as the first message in a fresh Codex Desktop or Codex CLI task opened
at the target app repo root. The folder may be empty when the plugin is globally
installed; `ios-app-bootstrap` deploys the embedded READY starter pack first.

`ios-app-bootstrap` is the single public setup entry point. It may delegate to the other READY skills internally, but it owns completion through the first simulator launch and receipt.

The complete READY suite contains:

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

```md
Use $ios-app-bootstrap as the single READY setup entry point. Coordinate the other globally installed READY skills internally when their phase applies.

Work only inside this repo:
- /Users/Path/To/NewApp/

This repo is a READY iOS app development workspace. Deploy or repair the embedded READY starter pack when `AGENTS.md`, `docs/`, or `.stitch/` is missing. The repo root is the folder containing those paths after deployment; a local `plugins/` directory is optional and normally absent when using the globally installed plugin. Keep the app repo as the operating root even when the generated SwiftUI/Xcode project lives in a nested app container.

Bootstrap inputs:
- App name: [APP_NAME]
- App purpose: [ONE_SENTENCE_PURPOSE]
- Target users: [TARGET_USER]
- Platform: [IPHONE_ONLY or IPHONE_AND_IPAD]
- Current app maturity: prototype
- First 3–5 must-have features:
  1. [FEATURE_1]
  2. [FEATURE_2]
  3. [FEATURE_3]
  4. [FEATURE_4]
  5. [FEATURE_5]
- Visual tone: [TONE_1], [TONE_2], [TONE_3]
- Stitch project: [STITCH_PROJECT_NAME_OR_ID or NONE_YET]
- Stitch role: [PRIMARY_CONCEPT_SOURCE / SECONDARY_REFERENCE / NOT_IN_SCOPE]
- Screenshots, notes, or feature plan: [PATH_OR_LINK_OR_NONE]
- Backend needed now: [YES or NO]
- Cloudflare needed now: [YES or NO]
- Bundle identifier: [FINAL_REVERSE_DOMAIN_ID or PROVISIONAL]

Completion contract:
1. Deploy or safely repair the embedded READY starter pack from the active bootstrap skill when required; preserve differing existing files and do not copy plugin source into the app repo.
2. Preflight Codex workspace access, Xcode/Simulator, XcodeBuildMCP, Stitch, and optional service tooling.
3. Fill or repair product-specific content in `AGENTS.md`, `docs/app-build-spec.md`, `.stitch/APP.md`, `.stitch/DESIGN.md`, `.stitch/metadata.json`, `.stitch/ROADMAP.md`, and `.stitch/next-prompt.md`.
4. When Stitch is in scope and no project exists, generate first-pass concepts in one provenance-backed Stitch project.
5. Inspect required core concept roles for hierarchy, clipping, overflow, generic treatment, and product identity. Use at most two corrective edit/variant attempts per core role during bootstrap, then keep the strongest usable artifact and record remaining gaps.
6. Refresh stable Stitch intake manifests, extract source artwork when available, synthesize the feature map and semantic design system, and create the visual-spine plan and screen packets.
7. Keep an ambiguous or optional Stitch operation visible without letting it block independent native setup. The active baton must point to the best dependency-safe executable task.
8. Create or confirm the native SwiftUI Xcode project with app-specific target, module, scheme, source root, app entry type, and test-target names.
9. Do not retain `MyApp` or another unrelated app's target/test names. Treat `com.example.*` as provisional simulator-only identity and label it explicitly.
10. Use XcodeBuildMCP to discover the scheme and run the first simulator build/launch. Diagnose setup failures instead of stopping after scaffold generation.
11. Validate `.stitch/next-prompt.md` frontmatter and activate the first dependency-safe delivery task after scaffold validation.
12. Render `docs/bootstrap-receipt.md` with the Stitch project/status, native target/scheme/project/bundle ID, first build result/evidence, active task, baton validation, unresolved risks, completion state, and exact next prompt.

Operating rules:
- preserve the source path: design evidence -> feature map/design system -> roadmap/baton -> native SwiftUI
- use Stitch semantically, not as literal SwiftUI layout truth
- preserve product-critical source artwork and visual identity
- separate visible evidence from inferred requirements
- keep service contracts separate from UI placeholders
- classify unavailable optional services as non-blocking
- treat the bootstrap receipt as informational, not as a gate
- do not stop after documentation or Stitch generation alone
- stop after the runnable scaffold and receipt unless this prompt also explicitly authorizes product-feature delivery
- ask only for a missing decision or credential that prevents meaningful progress

If Stitch is unavailable and was not declared mandatory, continue from the product brief, screenshots, or notes; create and validate the native scaffold; and record the degraded design path in the receipt.

If `ios-native-scaffold` is unavailable, create the smallest valid SwiftUI Xcode project by the best available local path and validate it with XcodeBuildMCP. Do not ask me to manually create or open the project unless automated scaffold recovery is genuinely blocked.
```

After a `ready_for_delivery` receipt, use the `/goal` prompt in `SETUP.md` to start autonomous feature delivery.
