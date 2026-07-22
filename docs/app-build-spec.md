# [APP_NAME] Build Spec

## Purpose

Build `[APP_NAME]`, a `[PRIMARY_PLATFORM]` app that helps `[TARGET_USER]`:

- `[JOB_TO_BE_DONE_1]`
- `[JOB_TO_BE_DONE_2]`
- `[JOB_TO_BE_DONE_3]`

## Product Intent

This app should feel:

- `[DESIRED_QUALITY_1]`
- `[DESIRED_QUALITY_2]`
- `[DESIRED_QUALITY_3]`

It should not feel:

- `[UNDESIRED_QUALITY_1]`
- `[UNDESIRED_QUALITY_2]`
- `[UNDESIRED_QUALITY_3]`

## Must-Have Features

1. `[FEATURE_1]`
2. `[FEATURE_2]`
3. `[FEATURE_3]`
4. `[FEATURE_4]`

## Launch Scope

### Phase 1
- `[PHASE_1_ITEM_1]`
- `[PHASE_1_ITEM_2]`

### Phase 2
- `[PHASE_2_ITEM_1]`
- `[PHASE_2_ITEM_2]`

## Design Inputs

### Stitch or concept references
- `[STITCH_REFERENCE_1]`
- `[STITCH_REFERENCE_2]`

### Benchmark apps or products
- `[BENCHMARK_1]`
- `[BENCHMARK_2]`

## Backend / Data Notes

- backend strategy: `[BACKEND_STRATEGY]`
- service notes: `[SERVICE_NOTES]`
- analytics / instrumentation notes: `[ANALYTICS_NOTES]`
- expected first service maturity: `[level0_placeholder | level1_contract | level2_client | level3_local_dev | level4_integrated | level5_production_ready]`

## Operating Expectations

- current app maturity should be treated as: `[prototype | dogfood | beta | release_candidate | production]`
- roadmap tasks should use the current task template
- the active baton should use the current baton schema
- metadata should track evidence, risk, service maturity, and task injection history
- cross-feature coherence should be reviewed when recurring patterns or shared seams change
- release-readiness work should be injected only when maturity and risk justify it

## Validation Expectations

- changed features should be built and run before being declared complete
- validation depth should match the task's validation tier
- regression scope should match the task's blast radius
- evidence quality should match the task's expectation: `light`, `standard`, or `strong`
- core user flows should be verified manually when practical
- backend-connected features should be tested end to end

<!--
## Example App Specific Success Criteria

This build spec is successful if the app can:

- serve the target user and core jobs to be done clearly
- deliver the must-have features at the intended level of quality
- reflect the desired product feel while avoiding the undesired qualities
- maintain a clear launch scope with realistic phase boundaries
- keep roadmap, baton, and metadata state aligned with the real implementation
- validate changed features to the right depth for task risk and blast radius
- verify core user flows manually when practical and backend flows end to end when needed
- capture evidence and remaining risk honestly enough for the current app maturity
- leave the repo in a more operational state after each meaningful delivery loop
-->

## Fresh Agent Bootstrap Prompt

Copy and adapt this when handing the repo to a new coding agent:

```md
You are bootstrapping and building `[APP_NAME]`.

Use this repo as a roadmap-driven, agent-assisted iOS app development workspace.

Your job is to:
1. inspect the repo and infer the current implementation state
2. read the local instruction and memory files
3. ask only the most important missing product questions
4. refine the roadmap and source-of-truth docs where needed
5. identify the highest-value next task
6. move into implementation and validation mode

Important working rules:
- treat `AGENTS.md` as the repository's operational instructions
- use `docs/app-build-spec.md` as the product brief
- use `.stitch/APP.md`, `.stitch/DESIGN.md`, `.stitch/ROADMAP.md`, `.stitch/next-prompt.md`, and `.stitch/metadata.json` as repo-local operating memory
- separate current-state truth from design authority: verified implementation
  defines existing behavior, while approved design-first references define the
  intended visual target until explicitly accepted, rejected, or superseded
- validate meaningful changes through the appropriate build/run/debug loop
- update roadmap state, baton state, evidence state, and risk state before finishing

When backend or cloud services are needed:
- define the app-facing contract
- implement or refine the service layer at the right maturity level
- test the real data flow end to end when applicable

When design exploration is needed:
- use Stitch conceptually
- save useful design artifacts locally
- translate concepts semantically, not literally
- record adoption outcome when concept work materially informs the app

Always leave the repo in a more operational state:
- clearer instructions
- clearer roadmap
- clearer source-of-truth guidance
- validated implementation progress
- explicit evidence and remaining risk where appropriate
```
