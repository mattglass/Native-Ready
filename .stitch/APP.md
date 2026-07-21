# [APP_NAME] — Stitch Workspace

> **Purpose:** This folder is the local product and concept memory for `[APP_NAME]`.

## 1. Product Identity
- **App:** `[APP_NAME]`
- **Platform:** `[PRIMARY_PLATFORM]`
- **Audience:** `[TARGET_USER]`
- **Repo:** `[REPO_NAME]`
- **Primary native target:** `[MAIN_TARGET_NAME]`
- **Current phase:** `[prototype / dogfood / beta / release_candidate / production]`

## 2. Product Goals
The app exists to:

1. `[GOAL_1]`
2. `[GOAL_2]`
3. `[GOAL_3]`
4. `[GOAL_4]`
5. `[GOAL_5]`

## 3. Source-of-Truth Hierarchy
When docs, concept work, and implementation disagree, prefer this order:

1. **Live native implementation**
2. **`AGENTS.md`**
3. **`docs/app-build-spec.md`**
4. **`.stitch/DESIGN.md`**
5. **`.stitch/ROADMAP.md` and `.stitch/next-prompt.md`**
6. **Concept references and future Stitch work**

## 4. Core Feature Areas

### Feature Area 1
- `[FEATURE_AREA_1_ITEM_1]`
- `[FEATURE_AREA_1_ITEM_2]`
- `[FEATURE_AREA_1_ITEM_3]`

### Feature Area 2
- `[FEATURE_AREA_2_ITEM_1]`
- `[FEATURE_AREA_2_ITEM_2]`
- `[FEATURE_AREA_2_ITEM_3]`

### Feature Area 3
- `[FEATURE_AREA_3_ITEM_1]`
- `[FEATURE_AREA_3_ITEM_2]`
- `[FEATURE_AREA_3_ITEM_3]`

### Feature Area 4
- `[FEATURE_AREA_4_ITEM_1]`
- `[FEATURE_AREA_4_ITEM_2]`
- `[FEATURE_AREA_4_ITEM_3]`

## 5. Native Destination Map
Use these as the primary implementation destinations:

- Native project: `[NATIVE_PROJECT_PATH]`
- App entry: `[NATIVE_SOURCE_ROOT][APP_ENTRY_TYPE].swift`
- App shell: `[NATIVE_SOURCE_ROOT]Features/AppShell/`
- First feature: `[NATIVE_SOURCE_ROOT]Features/[FIRST_FEATURE_FOLDER]/`
- Services: `[NATIVE_SOURCE_ROOT]Shared/Services/`
- Persistence: `[NATIVE_SOURCE_ROOT]Shared/Persistence/`
- Design system: `[NATIVE_SOURCE_ROOT]Shared/DesignSystem/`

## 6. Concept / Stitch Policy
- Treat Stitch as a concept and layout-exploration system by default
- Do not let concept output overrule native UX, product constraints, or service reality
- Favor concepts that feel implementable in SwiftUI and credible for the target user
- Prefer workflow clarity over decorative novelty

## 7. Preferred First Concepts
- `[PREFERRED_CONCEPT_1]`
- `[PREFERRED_CONCEPT_2]`
- `[PREFERRED_CONCEPT_3]`
- `[PREFERRED_CONCEPT_4]`

## 8. Working Rules
1. Keep the roadmap concrete enough for implementation, not just ideation.
2. Every serious concept should name its likely native destination.
3. Prioritize trust, clarity, and repeat-use value.
4. Keep the product tone aligned with the intended audience.
5. Use `.stitch/ROADMAP.md` as the queue and `.stitch/next-prompt.md` as the active baton.

## 9. App Feature Inventory & Requirements Map

Generate this section from Stitch/screenshots/notes with `ios-feature-map`.

Keep visible screen evidence separate from inferred requirements, future scope, service implications, and privacy/risk notes.
