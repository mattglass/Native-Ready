# Design Authority Regression — 2026-07-22

## Outcome

The visual downgrade was not caused by Stitch losing the LawnCare design
language, and the design-spine skill was not removed. The engine contained a
latent source-of-truth inversion: as soon as an initial SwiftUI implementation
existed, several starter and skill documents instructed later work to treat it
as visual authority. A generic first pass could therefore demote stronger
Stitch references into optional concepts.

The second failure was enforcement. Visual promotion rules existed only as
prose. Nothing executable stopped roadmap metadata from declaring a prototype
visual pass while a core screen remained same-family-only, used generic
substitutes, or lacked the required full-app audit.

## Commit And PR Audit

The LawnCare workspace started from `85f7cd7`, the merge of PR #7. LotCoach
started from `f320378`, the merge of PR #10. The intervening changes were:

| PR | Change | Design-regression finding |
|---|---|---|
| #1 | Fixed baton YAML frontmatter | Baton schema and validator only; no visual-authority change |
| #2 | Updated NATIVE READY branding | README and setup copy only |
| #3 | Added global plugin installation | Marketplace, manifest, and installation docs; no visual-authority change |
| #4 | Added licensing and plugin artwork | Packaging, license, and brand assets only |
| #5 | Split engine and plugin licensing | License-boundary changes only |
| #6 | Fixed Stitch API-key onboarding | Authentication, MCP, and setup changes only |
| #7 | Hardened first-run bootstrap | Xcode/toolchain, scaffold, launch, and receipt changes; no visual-authority change |
| #8 | Made Cloudflare MCP opt-in | Configuration-only; no visual workflow change |
| #9 | Hardened standalone plugin deployment and script path resolution | Did not weaken visual rules; made the committed starter more consistently deployable |
| #10 | Added bounded Stitch timeout recovery and longer MCP timeout | Preserved prompt content and project identity, but under-enforced polling evidence and design handoff readiness |

`git blame` traces the conflicting hierarchy to initial commit `8168dbd`, so it
predates that PR window. LawnCare's effective local plugin files also match
current main apart from files that were untracked at its older base commit.
There is no evidence that LawnCare succeeded because it ran a distinct older
visual-spine implementation.

The closer PR #10 audit found a separate contributing weakness, not the cause
of LotCoach's prompt quality. LotCoach has five durable, design-rich prompt
files and five successful operations; none timed out. Its downgrade happened
after Stitch, during authority and native translation. However, PR #10's
journal accepted a counter-only polling transition and required only one poll,
while the active generation and variant tool contracts prescribe polling every
30 seconds up to 10 times. Its default operational audit also exited zero when
required concept coverage was missing but linked to a future task. That made a
partial concept set easy for a downstream loop to mistake for implementation
readiness.

At code level, PR #10 introduced or preserved four specific gaps in
`stitch_operation_journal.py` and its policy:

- `transition_operation(..., "polling")` incremented `pollCount` without an
  observed screen list, project update time, response-completeness flag, or
  matching-output decision;
- timeout recovery and replacement authorization required only one recorded
  polling transition instead of the active tool's complete 10-poll budget;
- `audit_concept_coverage` returned no error or warning for a required missing
  role as long as `linkedTask` was populated; and
- the journal retained prompt text and digest but not the durable prompt-file
  path, so audit could not confirm the app-local prompt artifact still matched.

## Root Cause

The inversion was repeated across the generated app contract:

- `.stitch/DESIGN.md` put live implementation first as visual source of truth.
- `docs/ai-app-development-engine-spec.md` said the live app wins for UI.
- `docs/app-build-spec.md` subordinated conceptual design to implementation.
- `AGENTS.md` warned agents not to let concepts outrank implementation without
  distinguishing runtime truth from intended visual identity.
- `stitch-ios-intake` told refresh work to keep live SwiftUI tokens
  authoritative once implementation existed.

Those instructions conflict with the visual-spine rules that say not to flatten
image-forward Stitch work into default cards or SF Symbols. Because no
deterministic closeout check existed, the conflict could resolve differently
between otherwise similar app runs.

Additional inversions remained in `.stitch/APP.md`, the Stitch prompt evidence
order, and `stitch-loop-ios`: they ranked current native files or tokens above
the active Stitch visual system. This could feed a generic first native pass
back into later prompts and compound the downgrade.

