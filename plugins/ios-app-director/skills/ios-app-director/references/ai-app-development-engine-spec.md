# AI-Assisted App Development Engine Spec

## Purpose

This document defines a repeatable system for building production-ready apps with an AI coding agent operating inside a tool-rich development environment.

The system combines:

- Codex / agent logic for planning, coding, refactoring, and debugging
- XcodeBuildMCP for build-run-verify loops
- Stitch workflows for concept generation and UI direction
- Cloudflare Workers / APIs for production endpoints, orchestration, and app data services
- repo-local memory such as `.stitch/`, roadmap files, and project instructions
- live debug cycles that improve the product and the workflow over time

This is an agent workflow specification, not an independent runtime. Codex
interprets these instructions, maintains repo-local state, and invokes
configured tools to perform the work.

---

## Core Idea

The agent should not act like a one-shot code generator.

It should behave like a persistent product-building operator that can:

1. understand the app goal
2. establish local working memory
3. generate or refine design direction
4. implement native features
5. build and validate the app
6. connect production services and APIs
7. debug real behavior
8. update the roadmap and continue

The result is a loop that can keep moving from concept to implementation to validation with much less manual orchestration.

---

## System Components

## 1. Agent Logic

The coding agent is responsible for:

- planning next actions
- reading and updating repo instructions
- writing and editing code
- tracing bugs
- refactoring incrementally
- validating live behavior
- updating project memory
- choosing the next best task when enough context exists

The agent should prefer:

- small, composable changes
- persistent local documentation
- explicit task state
- validation before claiming completion

---

## 2. Native Build + Validation Loop

For Apple-platform apps, `XcodeBuildMCP` is the primary validation system.

Use it to:

- discover project/workspace configuration
- confirm session defaults
- build and run on simulator
- inspect logs
- capture screenshots
- inspect UI hierarchy
- iterate quickly during debug cycles

### Required behavior

- confirm defaults before the first build/test/run in a session
- use build-run loops instead of analysis-only conclusions
- verify the actual feature in simulator when practical
- treat successful build as necessary but not sufficient

---

## 3. Stitch Design System

Stitch is used as a **concept and design-direction engine**, not as a blind source of UI truth.

Use Stitch to:

- explore new screen concepts
- refine information hierarchy
- test alternate layouts
- generate conceptual references for future native screens
- synthesize local design-system memory

Stitch outputs should be treated as:

- concept artifacts
- layout inspiration
- design references

They should not be copied literally into native code without interpretation.

### Local Stitch memory

The repo should maintain a `.stitch/` workspace:

- `.stitch/APP.md` — app framing and source-of-truth rules
- `.stitch/DESIGN.md` — semantic design system
- `.stitch/ROADMAP.md` — living queue of design / implementation tasks
- `.stitch/next-prompt.md` — current baton
- `.stitch/metadata.json` — project IDs, screen IDs, mappings
- `.stitch/designs/` — saved concept artifacts
- `.stitch/prompts/` — reusable prompt fragments if needed

---

## 4. Cloudflare Services Layer

Cloudflare Workers and related services provide the production-capable backend layer for modern apps in this system.

Use Cloudflare for:

- app endpoints
- API orchestration
- proxy layers
- auth-related flows
- edge business logic
- data shaping for app clients
- webhook handling
- service integration
- scheduled jobs

Depending on the app, this may also include:

- Durable Objects
- KV / D1 / R2
- queues
- AI services
- Workers-based MCP integrations

### Principle

The app and the backend should be developed as one system.

The agent should be able to:

- update app UI
- update backend endpoints
- test data flows
- debug both sides
- keep the roadmap current across both surfaces

---

## 5. Repo-Local Memory

Persistent local memory is what allows the system to continue across sessions.

Important files may include:

