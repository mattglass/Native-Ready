# iOS Baton Schema

The iOS Stitch baton lives at `.stitch/next-prompt.md`.

## Recommended Format

```yaml
---
platform: ios
roadmap_task: STITCH-IOS-001
feature: ai-coach
screen: coach-check-in
destination: LauricidinApp/Views/AICompanionView.swift
mode: concept
stitch_project: "9431272072017980542"
device: MOBILE
---
<prompt body>
```

## Fields

| Field | Required | Purpose |
|---|---|---|
| `platform` | yes | Should be `ios` |
| `roadmap_task` | yes | Task ID from `.stitch/ROADMAP.md` |
| `feature` | yes | App feature area (`cart`, `rewards`, `ai-coach`, etc.) |
| `screen` | yes | Stable conceptual screen key |
| `destination` | yes | Native file most likely to receive the concept |
| `mode` | yes | `concept`, `edit`, or `implementation-ready` |
| `stitch_project` | optional | Preferred project ID for concept exploration |
| `device` | optional | Usually `MOBILE` |

## Prompt Body Requirements
The markdown body should include:

1. a one-line summary of the desired screen
2. a source-of-truth reminder pointing back to `.stitch/DESIGN.md`
3. concrete goals
4. a proposed screen structure
5. explicit "do not" constraints if needed

## Important Difference from Website Loop
This baton does **not** target HTML output filenames.

Instead, it targets:
- a feature area
- a native destination file
- a concept-to-SwiftUI translation path
