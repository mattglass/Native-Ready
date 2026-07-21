# iOS Roadmap Schema

The roadmap lives at `.stitch/ROADMAP.md`.

It is the **queue** for the Stitch-to-iOS loop.

## Task Format

Each task should use a dedicated markdown section:

```md
## Task STITCH-IOS-001
- status: ready
- priority: high
- feature: ai-coach
- screen: coach-check-in
- mode: concept
- destination: `LauricidinApp/Views/AICompanionView.swift`
- stitch_project: `9431272072017980542`
- references:
  - `AI Personal Health Coach / AI Companion`
- summary: Create a guided coach check-in concept.
- success_criteria:
  - Introduces a low-friction check-in interaction
  - Gives one clear next-best action
```

## Required Fields

| Field | Purpose |
|---|---|
| `status` | `ready`, `in_progress`, `blocked`, `done`, or `icebox` |
| `priority` | task urgency |
| `feature` | app feature area |
| `screen` | stable screen/concept key |
| `mode` | `concept`, `edit`, or `implementation-ready` |
| `destination` | likely native destination file |
| `summary` | one-sentence intent |

## Agent Rules

When running the loop:

1. choose the highest-priority `ready` task
2. mark it `in_progress`
3. generate `.stitch/next-prompt.md` from it
4. execute the work
5. mark it:
   - `done` if completed
   - `blocked` if progress cannot continue
   - `ready` again if intentionally deferred

## Notes Discipline

If you change a task status, add a concise note when useful:
- what was explored
- what was implemented
- why it was blocked
- whether the concept was adopted or rejected
