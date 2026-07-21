# Semantic Design-System Synthesis

Use this contract to create or refresh `.stitch/DESIGN.md`. The file is the
READY workflow's compact design memory: specific enough to guide Stitch and
SwiftUI, but adaptable as the product becomes real.

## When To Refresh

Refresh when:

- the template still contains unresolved placeholders
- a live Stitch project establishes the first coherent visual system
- multiple adopted screens consistently change a token or component rule
- the user makes a product-level design decision
- live native implementation becomes more authoritative than earlier concepts

Do not rewrite it for a one-off experiment, rejected screen, or decorative
variation.

## Evidence Order

1. live native design tokens and shipped behavior
2. explicit user decisions
3. active Stitch project metadata and design-system fields
4. representative live Stitch screens
5. saved screenshots and exported HTML/CSS
6. intake and image-asset manifests
7. older prompt notes and cautious proposals

Label uncertain or newly inferred rules as proposed. Never invent exact hex,
font, spacing, metric, or accessibility claims merely to fill a section.

## Preserve The Eight-Section Contract

Keep these sections and fill them with evidence-backed guidance:

1. **Visual Theme & Atmosphere** — product personality, emotional qualities,
   audience fit, content voice, and what the app must not feel like.
2. **Color Palette & Roles** — exact values when known, semantic roles, surface
   hierarchy, text contrast, light/dark behavior, and state colors.
3. **Typography Rules** — families when known, semantic hierarchy, dynamic type,
   weight/scale relationships, and voice.
4. **Component Stylings** — geometry, shape, depth, borders, materials, artwork,
   buttons, cards, inputs, modules, and interactive states.
5. **Layout Principles** — hierarchy, spacing rhythm, density, safe areas,
   iPhone/iPad adaptation, navigation, motion purpose, and reduced-motion rules.
6. **Stitch Use Policy** — the stable prompt fragment for platform, theme,
   palette, interaction, layout, artwork, and consistency with the active system.
7. **Suggested Concept Directions** — a small set of purposeful, testable future
   explorations rather than a backlog of random styles.
8. **Banned Patterns** — product-specific anti-patterns, fake data/claims,
   inaccessible motion or contrast, generic filler, and web-layout leakage.

At the top, record the evidence sources and confidence. Keep provenance brief;
link to the intake record instead of copying its full inventory.

## Product-Aware Rules

- Calibrate expressiveness, density, symmetry, illustration, and motion to the
  target user and context. There is no universal premium style.
- Preserve meaningful personality without weakening readability, trust, or
  native interaction.
- Describe states for reusable components: default, pressed, focused, selected,
  disabled, loading, empty, error, success, and completion where applicable.
- Use purposeful motion and celebration; provide reduced-motion behavior.
- Ban fabricated metrics, social proof, compliance claims, and services.
- Avoid generic AI copy, empty dashboard tiles, and arbitrary visual clichés.

## Native Source Of Truth

Once SwiftUI implementation exists, reconcile the document with live tokens and
components. Concepts may propose changes, but they do not silently override the
native system. Record intentional divergences as roadmap or visual-spine work.
