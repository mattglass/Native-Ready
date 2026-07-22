---
name: ios-feature-map
description: Synthesize or refresh a quality-controlled iOS App Feature Inventory and Requirements Map from Stitch screens, screenshots, prompt notes, Google Docs, ChatGPT feature plans, or design-intake artifacts. Use to fill or update `.stitch/APP.md` section 9, refine `docs/app-build-spec.md`, and seed roadmap candidates before ios-app-director starts implementation or when new Stitch evidence changes the app plan.
---

# iOS Feature Map

Use this skill to replace the manual "paste a giant feature plan into APP.md" step with a repeatable synthesis workflow.

Use it again after `stitch-ios-intake` refreshes an existing app with new Stitch screens.

Resolve `<ios-feature-map-skill-dir>` as the directory containing this active
`SKILL.md`. Run its bundled helper from that directory rather than assuming the
app repo contains the script.

## Read First

Read:
- `references/feature-map-template.md`
- `references/quality-rubric.md`
- `references/screenshot-analysis-prompt.md`
- `../stitch-ios-concept-builder/references/stitch-operation-policy.md`

If present, also read:
- `.stitch/intake/design-intake.md`
- `.stitch/intake/intake-manifest.json` or `.stitch/intake/intake-manifest.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/metadata.json`
- `.stitch/operations/current.json`
- `.stitch/ROADMAP.md`
- `docs/app-build-spec.md`
- any Google Doc export, pasted plan, screenshots, or Stitch screen notes supplied by the user
- any new user prompt that changes product capability, user outcomes, data or
  service expectations, roadmap scope, or implementation priority

## Workflow

### 1. Separate Evidence From Inference

Organize inputs into:
- visible features from live Stitch screens
- artifact-only evidence from saved screenshots, HTML, or extracted assets
- explicit notes from the user or Google Doc
- inferred requirements
- safety, privacy, service, data, and AI implications
- unknowns

Use `.stitch/metadata.json` `conceptCoverage` as the durable coverage ledger
when it exists. Coverage roles are derived from the product brief, user prompt,
and feature map; do not impose a fixed screen list or screen count. Classify each
role as `live`, `artifact_only`, `missing`, `deferred`, or `not_needed`, and keep
its evidence provenance explicit.

If `.stitch/operations/current.json` contains an unresolved operation, preserve
its operation ID and recovery state. An invalid-argument response means the
operation did not start. A timeout or connection loss leaves the outcome
unknown until polling resolves it or the operation becomes
`ambiguous_timeout`. Never interpret either outcome as permission to create a
fallback project.

When a new user prompt changes future product behavior, update the feature map
before roadmap implementation. Treat it as `note` evidence unless it is already
visible in screenshots or Stitch artifacts.

Do not force purely visual or artwork-only prompts into `.stitch/APP.md` unless
they imply a user-facing capability, requirement, or implementation task. Route
visual language, composition, component personality, and fidelity expectations
to `.stitch/DESIGN.md`, `.stitch/visual-spine-plan.md`, or screen packets, then
seed roadmap work only when native implementation is needed.

Mark risky or speculative requirements as implied, future, or requires validation.

When screenshots or Stitch screen images are available, first run the screen-to-feature extraction pass described in `references/screenshot-analysis-prompt.md`. Treat the extracted screen observations as high-value evidence because they reveal what the design actually communicates.

If an intake manifest exists, use it as the artifact index for screenshots, HTML exports, notes, and design-intake records. If the Stitch project changed and the manifest is stale or missing, refresh it with the stable `stitch-ios-intake` manifest command or a directory-level `rg --files .stitch/intake | sort` fallback before analysis. If new screenshot or HTML URLs need to be downloaded, use the stable `save_stitch_screen_artifacts.py` command first. Do not use path-specific shell commands that enumerate each newly added screenshot or HTML file.

### 2. Produce The Feature Map

Use `references/feature-map-template.md`.

The feature map should include:
- product reading summary
- feature list by screen
- navigation model
- core requirements matrix
- missing or implied screens
- AI/service/data requirements where relevant
- design and UX observations
- MVP, next-release, and later scope
- quality-control notes
- product requirement summary

For every product-required concept role that is `missing`, include a concrete
`stitch_art_expansion` next action against the existing active project and link
it to the corresponding coverage entry. A role backed only by saved artifacts
may guide native work, but label it `artifact_only` rather than claiming it is a
live Stitch screen. A deliberately postponed role may be `deferred` with the
reason and revisit condition recorded.

Keep this useful for agents. Name likely native destinations only when enough repo context exists.

### 3. Apply Quality Control

Use `references/quality-rubric.md`.

Before writing the map, check:
- Does each feature trace to a screen, note, or inference?
- Are unsupported claims softened?
- Are privacy, consent, deletion, auth, and retention issues visible?
- Are regulated-domain risks flagged?
- Are MVP tasks separated from later ambition?
- Are service contracts separated from UI placeholders?
- Are roadmap candidates concrete enough for `ios-app-director`?
- Does each product-required concept role have truthful coverage and provenance?
- Does each required `missing` role have a linked `stitch_art_expansion`
  candidate rather than an unrecorded generic native substitute?
- Are unresolved Stitch operation IDs and recovery states preserved?

### 4. Write Section 9

Use the helper script when possible:

```bash
python3 <ios-feature-map-skill-dir>/scripts/replace_app_feature_inventory.py \
  --app-md /path/to/repo/.stitch/APP.md \
  --feature-map /path/to/generated-feature-map.md
```

The script replaces `## 9. App Feature Inventory & Requirements Map` and preserves the rest of `APP.md`.

If writing manually, keep the heading exactly:

```md
## 9. App Feature Inventory & Requirements Map
```

### 5. Update Supporting Memory

After section 9 is updated:
- update `docs/app-build-spec.md` with the concise product purpose, must-have features, design inputs, service notes, and maturity expectations
- update `.stitch/metadata.json` when new Stitch projects, reference screens,
  risk records, service maturity facts, operation state, or concept coverage is
  known; preserve `stitchOperations` and `conceptCoverage`
- create or refine `.stitch/ROADMAP.md` only after the feature map is coherent
- write `.stitch/next-prompt.md` from the highest-value concrete first task

When a required concept role is missing, seed or preserve a
`stitch_art_expansion` roadmap candidate. Keep the project ID tied to the active
project provenance and carry any unresolved operation ID into the task and
baton. Missing concept evidence blocks only work that depends on that evidence;
continue dependency-safe native or planning work.

When refreshing an app that already has native code:
- preserve completed task evidence
- do not overwrite scaffold/build validation records
- add roadmap candidates only for materially new screens, risks, or implementation gaps
- keep the current baton unless the new evidence changes the active task's scope or priority

Do not start Swift implementation from this skill. Hand off to `ios-app-bootstrap`, `ios-app-director`, or `stitch-loop-ios`.
