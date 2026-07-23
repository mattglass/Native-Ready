---
name: ios-visual-spine
description: Audit and improve design-first iOS visual fidelity by comparing Stitch screenshots with native simulator screenshots, extracting product-critical artwork/mood/component treatments, creating a visual asset strategy, and inserting or implementing visual-spine roadmap tasks before prototype promotion, beta, or release-readiness work.
---

# iOS Visual Spine

Use this skill when a design-first iOS app has Stitch screenshots, visual
concepts, or generated design evidence and the native app needs to feel like the
same product family, pass a prototype visual gate, or match a named reference
screen closely.

This skill exists to prevent a common failure mode: extracting features from
Stitch while losing the artwork, mood, image treatment, and custom visual
identity that made the concept worth using.

## Read First

Read:
- `references/visual-spine-rubric.md`
- `references/visual-parity-audit-template.md`
- `references/stitch-art-expansion-loop.md`
- `references/screen-implementation-packet-template.md`
- `.stitch/intake/design-intake.md`
- `.stitch/intake/intake-manifest.md` or `.stitch/intake/intake-manifest.json`
- `.stitch/intake/image-asset-manifest.md` or `.stitch/intake/image-asset-manifest.json`
- `.stitch/DESIGN.md`
- `.stitch/APP.md`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`

If native implementation exists, also inspect:
- simulator evidence under `.stitch/evidence/`
- primary SwiftUI screens
- shared design system files
- asset catalogs

## Design Authority Boundary

For a design-first app, verified native behavior is authoritative for what the
app currently does, but it is not automatic authority for what the app should
look like. Until the user explicitly accepts, rejects, or supersedes a visual
direction, the active Stitch references, extracted source artwork,
`.stitch/DESIGN.md`, and screen packets define intended visual identity. Treat
the live SwiftUI implementation as adoption evidence to compare against that
intent. Never let an early scaffold promote its generic tokens, default
`TabView`, plain cards, or SF Symbols into the design source of truth merely
because they exist first.

## Workflow

### 1. Pair References With Native Screens

Create a comparison set:
- Stitch screenshot for each core screen
- current simulator screenshot for the matching native surface
- SwiftUI files and design tokens that control that surface

Core screens usually include onboarding, app shell, discovery/home, primary
detail, creation/capture flow, history/log, achievement/reward, settings, and
any domain-defining interaction.

### 2. Extract The Visual Spine

For each core screen, identify:
- hero artwork or image-forward treatment
- background mood, gradients, texture, depth, and glow
- card shapes, proportions, borders, overlays, and image placement
- icon language and whether SF Symbols are sufficient
- product-specific motifs and decorative details
- motion/celebration moments
- typography scale and emotional voice
- what must survive native translation for the screen to feel like the same app

Apply the product-aware taste gate in `references/visual-spine-rubric.md` while
extracting these signatures. Judge richness, density, motion, and personality
against the app's audience and purpose rather than a universal house style.

### 3. Classify Fidelity

Use:
- `strongly_adopted`: native screen clearly matches the concept family.
- `prototype_visual_gate_passed`: native screen is close enough to support
  prototype exit for a core product surface.
- `same_family_only`: native screen is related to Stitch but not rich or close
  enough for prototype exit when the screen is core.
- `partially_adopted`: layout/features exist, but artwork or mood is weakened.
- `generic_substitute`: native screen uses generic symbols/cards where the concept had product-defining artwork.
- `missing`: concept surface has no native equivalent.
- `intentionally_deferred`: a ready follow-up task exists with a reason.
- `parity_unproven`: exact or close matching is claimed, but the evidence does
  not prove it requirement-by-requirement.

### 4. Choose An Asset Strategy

For every product-critical visual, choose one:
- source artwork extracted from Stitch HTML
- bundled source/reference asset from `.stitch/intake/assets/`
- new Stitch art expansion screen or state
- native vector/shape drawing
- generated bitmap asset
- SF Symbol plus custom treatment
- deferred asset task

Prefer source artwork from `.stitch/intake/assets/` when Stitch HTML already
provides usable hero/card/badge imagery. Do not silently replace available
Stitch artwork with weaker generated substitutes or plain SF Symbols. If source
artwork is unavailable, unsuitable, or intentionally not used, record why. If a
placeholder or generated substitute is used, mark it as a substitute and create a
visual-fidelity task before beta or release-readiness.

When the app needs more high-quality product artwork than the current intake
contains, use `references/stitch-art-expansion-loop.md`: ask Stitch for another
screen, state, or variant in the same visual world, then rerun intake and asset
extraction before implementing a weaker native substitute.

### 5. Insert Or Implement The Visual-Spine Task

If the app is still early, prefer one coherent visual-spine task over many tiny
polish tasks. It may cover multiple screens when they share the same design
language.

Good early visual-spine tasks often create:
- shared visual primitives
- hero artwork components
- image-forward recipe/content cards
- background/motif components
- badge/reward treatments
- tab/app shell personality
- screenshot comparison evidence

Before implementation, create or update screen implementation packets under
`.stitch/screen-packets/` for the core screens you will touch. These packets
bridge Stitch evidence to SwiftUI destinations and should name the visual spine,
interaction contract, data/state needs, safety/privacy copy, and validation path.
When source artwork exists, packets should include the specific asset manifest
entries or `.stitch/intake/assets/` paths that should drive native image assets.

### 6. Run Prototype Visual Exit Audit

Before any task or closeout claims prototype completion, dogfood readiness,
user-testing readiness, beta readiness, or exact Stitch parity, audit the core
screen set:
- onboarding/app shell
- discovery/home
- primary detail
- creation or capture/result flow
- history/log
- reward/trust moment
- settings or guidance

For each applicable screen, compare the Stitch reference, screen packet, source
assets, native SwiftUI destination, and latest simulator screenshot. If the
screen is only `same_family_only`, `partially_adopted`, `generic_substitute`, or
`parity_unproven`, create or activate a visual-spine task instead of promoting
maturity.

Write or update `.stitch/visual-parity-audit.md` using
`references/visual-parity-audit-template.md` when the audit affects maturity,
user-testing readiness, beta readiness, or exact-reference work.

After updating the audit and `.stitch/metadata.json`, run:

```bash
python3 <ios-visual-spine-skill-dir>/scripts/validate_visual_exit.py \
  --repo-root . --claim prototype_exit
```

Resolve `<ios-visual-spine-skill-dir>` as the directory containing this active
`SKILL.md`. Use `user_testing_readiness`, `beta_readiness`,
`release_readiness`, or `exact_reference` when that is the actual claim. A
blocked result must keep or create the smallest visual-spine task; it cannot be
overridden by a successful build or by prose in roadmap notes. The script
validates evidence consistency and coverage. It does not replace the required
side-by-side visual judgment.

When a user asks for a named screen to match Stitch exactly, classify the target
as `exact_reference` and keep work active until a requirement-by-requirement
comparison proves the match or documents each remaining mismatch as a product
decision.

### 7. Close With Evidence

Before closing the task:
- capture simulator screenshots for changed screens
- compare them with Stitch references
- record the adoption outcome in roadmap notes
- update `.stitch/DESIGN.md` or `.stitch/metadata.json` when the design system changed
- create follow-up tasks for unresolved core-screen fidelity gaps

## Output

Produce either:
- a visual-spine audit with prioritized roadmap tasks, or
- direct implementation plus evidence, if the requested scope is clear.

When writing an audit, include the packet paths that should drive the next
implementation task.

Do not claim beta, release-candidate, or production readiness while core screens
still have `generic_substitute` visual status unless the user explicitly accepts
that tradeoff.
