# Visual Spine Rubric

## Purpose

Protect the creative value of design-first workflows. Stitch should not only
seed features; it should seed the app's recognizable visual identity.

## Screen Comparison Checklist

For each Stitch/native screen pair, compare:

- **Hero media:** Does native have the same level of product-specific artwork,
  illustration, photo treatment, or object focus?
- **Composition:** Does native preserve the concept's major spatial move, such
  as hero-first, image-forward cards, staged flow, or celebration reveal?
- **Color energy:** Does native carry the same dominant palette, contrast, glow,
  and accent balance?
- **Component personality:** Do cards, buttons, chips, tabs, badges, and forms
  feel custom to the app rather than generic system defaults?
- **Motifs:** Are domain motifs present, such as stars, frosting, rockets,
  health charts, maps, instruments, inventory objects, or venue cues?
- **Trust and readability:** Did visual richness preserve clarity,
  accessibility, and safety/privacy messaging?
- **Native fit:** Does the translation feel like a polished SwiftUI app rather
  than a web screenshot or a bare scaffold?

## Product-Aware Taste Gate

Visual quality is contextual. Calibrate density, asymmetry, illustration,
motion, decoration, and restraint to the product, target age, trust level, and
usage environment. Do not impose one universal premium formula such as a single
accent, a specific font, no emoji, mandatory asymmetry, or minimal motion.

Reject or repair:

- fabricated metrics, testimonials, social proof, compliance claims, or live
  service behavior
- generic AI copy, startup filler, empty dashboard tiles, and arbitrary visual
  clichés that do not serve the product
- decorative density that obscures hierarchy or weakens accessibility
- motion without a functional or emotional purpose
- incomplete loading, empty, error, success, disabled, selected, or completion
  states where the product flow requires them
- artwork or component treatments that ignore the audience, domain, or existing
  design evidence

Require readable contrast, touch targets, Dynamic Type resilience, and a
reduced-motion path. Expressiveness is welcome when it strengthens identity and
the product remains understandable and trustworthy.

## Fidelity Levels

### Strongly adopted
- Core artwork or visual treatment is present.
- Composition and color energy are recognizably related to Stitch.
- Native components feel app-specific.
- Screenshot comparison supports the stated parity target for the task.

### Prototype visual gate passed
- Core source artwork, image treatment, or an explicitly accepted native
  equivalent is present.
- First-viewport composition, primary actions, color energy, motifs, and
  component personality are close enough that a user can judge the intended
  product experience.
- Simulator evidence is compared against the Stitch reference.
- Remaining gaps are documented as non-blocking, or have a ready follow-up
  before any dogfood/user-testing/beta promotion.

### Same family only
- The native screen is recognizably inspired by Stitch, but it simplifies
  artwork, composition, content density, or personality enough that users would
  not experience the full concept yet.
- This is useful progress for early implementation.
- This is not enough to leave prototype for core screens when Stitch contains
  strong source artwork or the user asked for close matching.

### Partially adopted
- Layout, copy, and core features are present.
- Some colors/tokens match.
- Product-critical artwork, media, motif, or composition is missing or weak.
- Needs a visual-spine follow-up before beta/release claims.

### Generic substitute
- Native screen mostly uses SF Symbols, default cards, simple gradients, or
  plain lists where Stitch provided custom artwork and richer composition.
- This is acceptable only for the initial scaffold or a named temporary state.

### Missing
- Stitch screen has no native equivalent.

### Intentionally deferred
- Gap is known.
- Roadmap has a ready or scheduled task.
- User/product reason explains deferral.

### Parity unproven
- The agent claims close or exact adoption, but evidence does not compare the
  native screen requirement-by-requirement against the Stitch reference.
- Keep the task active or create a follow-up until proof or an explicit product
  decision exists.

## Roadmap Acceptance Criteria

A visual-spine task should include:

- reference Stitch screenshots
- extracted Stitch image assets when HTML provides product-critical artwork
- current simulator screenshots if native exists
- SwiftUI destination files
- product-critical visual signatures to preserve
- asset strategy
- screenshot comparison evidence requirement
- acceptance language for the correct visual target
- `visual_parity_target`: `same_product_family`, `prototype_visual_gate`, or
  `exact_reference`
- explicit reason when generated substitutes are used instead of available
  source artwork

## Common Fixes

- Replace plain SF Symbol heroes with extracted Stitch source artwork, native
  drawn hero marks, generated bitmap assets, or bundled artwork.
- Prefer saved Stitch artwork over regenerated approximations when source art is
  available and appropriate for the prototype.
- When source artwork is missing or too narrow, prompt Stitch for more screens,
  states, or variants in the same project before settling for weaker native
  substitutes.
- Make content cards image-forward when Stitch cards are image-forward.
- Add reusable background/motif primitives instead of one-off gradients.
- Add product-specific tab, badge, and empty-state treatments.
- Preserve staged visual storytelling in AI/capture/result flows.
- Schedule visual fidelity before release hardening when core screens look
  generic.
