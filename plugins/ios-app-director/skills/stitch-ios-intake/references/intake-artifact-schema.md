# Intake Artifact Schema

Use this shape for `.stitch/intake/design-intake.md`.

```md
# [APP_NAME] Design Intake

## Product Seed
- app:
- purpose:
- target user:
- platform:
- maturity:
- backend needed now:
- cloudflare needed now:

## Source Artifacts
- Stitch project:
- Google Doc:
- screenshots:
- image assets:
- intake manifest:
- image asset manifest:
- artifact sources:
- notes:

## Stitch Project
- project id:
- title:
- device type:
- update time:
- design system:

## Stitch Operation State
- journal:
- active mutation project:
- unresolved operation ids:
- recovery state:

## Screen Inventory
| Key | Title | Screen ID | Device | Role | Confidence |
| --- | --- | --- | --- | --- | --- |
| welcome | Welcome | ... | mobile | onboarding entry | high |

## Concept Coverage
| Role | Required | Status | Live Screen IDs | Artifact Paths | Linked Task | Note |
| --- | --- | --- | --- | --- | --- | --- |
| onboarding entry | yes | live | ... | ... | ... | ... |

## Intake Manifest
- json:
- markdown:
- source log:
- pending queue:
- screenshots:
- assets:
- html:
- records:
- generated at:

## Image Asset Manifest
- json:
- markdown:
- assets directory:
- product-critical candidates:
- source/provenance notes:

## Design System Signals
- design document:
- evidence sources:
- confidence:
- observed rules:
- proposed rules:
- visual tone:
- colors:
- typography:
- component patterns:
- component states:
- artwork and motifs:
- motion and reduced-motion behavior:
- navigation patterns:
- content voice:

## Visible Feature Clues
Group by screen. Capture only what is visible or directly stated.

## Implied Product Requirements
Capture likely requirements separately from visible facts.

## Data, Service, And AI Clues
Name data needs, cloud needs, AI surfaces, and integration assumptions.

## Safety, Privacy, And Claims
Flag unsupported compliance claims, sensitive data flows, medical/legal/financial risk, auth, consent, retention, deletion, and escalation needs.

## Open Questions
Ask only questions that block feature-map synthesis or first-roadmap generation.
```
