# Native Implementation Guardrails

## Purpose

Keep autonomous iOS delivery fast without letting speed create brittle product
state, malformed memory, or generic UI drift.

## Large Early Slices

Large early slices are good when they create a coherent product surface. A
prototype task may implement onboarding plus app shell, discovery plus detail,
or capture plus result when those surfaces must be judged together.

After the app has multiple implemented feature areas, prefer narrower edits
unless the roadmap explicitly calls for a coherent cross-screen refactor. Do not
rewrite large Swift files only to make small visual or data changes.

## Stable Content Identity

Do not connect recipes, lessons, items, badges, or sample content by array
indexes once multiple screens reference them. Use stable IDs and named fixtures
instead.

Good:
- `CupcakeIdea.galaxyUnicorn`
- `CupcakeRecipe.galaxyUnicorn`
- `RecipeCatalog.recipe(for: idea.id)`

Risky:
- `RecipeCatalog.samples[2]`
- adding a new sample at the front of a shared array
- copying detail data from whichever card happens to be first

When a task adds a new content variant, regression-check every screen that uses
the shared fixture family.

## SwiftUI Code Hygiene

- Avoid `Text("A") + Text("B")` for styled inline labels on iOS 26. Use
  interpolation, `HStack`, or a dedicated styled label component.
- Avoid unsupported SF Symbols. When uncertain, use a symbol already present in
  the project or verify it in the app before closing.
- Keep fixed CTAs, custom tab bars, and safe-area overlays from covering safety,
  privacy, form, or primary action content.
- If a screen hides native tab bars to mimic Stitch, regression-check navigation
  in and out of that screen.
- After adding bundled assets, verify asset names at runtime through the screen
  that uses them, not only by checking the asset catalog files.

## Repo Memory Writes

- Keep durable repository operating guidance in `AGENTS.md`; do not add
  model-level instruction overrides during setup.
- When writing `.stitch/next-prompt.md`, keep frontmatter keys unindented and
  validate with `ios-app-director/scripts/validate_baton_frontmatter.py`.
- Prefer structured scripts or targeted patches for memory updates that include
  backticks, URLs, colons, or multiline frontmatter.

## Simulator Automation

- Runtime UI element refs expire. After build/run, navigation, or any failed tap,
  call `snapshot_ui` again before reusing element refs.
- Capture evidence for the actual screen state being claimed. A build success
  plus a home snapshot does not prove a detail, modal, persistence, or parity
  claim.
- When exact or prototype-gate visual parity is the task, capture at least the
  first viewport and the main scrolled content sections.
