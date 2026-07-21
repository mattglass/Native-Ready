# Design Intake Policy

## Purpose
Use Stitch and other concept sources to improve native product quality without copying generic layouts literally.

## Design intake rules
1. Treat concept work as directional, not authoritative.
2. Extract semantic value first: hierarchy, trust signals, navigation clarity, information density, tone.
3. Prefer SwiftUI-feeling structure over exact visual mimicry.
4. Prefer app-specific product logic over decorative novelty.
5. Preserve the concept's distinctive visual identity when it is central to the product experience.

Do not let "semantic translation" become generic UI. If Stitch produced the
app's magic through artwork, image-forward cards, composition, playful motifs,
custom backgrounds, or a highly specific mood, capture those as implementation
requirements. Decide explicitly whether each visual element will be translated
with source artwork extracted from Stitch HTML, native drawing, bundled bitmap
assets, generated assets, cropped/reference assets, or a deferred visual task.
When the saved Stitch HTML already provides usable product-critical images,
prefer extracting them into `.stitch/intake/assets/` and referencing
`.stitch/intake/image-asset-manifest.*` before generating substitutes.

## Stable Stitch artifact discovery
When Stitch evidence changes, inventory `.stitch/intake/` through a stable manifest before feature-map or roadmap work.

When new screenshot or HTML URLs need to be saved, use:

```bash
python3 plugins/ios-app-director/skills/stitch-ios-intake/scripts/save_stitch_screen_artifacts.py --repo-root . --from-queue
```

Store the changing URLs in `.stitch/intake/pending-stitch-artifacts.json` before running the command. Use the direct `--slug --screenshot-url --html-url` form only when queueing is unnecessary.

Preferred local-plugin command:

```bash
python3 plugins/ios-app-director/skills/stitch-ios-intake/scripts/build_intake_manifest.py --repo-root .
```

When saved HTML contains product-critical `<img>` artwork, also run:

```bash
python3 plugins/ios-app-director/skills/stitch-ios-intake/scripts/extract_stitch_image_assets.py --repo-root .
```

Use `.stitch/intake/image-asset-manifest.*` as the stable source-artwork index.
Generated artwork is a fallback or product decision, not proof that available
Stitch source artwork has been adopted.

If that path is unavailable, use the bundled `stitch-ios-intake` script from the active skill directory, or fall back to `rg --files .stitch/intake | sort`.

Avoid commands that enumerate exact new asset paths such as `mkdir -p ... && curl ... && file .stitch/intake/screenshots/11-new-screen.png ...`. New screenshot and HTML filenames are expected to change; the save script and manifest are the reusable discovery surfaces.

## What to extract from a concept
- primary hierarchy
- strongest trust signal
- navigation pattern
- content grouping logic
- action placement
- tone and pacing
- signature artwork, hero imagery, icon language, decorative motif, and image/card treatment
- color balance, background treatment, depth, glow, motion, and empty-space rhythm
- which visuals are product-critical versus merely decorative

## What to avoid copying blindly
- ornamental sections without product value
- web-style density that harms native readability
- impossible or awkward native patterns
- visual decisions that weaken professional trust
- screenshot-as-UI shortcuts that make native text, accessibility, localization, or layout brittle

## Adoption outcomes
When concept work materially informs implementation, record one of:
- adopted
- partially adopted
- deferred
- rejected

## Good native translation behavior
A strong translation usually:
- simplifies hierarchy
- tightens calls to action
- improves trust and clarity
- reduces generic marketing tone
- respects the app's existing design system
- preserves the app-specific visual signature at the fidelity level the task
  requires: `same_product_family` for early progress, `prototype_visual_gate`
  before maturity promotion, or `exact_reference` when the user asks to match a
  named Stitch screen

## Visual fidelity check

For design-first apps, every design-translation task should compare at least
one Stitch reference screenshot with a simulator screenshot before closeout.
Record whether the visual identity is:

- `strongly_adopted`: native screen clearly carries the concept's artwork,
  composition, color energy, and component personality.
- `prototype_visual_gate_passed`: core native screen is close enough to support
  prototype exit for the current product maturity goal.
- `same_family_only`: related to Stitch, but not enough for prototype exit when
  source artwork or image-forward composition defines the product.
- `partially_adopted`: layout and tone are present, but signature artwork or
  image treatment is missing.
- `generic_substitute`: native implementation uses symbols, gradients, or
  generated substitute art where Stitch provided usable product-critical source
  artwork.
- `parity_unproven`: close or exact adoption is claimed, but simulator evidence
  does not prove it requirement-by-requirement.
- `deferred`: a named visual follow-up task exists and is sequenced before
  beta/release-readiness claims.
- `rejected`: the concept visual was intentionally not used, with a reason.

If a core screen is only `partially_adopted`, do not treat the design work as
fully done unless a visual-fidelity follow-up task is ready or in progress.
