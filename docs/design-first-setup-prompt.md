# Advanced Design-First Bootstrap Inputs

This file adds detailed Stitch guidance to the stable bootstrap. It is not a second setup front door.

Start with `$ios-app-bootstrap`. The skill may delegate design phases internally to `stitch-ios-concept-builder`, `stitch-ios-intake`, `ios-feature-map`, `ios-visual-spine`, `stitch-loop-ios`, and the internal `ios-setup-orchestrator` coordinator.

## Recommended First Prompt

```md
Use $ios-app-bootstrap as the single READY setup entry point for this design-first iOS app.

App name: [APP_NAME]
App idea: [SHORT_PRODUCT_IDEA]
Target users: [WHO_IT_IS_FOR]
Primary outcome: [WHAT_THE_APP_HELPS_THEM_DO]
Platform: [IPHONE_ONLY or IPHONE_AND_IPAD]
Visual tone: [DESIGN_FEEL]
Stitch project: [STITCH_PROJECT_NAME_OR_ID or NONE_YET]
Stitch role: PRIMARY_CONCEPT_SOURCE
Screenshots or feature plan: [PATHS_OR_NONE]
Backend needed now: [YES or NO]
Cloudflare needed now: [YES or NO]
Bundle identifier: [FINAL_REVERSE_DOMAIN_ID or PROVISIONAL]

Keep one active Stitch project for this app's visual world and record its provenance. Do not create fallback projects or use unproven project IDs after tool errors, empty reads, or timeouts.

For each product-required core concept role:
1. Generate or identify the first result.
2. Inspect hierarchy, clipping, overflow, generic treatment, product identity, and usefulness as native implementation evidence.
3. Use edit or variant operations for material defects, with at most two corrective attempts during bootstrap.
4. Keep the strongest usable result and record unresolved visual work in the roadmap.

Then complete the stable bootstrap contract:
1. Save or refresh `.stitch/intake/*` and stable manifests.
2. Extract product-critical source artwork from Stitch HTML when available.
3. Build or update `.stitch/APP.md` section 9 and `.stitch/DESIGN.md`.
4. Create the visual-spine plan and core `.stitch/screen-packets/`.
5. Update `docs/app-build-spec.md`, roadmap, metadata, risks, and baton.
6. Create the native SwiftUI Xcode scaffold with app-specific naming.
7. Use XcodeBuildMCP for scheme discovery and the first simulator build/launch.
8. Validate the active baton.
9. Render `docs/bootstrap-receipt.md`.
10. Stop after the receipt unless I also authorize product-feature delivery.

An ambiguous Stitch mutation blocks an untracked replacement of that same operation, not independent intake, native scaffolding, or build validation. Optional Cloudflare or non-critical concept gaps must not become the active baton when native work is executable.
```

## Design Evidence Rules

- Prefer user decisions and live native behavior over speculative concepts.
- Use live Stitch project data, saved screenshots/HTML, extracted artwork, and stable manifests as evidence.
- Preserve artwork, mood, image treatment, motifs, and component personality that make the product recognizable.
- Use `same_product_family` for early progress, `prototype_visual_gate` before maturity promotion, and `exact_reference` only when a named screen truly requires parity.
- Never copy Stitch HTML directly into SwiftUI.
- If design evidence is unavailable, continue with an explicitly degraded native design path unless Stitch was declared mandatory.

## Optional Delivery Goal

After `docs/bootstrap-receipt.md` reports `ready_for_delivery`:

```md
/goal Build autonomously toward the v1 app until the planned features work, the roadmap is reconciled, validation evidence is captured, and the app is ready for real user testing.

Use $ios-app-director to continue from the active baton.

Continue roadmap-driven implementation task by task. Validate meaningful native changes with XcodeBuildMCP, update evidence and repo memory, use bounded Stitch expansion when visual fidelity requires it, and keep advancing until a concrete external blocker or user-level product decision prevents meaningful progress.
```