- `AGENTS.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- feature build specs in `docs/`
- architecture notes
- API notes
- environment setup docs

### Why this matters

Without local memory, every new session starts cold.

With local memory, a new agent can quickly recover:

- app purpose
- current design language
- product priorities
- active backlog
- source-of-truth rules
- service architecture
- known constraints

---

## 6. Live Debug Cycle

A defining part of this system is the debug loop.

The agent should:

1. inspect the code
2. reproduce the issue
3. patch the implementation
4. rebuild and rerun
5. inspect logs or UI state
6. verify the fix end to end
7. update docs / roadmap / notes

This loop should continue until the issue is:

- clearly solved, or
- clearly explained with evidence

The system gets better as these debug loops accumulate because the agent builds stronger working knowledge of:

- the stack
- the product
- recurring failure modes
- validation shortcuts
- design patterns

---

## Source-of-Truth Hierarchy

When instructions conflict, prefer this order:

1. repo-level project instructions
2. current working implementation
3. explicit product goals
4. local design-system docs
5. roadmap state
6. conceptual design references

For UI work:

1. live app implementation wins
2. local design tokens win
3. Stitch concepts are subordinate unless promoted

For feature work:

1. verified runtime behavior wins over assumptions
2. successful validation wins over theoretical correctness

---

## Operating Loop

## Stage 1: Intake

At the start of a new app or major product surface, the agent should gather:

- app name
- platform(s)
- app purpose
- primary user
- key jobs-to-be-done
- must-have features
- design references
- existing app or brand examples
- preferred Stitch project(s), if any
- expected backend / API needs
- preferred launch scope

If information is missing, the agent should ask a few focused questions, not a huge survey.

---

## Stage 2: Bootstrap the Repo

`ios-app-bootstrap` is the single public setup entry point. It owns the run
through persistent operating files, design evidence, native project creation,
first simulator build/launch, baton validation, and the bootstrap receipt. It
may delegate design-first phases internally, but users should not have to
choose between competing setup entry points.

The agent should create or verify:

- `AGENTS.md`
- local instruction files
- `.stitch/` workspace if Stitch will be used
- feature specs in `docs/`
- environment / service config notes
- roadmap files
- an app-specific native SwiftUI Xcode project
- first scheme-discovery and simulator build/launch evidence
- `docs/bootstrap-receipt.md`

The goal is to make the repo legible and runnable for future sessions. Stop
after the receipt unless the user's active request also authorizes delivery.

---

## Stage 3: Establish Product Memory

Create and maintain:

- app framing in `.stitch/APP.md`
- design guidance in `.stitch/DESIGN.md`
- feature queue in `.stitch/ROADMAP.md`
- active task baton in `.stitch/next-prompt.md`
- integration metadata in `.stitch/metadata.json`

This allows the system to move from one task to the next without losing context.

---

## Stage 4: Design Exploration

When a feature benefits from conceptual UI work:

1. choose a roadmap item
2. write or refresh the baton
3. inspect native context
4. use Stitch for concept generation or editing
5. save artifacts locally
6. decide whether to:
   - keep concept-only
   - convert into native implementation
   - defer

---

## Stage 5: Native Implementation

When work moves into code:

1. inspect the destination files
2. implement incrementally
3. preserve the current architecture unless intentionally changing it
4. reuse design tokens and existing patterns
5. keep code organized by feature when possible

Do not let conceptual design work bypass implementation discipline.

---

## Stage 6: Backend / Services Implementation

When a feature needs remote behavior:

1. define the app-facing contract
2. implement or update the Cloudflare Worker / endpoint
3. wire the native app to the contract
4. test the real data flow
5. capture any new operational knowledge in docs

The agent should think in terms of end-to-end feature completion, not isolated frontend or backend work.

---

## Stage 7: Validation

Validate every meaningful feature through the relevant loop:

- build
- run
- inspect
- test
- debug
- retest

For iOS:

- confirm XcodeBuildMCP defaults
- build and run on simulator
- inspect logs
- verify the changed flow manually where practical

For backend changes:

- hit the real or local endpoint
- inspect status codes and payloads
- verify the app consumes the response correctly

---

## Stage 8: Memory Update + Advancement

After completing or pausing work:

- update the roadmap status
- add concise notes
- refresh the baton
- capture any changed source-of-truth rules
- document architecture decisions if they matter

The loop should end in a better state than it started.

---

## Roadmap-Driven Development

The roadmap should be a living document, not a dead checklist.

Each task should ideally include:

- task ID
- status
- priority
- feature
- screen or surface
- destination file or module
- mode
- summary
- success criteria
- notes

### Suggested statuses

- `ready`
- `in_progress`
- `blocked`
- `done`
- `icebox`

### Loop behavior

The agent should be able to:

1. select the highest-priority actionable task
2. rewrite the baton from that task
3. execute the work
4. validate it
5. update the task state
6. choose the next task

This is what makes the roadmap a true operational queue.

---

## Stitch-to-Native Translation Rules

When turning concepts into app code:

- translate semantics, not screenshots
- preserve the app's own tone
- prefer native interaction models
- keep implementation plausible
- avoid generic AI-dashboard patterns
- avoid fabricated metrics
- avoid web-layout cargo-culting in native apps

The best concepts improve:

- trust
- clarity
- momentum
- hierarchy
- usability

Not just aesthetics.

---

## Agent Behavior Rules

The agent should:

- prefer execution over vague discussion
- patch files when needed
- validate claims
- update project memory
- make reasonable assumptions when low-risk
- ask only the most important missing questions

The agent should not:

- stop at analysis when it can test
- treat generated design as automatically correct
- make broad architectural changes without saying so
- claim a feature works without validation
- lose track of roadmap state

---

## New App Kickoff Questionnaire

A fresh agent instance should ask only a few focused questions like:

1. What is the app called, and what is its primary purpose?
2. What platform are we building first?
3. What are the first 3–5 must-have features?
4. Do you already have a Stitch project, design references, or example apps?
5. Will the app need a backend or app-specific endpoints? If yes, what kind?

Optional follow-up questions:

- What brand or visual tone should it follow?
- What existing repo or starter code should be reused?
- What launch scope matters most: prototype, internal test, or production-ready build?

---

## New Project Bootstrap Checklist

For a new app repo, the agent should aim to establish:

- repo instructions
- platform/build setup
- roadmap
- design workspace
- backend/service strategy
- validation path

### Minimum bootstrap artifacts

- `AGENTS.md`
- `docs/app-build-spec.md`
- `.stitch/APP.md` if Stitch is in scope
- `.stitch/DESIGN.md`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`
- `.stitch/metadata.json`
- backend notes if services are required
- app-specific native SwiftUI Xcode project
- first scheme-discovery and simulator build/launch result
- `docs/bootstrap-receipt.md`

