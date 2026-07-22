---
name: stitch-ios-intake
description: Capture or refresh design-first iOS app inputs from Google Stitch projects, Stitch screenshots, prompt notes, exported HTML, Google Docs feature plans, or pasted concept notes. Use before ios-app-bootstrap when a new SwiftUI app starts from screens/designs, and use again whenever a Stitch project gains new screens that should update APP.md, DESIGN.md, metadata, roadmap, or baton evidence.
---

# Stitch iOS Intake

Use this skill to turn rough design artifacts into structured app setup evidence.

The output is not implementation code. The output is a clean local intake record that `ios-feature-map`, `ios-app-bootstrap`, and `ios-app-director` can trust.

Use it in refresh mode when an existing app already has memory files but the live Stitch project has new or changed screens.

Resolve `<stitch-ios-intake-skill-dir>` as the directory containing this active
`SKILL.md`. Run bundled helper scripts from that directory; do not assume the
app repository contains a local plugin source checkout.

## Read First

If present, read:
- `references/intake-artifact-schema.md`
- `references/design-system-synthesis.md`
- `../stitch-ios-concept-builder/references/stitch-operation-policy.md`
- `SETUP.md`
- `AGENTS.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/intake/intake-manifest.json` or `.stitch/intake/intake-manifest.md`
- `.stitch/metadata.json`
- `.stitch/operations/current.json`
- `docs/app-build-spec.md`

## Workflow

### 1. Confirm The Setup Surface

Identify:
- app repo root
- app name and primary platform
- target user and product purpose
- current app maturity
- Stitch project name or project ID
- whether screenshots, exported notes, or a Google Doc plan already exist
- whether backend or Cloudflare work is in scope now

Ask only for missing inputs that block the intake. If the user gave a Stitch project name but no ID, use Stitch project listing when available.

### 2. Inspect Stitch When Available

When Stitch MCP tools are available:
- use `list_projects` if the project is unknown
- use `get_project` for project-level design theme, design system, screen instances, and project title
- use `list_screens` for screen titles, IDs, device type, screenshot URLs, HTML download URLs, dimensions, and ordering clues
- use `get_screen` for important screens when more detail is needed
- treat screenshot URLs as first-class intake evidence for later screen-to-feature extraction

Use only project IDs established by user input, repo metadata, intentional exact
discovery, or the current operation journal. Register secondary projects as
read-only references before project-specific inspection. Never probe an example
or stale project ID from tool documentation or another app.

Do not generate or edit Stitch screens during intake unless the user explicitly asks for new concept work.

When Stitch MCP is not available, use screenshots, pasted notes, exported HTML, Google Doc content, or user-provided screen descriptions.

### 3. Save New URL Artifacts With A Stable Command

When a new Stitch screen exposes screenshot or HTML download URLs, save them through the bundled script instead of composing a path-specific shell chain with `mkdir`, `curl`, `file`, and `wc`:

Preferred queued form:

```bash
python3 <stitch-ios-intake-skill-dir>/scripts/save_stitch_screen_artifacts.py --repo-root . --from-queue
```

Before running it, write `.stitch/intake/pending-stitch-artifacts.json`:

```json
{
  "artifacts": [
    {
      "slug": "13-achievement-unlocked",
      "screenshotUrl": "$SCREENSHOT_URL",
      "htmlUrl": "$HTML_URL",
      "screenTitle": "Achievement Unlocked",
      "screenId": "$SCREEN_ID"
    }
  ]
}
```

Direct single-screen form:

```bash
python3 <stitch-ios-intake-skill-dir>/scripts/save_stitch_screen_artifacts.py \
  --repo-root . \
  --slug 13-achievement-unlocked \
  --screenshot-url "$SCREENSHOT_URL" \
  --html-url "$HTML_URL" \
  --screen-title "Achievement Unlocked"
```

The script creates intake folders, downloads artifacts, validates PNG/HTML content, records source URLs in `.stitch/intake/artifact-sources.json`, clears the pending queue after a successful queued run, and rebuilds `.stitch/intake/intake-manifest.json` and `.stitch/intake/intake-manifest.md`.

### 4. Extract HTML Image Assets

After Stitch HTML files are saved, extract referenced `<img>` artwork into a
stable local asset manifest:

```bash
python3 <stitch-ios-intake-skill-dir>/scripts/extract_stitch_image_assets.py --repo-root .
```

