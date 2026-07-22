# Orchestration Policy

## Purpose
Keep `ios-app-director` reliable, repeatable, and architecture-aware while still allowing autonomous progress.

## Core operating rules
1. Prefer the repo's existing source-of-truth hierarchy over assumptions.
2. Prefer finishing or stabilizing the current baton before inventing new work.
3. Prefer the smallest coherent implementation slice that materially improves the product.
4. Prefer reusable seams over one-off hacks when the same concern will likely appear in multiple features.
5. Do not widen scope unless product goals, runtime findings, or dependencies justify it.
6. Keep fragile external mutations deterministic without narrowing creative or
   product judgment. For Stitch, preserve one active project identity,
   provenance for project-specific calls, truthful result state, and explicit
   ambiguous-timeout recovery.

## Work-mode selection
### Bootstrap mode
Use when the repo lacks the core local operating files: `AGENTS.md`, `docs/app-build-spec.md`, or roadmap/baton files.

### Delivery mode
Use when the repo has working memory and the next best step can be selected from the roadmap.

### Recovery mode
Use when roadmap, baton, docs, or implementation drift enough that normal delivery would compound confusion.

## Task selection policy
Choose work in this order:
1. active `in_progress` baton that still makes sense
2. highest-priority `ready` task whose dependencies are satisfied
3. split task when the current task mixes too many surfaces or concerns
4. new task only when no existing task responsibly captures the next best move

## When to create a new task
A new task is justified only when one or more of these are true:
- a product goal in `APP.md` is underrepresented in the roadmap
- runtime validation exposed a meaningful gap or new dependency
- a completed task unlocked a natural successor
- a design or service decision introduced a clear next implementation unit
- a production-readiness need has become timely for the app's maturity

When you create a new task, record:
- why now
- what unlocked it
- any dependency relationship
- whether it is feature, integration, debug, or readiness work

## Task splitting policy
Split a task when it:
- spans multiple unrelated modes (for example native UI + backend + analytics)
- cannot be validated coherently in one loop
- would produce weak roadmap notes because too much changed at once
- hides a dependency that should be explicit

In prototype and early dogfood, "smallest coherent" can still be a multi-screen
vertical slice when the user experience needs it. Do not split design identity,
primary interaction, and the first success state into separate tiny tasks if the
result would make the app feel generic or impossible to judge.

## Architecture coherence rules
Before adding state, service seams, or feature structure, ask:
- will another feature likely need this soon?
- is this a product-level concern or a one-screen concern?
- does this preserve the repo's current architecture unless a change is intentional?
- is this the lightest structure that still supports future work?

## Stop conditions
Pause and recover before continuing when:
- the roadmap contradicts the implementation
- the baton points at the wrong next step
- validation failed and the issue is not understood
- a new task would be guesswork rather than justified planning

An optional or out-of-scope MCP startup failure is not a stop condition. Record
and ignore it unless current product scope requires that capability.

An ambiguous Stitch timeout blocks only its dependent task chain. Continue
other dependency-safe work, but run configured autonomous recovery as soon as
the prescribed polling budget is exhausted instead of waiting for roadmap
exhaustion. Ask the user only when recovery mode is manual, the bounded attempt
is exhausted, or the remaining choice changes product intent.