The receipt reports setup state and remaining risks; it is not a gate. Optional
Stitch, Cloudflare, or evidence gaps should remain visible without blocking an
independent native scaffold. The active baton must point to the best
dependency-safe executable task rather than an optional timed-out operation.

---

## Recommended Execution Formula

This is the high-level algorithm:

1. understand the product
2. establish local memory
3. create or refine design direction
4. choose the top roadmap task
5. generate concept support if needed
6. implement natively
7. wire backend behavior if needed
8. build, run, and debug
9. verify the feature end to end
10. update memory and roadmap
11. write the next baton
12. continue

---

## What Makes This a Real System

This system becomes powerful when all of these are present together:

- persistent instructions
- tool-connected execution
- roadmap-driven next-step selection
- design memory
- backend integration
- live validation
- iterative debugging

Without those pieces, AI coding stays ad hoc.

With them, the agent starts behaving more like a product development engine.

---

## Copy/Paste Kickoff Prompt For a Fresh Agent

Use or adapt this when starting a new app:

```md
Use this repo as the working base for a roadmap-driven AI app development system.

Your job is to help bootstrap and build a production-capable app using:
- native app implementation
- local project memory
- Stitch concept workflows where useful
- backend/services support where needed
- strict validation loops before claiming completion

Please do the following:
1. inspect the repo and infer the current state
2. ask only the most important missing product questions
3. establish or refine repo-local memory and roadmap files
4. identify the highest-value first build target
5. move into implementation/debug mode once enough context exists

When design work is needed, use Stitch conceptually, not as blind UI truth.
When backend work is needed, design app-facing contracts and implement the service layer.
When native work is changed, validate with the appropriate build/run loop.

Always leave the repo in a more operational state:
- clearer instructions
- clearer roadmap
- clearer source-of-truth rules
- validated progress
```

---

## Success Condition

This system is working when a new coding agent can enter the repo, read the local memory, ask a few smart questions, and then move into productive build mode with minimal handholding.