## App Evidence

LawnCare retained honest gate state. Its onboarding passed, while Today, Plan,
History, and Settings remained blocked because their required Stitch roles were
missing.

LotCoach inverted the hierarchy in its generated `.stitch/DESIGN.md`, placed
the live SwiftUI implementation first, and recorded prototype promotion even
though:

- `.stitch/visual-parity-audit.md` was missing;
- Vehicle Match & Lot Camera recorded only same-product-family evidence; and
- its native vehicle treatment used generic silhouettes while the concept was
  image-forward.

That is an engine governance failure, not proof that the Stitch intake failed.

## Repair

Version `0.5.6` separates two kinds of truth:

- verified native behavior is authoritative for what currently exists; and
- user-approved design decisions, active Stitch references, extracted artwork,
  `.stitch/DESIGN.md`, and screen packets remain authoritative for intended
  visual identity until explicitly accepted, rejected, superseded, or proven by
  the applicable visual gate.

The repair also adds `ios-visual-spine/scripts/validate_visual_exit.py`. Before
a design-first maturity or exact-parity claim, it requires:

- a parseable `.stitch/visual-parity-audit.md` with a passing core-screen matrix;
- prototype-gate or exact-reference evidence rather than same-family evidence;
- matching structured parity metadata and simulator evidence;
- decisions for extracted source artwork;
- no unresolved generic, partial, unproven, or same-family adoption; and
- no missing or deferred required concept coverage.

The validator checks evidence consistency; side-by-side visual judgment remains
required. Director, visual-spine, roadmap-governance, and closeout instructions
now treat a nonzero result as a hard promotion gate.

The operation journal repair preserves PR #10's useful durable-prompt and
single-project recovery model while making it evidence-bearing:

- generation and variant operations default to the complete 10-poll contract;
- every poll records project update time, screen IDs, response completeness,
  and matching output rather than incrementing a counter;
- durable prompt paths and digests are verified from app-local memory;
- `ambiguous_timeout` and replacement authorization require the complete poll
  budget plus final same-project reconciliation; and
- a separate `native-design-handoff` audit fails for missing required concepts,
  unresolved matching operations, missing artifact provenance, or deferred
  fallback without explicit user acceptance.

Operational intake may still preserve partial coverage for planning. It can no
longer present that partial state as permission to implement the dependent
SwiftUI surface.

## Validation And Rollout

Before merge:

1. run the dependency-free plugin test suite;
2. validate each modified skill with `quick_validate.py`;
3. run the visual-exit validator against a passing fixture;
4. confirm it blocks LotCoach for its missing audit and same-family vehicle
   evidence;
5. confirm it preserves LawnCare's existing blocked full-app decision; and
6. confirm the operational journal audit remains informative for legacy state
   while the native-design-handoff gate blocks LawnCare's unresolved concepts;
7. confirm LotCoach's five successful durable prompts pass journal integrity
   checks, proving the regression occurred after prompt generation; and
8. verify root starter files remain byte-identical to their deployed-template
   copies.

After merge:

1. publish or reinstall iOS App Director `0.5.6` and restart Codex so the active
   skill snapshot is unambiguous;
2. use the updated template for all newly deployed READY apps;
3. migrate existing design-first apps by repairing the header in
   `.stitch/DESIGN.md`, rerunning the full-app visual audit, and activating the
   smallest visual-spine recovery task when validation blocks; and
4. recover LotCoach in its own app branch after the engine fix lands, preserving
   its functional improvements while rebuilding the shell, live coach,
   debrief, and vehicle experience from Stitch evidence.

## Acceptance Criteria For Main

- No distributed instruction says that an early live implementation
  automatically wins visual authority.
- Root and deployed starter contracts use the same design-authority hierarchy.
- A design-first maturity claim without a full audit fails deterministically.
- Same-family, generic-substitute, parity-unproven, partial, missing, or deferred
  core evidence cannot pass promotion.
- Extracted source artwork requires an explicit adoption decision.
- Polling recovery cannot advance on counter-only or prematurely exhausted
  evidence.
- Required missing concept evidence may continue into planning but blocks
  dependent native design handoff.
- Plugin tests cover the hierarchy, operation recovery, handoff gate, and
  executable visual promotion gate.
