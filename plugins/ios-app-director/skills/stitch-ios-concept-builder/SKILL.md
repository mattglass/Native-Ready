---
name: stitch-ios-concept-builder
description: Generate first-pass Google Stitch iOS app concepts from bootstrap answers, product intent, target user, feature ideas, visual tone, or later artwork/screen-state expansion needs. Use before stitch-ios-intake when no Stitch project/screens exist yet, when a design-first iOS setup needs initial onboarding and primary app screens, or when the native app needs richer Stitch-consistent artwork.
---

# Stitch iOS Concept Builder

Use this skill to create the first design artifact set for a new iOS app idea.
Also use it when an existing design-first app needs more Stitch-generated
artwork, variants, or screen states to preserve the product's visual world.

The output is a Stitch project and screen set that can be analyzed by `stitch-ios-intake` and `ios-feature-map`. Do not implement Swift from this skill.

Resolve `<stitch-ios-concept-builder-skill-dir>` as the directory containing
this active `SKILL.md`. Run its operation-journal helper from that directory;
do not assume the app repo contains plugin scripts.

## Read First

Read:
- `references/screen-set-blueprint.md`
- `references/ios-stitch-prompt-contract.md`
- `references/art-expansion-blueprint.md`
- `references/stitch-operation-policy.md`

If present, also read:
- `../ios-app-bootstrap/references/bootstrap-questionnaire.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `docs/app-build-spec.md`

## Workflow

### 1. Gather Bootstrap Inputs

Collect only what is needed to generate useful screens:
- app name
- one-sentence purpose
- target user
- platform: iPhone only or iPhone and iPad
- first 3-5 must-have features
- desired visual tone
- backend / Cloudflare / AI scope
- sensitive-domain constraints
- example apps or style references

If the user already has a Stitch project, do not create a new one unless they ask.

When this is an artwork/content expansion for an existing app, gather:
- current Stitch project ID or name
- screen or feature needing richer artwork
- native visual gap blocking parity or maturity
- relevant existing Stitch reference screens
- needed variants or states
- whether the target is `same_product_family`, `prototype_visual_gate`, or
  `exact_reference`

### 2. Plan The Screen Set

Use `references/screen-set-blueprint.md`.

Default first screen set:
- Welcome / value proposition
- Primary onboarding choice or focus-area screen
- Goals/preferences setup
- First success / ready-to-start screen when onboarding is central to activation
- Data/sync/manual setup screen when data powers the app
- Main assistant/home screen
- One or two primary daily-use screens
- Profile/settings/privacy screen for sensitive apps

For non-health apps, translate the blueprint semantically rather than copying health-specific names.

Plan the set as focused mutation units as well as a coherent flow. Default to
one requested screen role per `generate_screen_from_text` call. When the active
tool explicitly supports a compound request and a small batch is materially
better, record every requested role in the operation journal so timeout
recovery can decompose it safely.

When the app targets kids, families, creativity, learning, games, wellness,
finance, health, or another trust-heavy domain, treat onboarding as a mini-flow,
not a single welcome screen. Generate enough onboarding screens to reveal:
promise, personalization, safety/trust, and the first meaningful action.

For artwork/content expansion, use `references/art-expansion-blueprint.md`.
Prefer additional screens or states in the existing project over isolated image
requests. The goal is to produce richer design evidence and extractable source
artwork that can be carried into SwiftUI.

### 3. Generate Or Edit In Stitch

Before the first Stitch call, verify that `STITCH_API_KEY` is available to the current Codex process without printing it. When it is absent, classify the capability as `api_key_required`, link the user directly to [Stitch Settings](https://stitch.withgoogle.com/settings), and use the plugin's secure macOS helper rather than asking for the secret in chat. Codex Desktop must be fully restarted after the key is added. Do not use Codex's generic OAuth **Authenticate** action for this API-key MCP.

When Stitch MCP tools are available:
- use `create_project` if no project exists
- use `generate_screen_from_text` for the first screen
- use focused additional `generate_screen_from_text` calls for distinct related
  screens; do not pack a whole screen set into one prompt only to reduce calls
- use `generate_variants` for a small comparable exploration of one real
  product decision
- use mobile device type for iPhone-first work
- build every generation, variant, or edit prompt with
  `references/ios-stitch-prompt-contract.md`
- use the active Stitch design system when one exists; otherwise carry the
  semantic rules from `.stitch/DESIGN.md` into the prompt
- explicitly request product-critical artwork, hero media, image-forward cards,
  motifs, and visual-spine consistency across screens
- when expanding artwork, ask Stitch to keep the same visual world and generate
  the missing screen/state/variant that will unblock native fidelity

Before the first project-specific read or mutation, follow
`references/stitch-operation-policy.md` and establish the operation journal with
`<stitch-ios-concept-builder-skill-dir>/scripts/stitch_operation_journal.py`
when available.

- Adopt a project ID only from user input, repo metadata, an intentional exact
  discovery match, or the successful current-run `create_project` result.
- Once a project is adopted, keep using it. Tool errors must not create fallback
  projects or cause calls against example/stale IDs.
- Snapshot screen IDs before a mutation, prepare the journal operation, and
  classify its result before reporting progress. Persist the exact prompt with
  `--prompt-file` and list each requested role with
  `--requested-screen-role`; never put secrets in a Stitch prompt.
- Treat an invalid argument as a payload problem, not a project problem.
- Treat `auth_required` with a present `STITCH_API_KEY` as a key-propagation or key-validity problem, not permission to create a replacement project.
- Treat a timeout as outcome unknown and poll the same project according to the
  current Stitch tool contract, recording each poll in the journal.
- When polling is exhausted, record `ambiguous_timeout` and act on the configured
  recovery mode immediately; do not finish unrelated work first.
- Default READY recovery to `autonomous`: perform one final same-project
  reconciliation, policy-authorize one linked replacement, and continue the
  loop without asking the user. For a compound request, decompose the recovery
  into focused screen roles instead of repeating the compound prompt.
- Escalate to the user only when recovery mode is `manual`, the bounded recovery
  is exhausted, or the remaining choice changes product intent.

These invariants do not constrain prompt content, screen-set size, visual
direction, or the decision to generate additional coherent variants.

### 4. Save Setup Evidence

After generation:
- record project ID, screen IDs, titles, screenshot URLs, and HTML URLs in `.stitch/intake/design-intake.md` if the repo exists
- record useful response descriptions, suggested follow-up changes, and variant
  rationale in the operation journal or intake record instead of discarding them
- update `.stitch/metadata.json` with primary project and reference screens when safe
- reconcile requested/product-required screen roles as `live`,
  `artifact_only`, `missing`, `deferred`, or `not_needed`
- generate a required `missing` role autonomously when no unresolved operation
  already covers it; missing concept evidence is work for the Stitch loop, not
  a routine user decision
- keep each required missing role actionable through a `stitch_art_expansion`
  task rather than treating the concept set as silently complete
- hand off to `stitch-ios-intake`

### 5. Avoid Premature Scope Lock

Generated screens are concept evidence, not product truth. The next skill must still extract and quality-check the feature map before roadmap or Swift implementation begins.
