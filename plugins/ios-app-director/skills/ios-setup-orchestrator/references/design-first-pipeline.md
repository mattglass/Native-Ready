# Design-First Setup Pipeline

This is the internal design-first pipeline used by the public
`ios-app-bootstrap` entry point.

## Old Manual Loop

1. Create Stitch screens.
2. Copy Stitch notes into a separate document.
3. Ask a chat to produce a large feature plan from screenshots and notes.
4. Paste that plan into `.stitch/APP.md` section 9.
5. Run bootstrap/director from the enriched memory.

## New Agentic Loop

1. `ios-app-bootstrap` owns the run, preflights capabilities, and delegates the
   design-first phases when they apply.
2. `stitch-ios-concept-builder` resolves one active project and creates
   first-pass Stitch screens when no design project exists yet.
3. `stitch-ios-intake` gathers Stitch project, screens, screenshots, HTML,
   design-system signals, source image assets, notes, and stable intake
   manifests.
4. `ios-feature-map` generates and quality-checks `.stitch/APP.md` section 9.
5. `ios-visual-spine` names product-critical artwork, motifs, hero media,
   image-forward components, asset strategy, and visual-fidelity gates.
6. `ios-app-bootstrap` fills or repairs repo-local operating files and preserves
   one public completion contract.
7. `ios-native-scaffold` creates the initial SwiftUI Xcode project and replaces placeholder native paths.
8. XcodeBuildMCP discovers the scheme and attempts the first simulator build/run.
9. `ios-app-bootstrap` writes the non-blocking bootstrap receipt and hands off.
10. `ios-app-director` begins implementation only when delivery is authorized.
11. `ios-feature-closeout` reconciles evidence, risk, roadmap, metadata, and baton.

## Design Evidence Order

Prefer sources in this order:
1. live native implementation, if it exists
2. user-provided product decisions
3. live Stitch MCP project data
4. extracted Stitch image assets indexed by `.stitch/intake/image-asset-manifest.*`
5. exported Stitch screenshots and HTML indexed by `.stitch/intake/intake-manifest.*`
6. Google Docs or pasted ChatGPT feature plans
7. older speculative notes

## Setup Done Criteria

Setup is complete when:
- `.stitch/APP.md` has a useful section 9 feature inventory
- `.stitch/DESIGN.md` names the app's semantic design direction
- `.stitch/intake/image-asset-manifest.*` exists when Stitch HTML contains
  product-critical source artwork
- the visual spine is explicit enough for implementation: product-critical
  artwork, image treatment, motifs, native asset strategy, and first visual
  fidelity gates are named in APP/DESIGN/ROADMAP/metadata
- `.stitch/metadata.json` records primary Stitch project and reference screens
- requested and product-required concept roles have been audited; missing roles
  remain visible as actionable expansion tasks rather than silent omissions
- no unresolved project-provenance violation or unreported ambiguous Stitch
  operation remains in the setup handoff
- `docs/app-build-spec.md` summarizes product purpose, scope, design inputs, and service notes
- `.stitch/ROADMAP.md` has at least three maturity-appropriate tasks
- `.stitch/next-prompt.md` points to the first concrete task
- the native scaffold exists, or setup is truthfully `blocked` by a concrete
  Xcode/tooling condition
- active operating memory does not use `MyApp` as a placeholder target
- Swift feature implementation has not started before the operating memory and native naming contract are coherent
- `docs/bootstrap-receipt.md` reports the first build/launch attempt, baton
  validation, active task, and remaining setup risks
