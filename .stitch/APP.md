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
Do not force current capability and intended visual direction into one ranking.

For product scope, constraints, and current behavior, prefer:

1. **Explicit user decisions and `AGENTS.md`**
2. **Verified runtime behavior and native implementation**
3. **`docs/app-build-spec.md`**
4. **`.stitch/ROADMAP.md` and `.stitch/next-prompt.md`**

For intended visual identity on a design-first surface, prefer:

1. **Explicit user design decisions**
2. **`.stitch/DESIGN.md`, approved screen packets, and their source artwork**
3. **The active Stitch design system and tracked reference screens**
4. **Native tokens and surfaces only after user acceptance or a passed visual gate**

An ungated native pass records adoption or divergence. It does not silently
replace the intended visual direction.

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
- Treat Stitch as a concept and layout-exploration system and, when approved,
  evidence of the intended visual identity
- Do not let concept output overrule verified native behavior, product
  constraints, or service reality
- Do not let an ungated native approximation overrule approved Stitch visual
  language, screen packets, or source artwork
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
