---
name: stitch-loop-ios
description: Iterative Stitch-to-iOS workflow for SwiftUI apps. Reads an iOS baton from .stitch/next-prompt.md, uses Stitch MCP for concept generation or editing, translates concepts into native destinations, and updates the app-focused Stitch workspace.
allowed-tools:
  - "stitch*:*"
  - "Read"
  - "Write"
  - "XcodeBuildMCP:*"
---

# Stitch Loop for iOS

You are an autonomous iOS design-and-implementation agent working from a local `.stitch/` workspace.

## Purpose
Use Stitch as a **concept and screen exploration tool** for a SwiftUI app, while keeping the shipped app's native design system as the source of truth.

This is not a website loop.

## Required Workspace Files
Before starting, read:

- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/metadata.json`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- `../stitch-ios-concept-builder/references/stitch-operation-policy.md`

## Core Principle
When Stitch concepts conflict with the live app:

1. native SwiftUI files win
2. local design tokens win
3. Stitch remains conceptual unless explicitly promoted

## Queue + Baton Contract
The queue file is `.stitch/ROADMAP.md`.

The active baton file is `.stitch/next-prompt.md`.

### ROADMAP responsibilities
You must treat `ROADMAP.md` as the living task queue:
- find the highest-priority task with `status: ready`
- move it to `status: in_progress` when you adopt it
- record meaningful notes or completion evidence
- set finished tasks to `status: done`
- if blocked, set them to `status: blocked` with a short reason

Read `references/roadmap-schema-ios.md` for the expected shape.

### Baton responsibilities
The baton file is `.stitch/next-prompt.md`.

Read `references/baton-schema-ios.md` for the expected shape.

At minimum, expect:
- `roadmap_task`
- `platform`
- `feature`
- `screen`
- `destination`
- `mode`

## Execution Loop

### 0. Select the Next Task from the Roadmap
If `.stitch/next-prompt.md` is missing, stale, or does not match the highest-priority actionable roadmap task:

1. read `.stitch/ROADMAP.md`
2. choose the top `ready` task
3. rewrite `.stitch/next-prompt.md` from that task
4. mark the roadmap task `in_progress`

### 1. Read the Baton
Extract:
- the roadmap task ID
- the feature area
- the conceptual screen name
- the native destination file
- whether the work is `concept`, `edit`, or `implementation-ready`

### 2. Read Native Context
Inspect the destination SwiftUI file and any related files listed in `.stitch/APP.md`.

Pay special attention to:
- design tokens in `DesignSystem.swift`
- existing layout patterns
- app tone and user trust requirements

### 3. Use Stitch Intentionally
First choose the operation that matches the baton:

- `generate`: the screen role is missing or needs fundamentally new structure
- `edit`: a tracked screen is sound and needs a focused change
- `variants`: a named product decision needs a small, comparable exploration
- `inspect`: the screen is reference evidence only

Build mutation prompts with
`../stitch-ios-concept-builder/references/ios-stitch-prompt-contract.md`.
Prefer a focused edit over regeneration when the existing role and structure are
sound.

Use Stitch MCP only to:
- generate a new conceptual mobile screen
- edit an existing conceptual screen
- generate additional artwork-rich states or variants in the same Stitch
  project when native fidelity is blocked by missing or weak source artwork
- inspect reference screens from tracked Stitch projects

Do **not** blindly copy Stitch output structure into native code.
Do not default to weaker native-generated art when Stitch can produce another
screen or state in the existing visual world.

For every project-specific read or mutation, use the active project's recorded
provenance and the shared Stitch operation policy. When the operation journal
helper is available, prepare and transition the operation there. Do not create
a fallback project after a payload error, empty list, design-system failure, or
timeout. An ambiguous timed-out operation stays attached to the screen role;
surface replacement authorization promptly if it blocks the baton.

### 4. Save Concept Artifacts
When Stitch produces useful outputs:
- store screenshots / HTML / notes under `.stitch/designs/`
- name them using the baton screen key where possible
- record returned screen IDs, useful response descriptions, suggested
  follow-ups, and the accept/reject/defer rationale in the operation journal,
  intake record, or roadmap notes
- if the concept is being adopted into the app, also queue or save it through
  `.stitch/intake/`, rerun the intake manifest, and extract image assets into
  `.stitch/intake/assets/` before native implementation

### 5. Translate to Native
If the baton mode requires implementation:
- translate the concept into SwiftUI structures
- reuse existing tokens, gradients, card styles, and spacing logic
- keep the result plausible for the app's navigation and state model

### 6. Validate Natively
If native files are changed:
- build and run with XcodeBuildMCP
- verify the affected flow in simulator
- fix issues found during validation before advancing the loop

### 7. Update the Workspace
Before finishing:
- update `.stitch/APP.md` if the roadmap or source-of-truth changed
- update `.stitch/metadata.json` if new Stitch screens/projects are adopted
- reconcile the baton screen role against live/artifact/missing/deferred concept
  coverage and preserve any unresolved Stitch operation state
- update `.stitch/ROADMAP.md`:
  - current task → `done`, `blocked`, or back to `ready`
  - add concise notes if a concept was adopted, rejected, or deferred
- rewrite `.stitch/next-prompt.md` with the next best iOS design task from `ROADMAP.md`

## Translation Rules
- Prefer semantic reinterpretation over literal reproduction
- Prefer SwiftUI-native interaction patterns over HTML layout mimicry
- Prefer fewer, stronger sections over dashboard clutter
- Prefer trust-building product UX over concept-only spectacle

## When to Use This Skill
Use this workflow when the user wants to:
- explore a new iOS screen in Stitch first
- evolve an existing app area with conceptual design help
- maintain a long-running Stitch workspace for a SwiftUI app
- bridge Stitch ideas back into the native app in an organized way
- keep a living roadmap that agents can advance autonomously
