# Stitch Art Expansion Loop

## Purpose

Use Stitch again when the native app needs more product-specific artwork,
screen states, content variants, or visual detail than the current intake
provides. A design-first product builder should not default to weaker generated
or hand-drawn substitutes when Stitch can produce richer concept art in the same
visual world.

## When To Trigger

Trigger this loop when:
- a core screen is blocked by missing hero, card, badge, reward, character, or
  object artwork
- existing Stitch screens define the mood, but do not cover the state now being
  implemented
- native generated artwork looks less polished than the original Stitch assets
- a recipe, lesson, item, badge, profile, empty state, or result needs several
  visually coherent variants
- exact or prototype-gate parity is blocked by insufficient reference material

Do not create a new Stitch project when an existing project already represents
the app's visual world unless the user explicitly wants a fork. Prefer adding
screens, variants, or states to the existing project.

## Expansion Prompt Pattern

Ask Stitch for an iPhone concept screen or screen state, not only a loose asset
request. The artwork should appear in product context so the native agent can
learn both the image and how it is used.

Include:
- existing app/project name and visual world
- source screen(s) to stay consistent with
- exact screen/state being expanded
- needed artwork types, such as hero image, content card art, badge art,
  mascot/character, empty state, result state, or ingredient/object art
- target user and product purpose
- design-system cues already present in `.stitch/DESIGN.md`
- layout role and primary actions
- safety/privacy/trust copy when relevant
- request for production-quality iOS concept design with visible labels and
  extractable image-forward elements

## Intake After Expansion

After Stitch creates or updates screens:
1. capture screen titles, IDs, screenshot URLs, and HTML URLs
2. save artifacts through `.stitch/intake/pending-stitch-artifacts.json` and
   `save_stitch_screen_artifacts.py --from-queue`
3. run `extract_stitch_image_assets.py --repo-root .`
4. rebuild `.stitch/intake/intake-manifest.*`
5. update `.stitch/intake/design-intake.md`
6. update `.stitch/APP.md` section 9 and `.stitch/DESIGN.md` when scope or
   visual language changes
7. update affected `.stitch/screen-packets/` with new source assets and
   fidelity targets
8. update `.stitch/ROADMAP.md`, `.stitch/metadata.json`, and
   `.stitch/next-prompt.md`

## Native Adoption Rule

Use newly extracted Stitch artwork when it is usable and product-critical.
Generated bitmap assets, native drawings, or SF Symbols are fallback strategies,
not automatic parity proof.

If native cannot match the Stitch concept tightly, record the reason using one
of these targets:
- `same_product_family`: acceptable early progress
- `prototype_visual_gate`: required before prototype promotion
- `exact_reference`: required when the user asks to match a named screen closely

When exact or prototype-gate parity remains blocked, keep the task active or add
a visual-spine follow-up instead of promoting maturity.
