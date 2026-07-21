# Feature Map Quality Rubric

Use this before writing `.stitch/APP.md` section 9.

## Evidence Labels

Every major requirement should be one of:
- `visible`: seen directly in a Stitch screen or screenshot
- `note`: stated in user notes, a Google Doc, or prompt text
- `inferred`: likely from UX/product context but not directly shown
- `future`: useful later but outside MVP or current maturity

Every Stitch concept role should separately carry one coverage status:
- `live`: present in the active or registered reference Stitch project with
  proven project and screen identity
- `artifact_only`: supported by saved screenshot, HTML, or extracted asset, but
  not currently verified as a live screen
- `missing`: required by the product but not yet represented by adequate concept
  evidence
- `deferred`: deliberately postponed with a reason and revisit condition
- `not_needed`: reviewed and intentionally unnecessary

## Required Checks

- Separate visible UI from implied backend, AI, persistence, and service behavior.
- Convert vague product wishes into implementation-sized requirements.
- Keep MVP scope smaller than the full feature universe.
- Identify missing screens that the shown flows imply.
- Derive concept roles from the product and user intent; never require a fixed
  number of screens or a universal role checklist.
- Distinguish live Stitch evidence from artifact-only evidence and retain the
  project, screen, artifact, note, or inference provenance.
- Give every required `missing` concept role a linked `stitch_art_expansion`
  candidate against the existing active project. Do not silently substitute a
  generic native treatment for missing design evidence.
- Preserve unresolved Stitch operation IDs and truthful recovery states. An
  invalid argument did not start; a timeout is unknown until reconciled.
- Do not create or recommend a fallback Stitch project because generation,
  listing, or design-system retrieval failed. A new project is appropriate only
  for an intentional new visual world or explicit user-authorized fork.
- Identify the likely native destination or feature area when repo context exists.
- Flag service contracts before letting UI imply live integrations.
- Flag any wording that sounds like unsupported compliance, medical, financial, legal, or safety claims.
- Prefer "personalize" over "train" when describing user data for AI unless model training is explicitly intended and consented.
- Include privacy controls, consent, deletion, retention, auth, and audit needs for sensitive data apps.
- Keep design observations semantic: tone, hierarchy, navigation, trust, density, platform fit.
- Capture product-critical visual signatures separately from generic tone:
  hero artwork, image-forward cards, custom illustrations, motifs, backgrounds,
  glows, depth, motion, and playful or premium component treatments.
- Identify an asset/artwork strategy for each product-critical visual. Do not
  silently replace distinctive Stitch artwork with plain SF Symbols unless that
  is called out as a deliberate temporary scaffold choice.
- If `.stitch/intake/image-asset-manifest.*` exists, prefer saved Stitch source
  artwork for product-critical hero/card/badge images before planning generated
  substitutes. Generated assets are fallback, not proof of exact adoption.
- Mark any core screen whose native version would feel generic without a
  visual-fidelity follow-up task.

## Roadmap Candidate Gate

A requirement is ready to become a roadmap task only when it has:
- a clear user-facing outcome
- a likely native destination or module
- a validation tier
- an evidence expectation
- a regression scope
- a maturity-appropriate priority

If any of those are missing, keep it in the feature map or create a discovery/planning task instead of a native implementation task.

## Visual Fidelity Gate

For design-first apps, the feature map should seed at least one early roadmap
candidate for the visual spine when Stitch provides a distinctive look. That
candidate may be combined with onboarding/app shell work, but it must name:

- reference Stitch screens
- native destinations
- source artwork candidates from `.stitch/intake/assets/`
- asset or drawing strategy
- simulator screenshot comparison evidence
- acceptance criteria for the correct visual target:
  `same_product_family`, `prototype_visual_gate`, or `exact_reference`

If source artwork is missing or too weak for the target, seed a
`stitch_art_expansion` candidate before a native polish task. The expansion
should ask Stitch for another screen, state, or variant in the existing visual
world, then route the result through intake and asset extraction.

If the expansion operation times out, preserve it as unresolved, poll the same
project, and request replacement authorization as soon as the ambiguity blocks
the dependent visual task. Continue unrelated dependency-safe work while that
decision is pending.

Do not let prototype promotion, user-testing, release-readiness, or App Store
tasks outrun unresolved visual parity gaps on core screens such as onboarding,
discovery, primary detail, and the main creation flow.