The script reads `.stitch/intake/html/*.html`, downloads image URLs into
`.stitch/intake/assets/`, writes `.stitch/intake/image-asset-manifest.json` and
`.stitch/intake/image-asset-manifest.md`, and rebuilds the intake manifest.

Use this before visual-spine planning whenever the Stitch concepts include
product-critical hero art, food/product images, avatars, badges, icons, or
illustrations. Do not treat generated substitutes as equivalent when the Stitch
HTML already provides usable source artwork. If a source image is unavailable,
unsuitable, or not licensed/provenanced for the intended use, record that reason
and create an explicit generated-asset or art-direction follow-up.

### 5. Use Stable Artifact Discovery

Before inspecting local screenshots, exported HTML, or new intake paths with shell commands, build or refresh the stable intake manifest:

```bash
python3 <stitch-ios-intake-skill-dir>/scripts/build_intake_manifest.py --repo-root .
```

If the script is unavailable, use stable directory-level discovery such as `rg --files .stitch/intake | sort`.

Do not ask for or rely on shell approvals that enumerate each newly named screenshot or HTML file, such as `ls -lh .stitch/intake/screenshots/11-new-screen.png ...`. New Stitch assets should flow through `.stitch/intake/intake-manifest.json` and `.stitch/intake/intake-manifest.md`.

### 6. Create A Local Intake Record

Create or update `.stitch/intake/design-intake.md`.

In refresh mode:
- preserve existing implementation evidence and completed task records
- add new screens to the inventory instead of replacing useful older context
- call out which screens are new, changed, adopted, deferred, or rejected
- separate desktop/web concepts from literal iOS implementation targets
- distinguish screens discoverable in the active live project from saved
  artifact-only evidence

The intake record should include:
- product identity and unresolved questions
- Stitch project metadata
- screen inventory with screen IDs when known
- design system signals: colors, typography, spacing, tone, components
- visible feature clues by screen
- implied flows
- native implementation hints
- safety, privacy, and claim risks
- confidence notes
- source links or local artifact paths
- intake manifest paths and counts
- image asset manifest paths and product-critical source artwork candidates
- concept coverage for requested/product-required roles using `live`,
  `artifact_only`, `missing`, `deferred`, or `not_needed`

If screenshots are available, create `.stitch/intake/screenshots/` and save or reference each screen image with stable names such as `01-welcome.png`, `02-focus-areas.png`, or `screen-title-screenId.png`. If download is not practical, record the screenshot URL and screen ID in the intake record.

After saving or refreshing screenshot, HTML, note, or design-intake artifacts, rebuild the intake manifest before handing off.

Keep the intake factual. Do not inflate product scope yet.

### 7. Synthesize The Semantic Design System

Create or refresh `.stitch/DESIGN.md` with
`references/design-system-synthesis.md` when the repo still has template
placeholders or the intake reveals a material design-system change.

- preserve the READY document's eight-section contract
- distinguish observed rules from proposed rules
- use exact tokens only when evidence supports them
- capture native behavior, states, artwork, motion, accessibility, and banned
  patterns, not just colors and typography
- keep live SwiftUI tokens authoritative once implementation exists

Do not rewrite a stable design system merely because one new screen differs.
Record the difference as a question or candidate direction until the evidence
supports a system-level change.

### 8. Update Structured Metadata

When `.stitch/metadata.json` exists, update only the relevant setup fields:
- `stitchProjects.primaryConceptProject`
- `referenceScreens`
- `app.name`, `app.platform`, `app.framework`, `app.repoRoot`
- design-system source notes if the schema has a place for them
- image asset source/provenance notes when product-critical artwork was
  extracted from Stitch HTML
- `stitchOperations` with the durable active-project and unresolved-operation summary
- `conceptCoverage` with live-versus-artifact provenance and linked expansion tasks

Preserve existing evidence, risks, roadmap history, and implementation records.

### 9. Hand Off

After intake, hand off to `ios-feature-map` with:
- path to `.stitch/intake/design-intake.md`
- path to `.stitch/intake/intake-manifest.json` or `.stitch/intake/intake-manifest.md`
- path to `.stitch/intake/image-asset-manifest.json` or `.stitch/intake/image-asset-manifest.md`
- path to any Google Doc export or pasted plan
- key Stitch project ID
- screen list and priority order
- required concept roles that are missing, artifact-only, or deferred
- unresolved Stitch operation IDs and recovery state
- remaining questions

Do not proceed to Swift files from this skill.
