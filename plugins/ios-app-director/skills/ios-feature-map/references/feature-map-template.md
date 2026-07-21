# Feature Map Template

Use this template for `.stitch/APP.md` section 9.

```md
## 9. App Feature Inventory & Requirements Map

[APP_NAME] reads as [one-sentence product category] with [number] major experiences:

1. [Experience 1]
2. [Experience 2]
3. [Experience 3]
4. [Experience 4]

The visual direction is [tone summary]. The UX should communicate [trust/value summary].

### 1. Feature List By Screen

#### A. [Screen Name]

Visible features:
- [Visible feature]

Functional requirements:
- [Functional requirement]

Visual translation requirements:
- [Signature artwork, hero image, card treatment, color/motion/depth requirement]
- [Native asset or drawing strategy: saved Stitch source artwork / generated asset / bundled bitmap / native shape / deferred]
- [Source artwork candidate: `.stitch/intake/assets/[file]` or none]

Data requirements:
- [Data or persistence requirement]

Service / AI requirements:
- [Service requirement]

Safety / privacy / claims:
- [Risk or guardrail]

Native implementation hints:
- likely destination: `[path or feature area]`
- state owner:
- validation notes:

### 2. Navigation Structure

Current visible navigation:
- [Observation]

Recommended native navigation:
| Destination | Purpose | Notes |
| --- | --- | --- |
| [Tab/Route] | [Purpose] | [Notes] |

### 3. Core Feature Requirements Matrix

| Area | Requirement | Priority | Source | Maturity |
| --- | --- | --- | --- | --- |
| [Area] | [Requirement] | Critical/High/Medium/Low | visible/note/inferred | prototype/dogfood/beta |

### 4. Missing Or Implied Screens

Coverage roles come from the product requirements, not a fixed screen count.

| Role / Screen | Required | Coverage | Source / Provenance | Why | Next Action |
| --- | --- | --- | --- | --- | --- |
| [Role] | yes/no | live/artifact_only/missing/deferred/not_needed | [project + screen ID, artifact path, note, or inference] | [Why the role exists] | [none, revisit condition, or linked `stitch_art_expansion` task] |

Unresolved Stitch operations:
- [Operation ID]: [polling / ambiguous_timeout / replacement_authorized], linked role [role], next recovery action [action]

### 5. AI, Data, And Service Requirements

- AI capability:
- Data source:
- Service contract:
- Consent/auth/deletion:

### 6. Design And UX Observations

What is working:
- [Observation]

Areas to tighten:
- [Observation]

### 7. Visual Fidelity And Asset Plan

Product-critical visual signatures:
- [Artwork, motif, or composition that must survive native translation]

Asset strategy:
- [Use saved Stitch source artwork / native drawing / generated bitmap assets / cropped concept reference / SF Symbols only if sufficient]

Screens that need visual parity tasks:
- [Screen]: [why]

Visual fidelity gate before beta/release:
- [What simulator screenshots must be compared against which Stitch references]

### 8. Suggested Scope

MVP must-have:
- [Item]

Next release:
- [Item]

Later:
- [Item]

### 9. Quality-Control Notes

- Unsupported claims:
- Sensitive data:
- Regulatory/safety concerns:
- Open questions:
- Concept coverage gaps:
- Unresolved Stitch operations:

### 10. Product Requirement Summary

[Concise summary agents can use to choose roadmap tasks.]
```
