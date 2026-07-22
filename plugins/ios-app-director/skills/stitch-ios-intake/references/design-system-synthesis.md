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
- a user-accepted or visual-gate-passing native implementation supersedes an
  earlier concept

Do not rewrite it for a one-off experiment, rejected screen, or decorative
variation.

## Visual-Intent Evidence Order

1. explicit user design decisions and accepted tradeoffs
2. active Stitch project metadata and design-system fields
3. representative live Stitch screens
4. saved screenshots, exported HTML/CSS, and extracted source artwork
5. accepted screen packets and native tokens that passed the applicable visual gate
6. current native tokens as evidence of adoption or divergence
7. older prompt notes and cautious proposals

Verified native behavior remains authoritative for current-state and runtime
claims. This ordering applies to intended visual identity; it prevents an early
generic scaffold from silently redefining a design-first product.

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

## Native Reconciliation

Once SwiftUI implementation exists, reconcile the document with live tokens and
components, but classify the result as adoption, intentional divergence, or a
remaining gap. The implementation becomes visual authority only after the user
accepts the divergence or the relevant screen passes its visual gate. Record
unaccepted differences as roadmap or visual-spine work; never promote scaffold
defaults merely because they were implemented first.
