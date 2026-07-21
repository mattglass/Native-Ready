# Stitch Art Expansion Blueprint

Use this when an existing design-first iOS app needs more artwork, content
variants, or screen states after the initial Stitch concept set.

## Goal

Generate additional Stitch screens or variants that preserve the existing app
visual world and give the native iOS builder better source material for:
- hero artwork
- image-forward cards
- recipe, item, lesson, or content variants
- badges and reward moments
- mascot or character states
- empty, loading, success, and result states
- safety, trust, and grown-up/admin surfaces

## Project Rule

If the app already has a Stitch project, add to that project. Do not create a
new project unless the user asks for a fork or the existing project is clearly
unrelated.

## Prompt Shape

Use the existing app name, target user, and design system. Name the specific
screen/state being expanded and the native gap it should unblock.

Ask for a full iPhone app screen or screen state that includes the needed art in
context. This gives the native builder layout, hierarchy, component treatment,
copy tone, and extractable artwork from the same artifact.

Include:
- app identity and visual tone
- reference screens to stay consistent with
- artwork needed
- screen role and user action
- data/content examples
- trust/safety/privacy copy when relevant
- production-quality native iOS concept language
- request for visible labels and image-forward elements

## Handoff

After generation, hand off to `stitch-ios-intake` so it can:
- save screenshots and HTML under `.stitch/intake/`
- extract image assets into `.stitch/intake/assets/`
- rebuild intake and image asset manifests
- update design intake, metadata, APP.md, DESIGN.md, screen packets, roadmap,
  and baton when the new evidence changes implementation scope
