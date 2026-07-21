# iOS Stitch Prompt Contract

Use this contract for every Stitch screen generation, variant, or focused edit.
It keeps prompt quality inside the READY workflow and makes the output useful to
both product planning and native SwiftUI implementation.

## Evidence Order

Build the prompt from the strongest available evidence:

1. explicit user decisions
2. live native behavior and design tokens
3. the active Stitch project's design system and reference screens
4. filled guidance in `.stitch/DESIGN.md` and `.stitch/APP.md`
5. intake artifacts and the current roadmap task
6. cautious proposals for details that are still undecided

Do not present an inferred token, feature, metric, or service as established
product truth.

## Generation Prompt

A complete prompt should state:

- **Platform:** native iOS, device class, and iPhone/iPad expectations
- **User and purpose:** who this screen serves and the outcome it supports
- **Screen role:** where it sits in the flow and how the user reaches or leaves it
- **Actions:** primary and secondary actions, selection behavior, and navigation
- **Content:** realistic labels/data plus relevant empty, loading, error, success,
  disabled, selected, or completion states
- **Hierarchy:** first-viewport priority, section order, density, and scrolling
- **Atmosphere:** product-specific emotional tone, voice, and trust level
- **Visual system:** semantic color roles, typography hierarchy, shapes, depth,
  components, artwork, and motifs appropriate to this product
- **Guardrails:** accessibility, sensitive-domain constraints, and unsupported
  claims or integrations to avoid
- **Output intent:** a production-quality native iOS concept with analyzable
  labels, state, and artwork rather than a web page dressed as an app

Use concrete visual language. Describe relationships and roles, not a pile of
decorative adjectives.

## Design-System Modes

### Active Stitch design system exists

Keep its established tokens and visual grammar. Do not inject a second palette,
type scale, or component language. Use `.stitch/DESIGN.md` to clarify semantic
intent, screen composition, content, artwork, and product-specific atmosphere.

### No active Stitch design system

If `.stitch/DESIGN.md` is filled and evidence-backed, include its semantic color
roles, type hierarchy, geometry, depth, component behavior, artwork, and motion
direction. If it still contains placeholders, propose only the smallest coherent
system needed for this concept and mark the proposal for later intake review.

## Native iOS Guardrails

- Prefer `NavigationStack`, sheets, tabs, lists, controls, and gestures that map
  naturally to SwiftUI.
- Avoid website headers, marketing-page heroes, footer navigation, hover-only
  behavior, and desktop dashboard grids.
- Keep touch targets, readable contrast, Dynamic Type, reduced-motion behavior,
  and safe areas in mind.
- Use product-appropriate density. A playful kids app, a clinical tool, and a
  professional utility should not be pushed toward one universal aesthetic.

## Focused Edits

Prefer editing an existing screen when its role and structure are sound. An edit
prompt must name:

- the exact screen and element to change
- the observed problem and desired result
- the interactions, content, tokens, and surrounding composition to preserve
- any state or accessibility consequence that must also be updated

Generate a replacement only when the screen role or underlying structure is
fundamentally wrong or missing.

## Variants

Use variants for a real product decision, not random decoration. Name the axis
being explored, such as density, artwork emphasis, age band, or navigation
model, and state what must remain invariant. Keep the set small enough to compare
meaningfully.

## Response Capture

After a Stitch call, inspect the returned screen IDs, descriptions, and suggested
follow-ups. Record useful suggestions and the reason a variant or edit was
accepted, rejected, or deferred in the operation journal, intake record, or
roadmap notes. Tool commentary is evidence, not an automatic instruction.
