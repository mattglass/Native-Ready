# iOS Concept Screen Set Blueprint

Use this to plan the first Stitch screen set from bootstrap answers.

## Default Screen Set

### 1. Welcome / Value Proposition
- app identity
- user promise
- primary CTA
- secondary learn-more or skip action
- trust cue appropriate to domain
- distinctive hero artwork or object focus that establishes the app's visual world

### 2. First Personalization Step
- focus areas, categories, preferences, or intent
- multi-select or single-select
- selected and unselected states
- continue/back affordances
- visual treatment for selected states, badges, chips, or cards

### 3. Goals Or Setup Details
- user goals or desired outcomes
- progress indicator when part of onboarding
- explanation of how choices affect the app
- tone-specific microcopy and visual motif

### 4. Trust, Safety, Or Grown-Up / Admin Step
Use when the app involves kids, families, sensitive data, AI, finance, health,
education, safety, or any domain where trust is part of activation.
- safety or privacy promise
- grown-up/admin/owner guidance when relevant
- local vs cloud behavior when relevant
- permission or consent preview without dark patterns
- ready-to-start or first mission setup cue

### 5. Data, Sync, Or Manual Setup
Use when the app depends on data sources, accounts, cloud sync, integrations, documents, or imports.
- connect option
- manual setup fallback
- consent / privacy reassurance
- unsupported-service caveat if needed

### 6. Primary Daily-Use Home
- main navigation model
- first high-value action
- summary or dashboard
- reusable card/component system
- visual spine carried forward from onboarding

### 7. Primary Feature Screen
- core workflow from the first must-have feature
- realistic empty/loading/data states where useful
- clear destination for native implementation
- product-critical artwork, media, or object treatment when the concept depends on it

### 8. Secondary Feature Screen
- second daily-use workflow or supporting feature
- enough contrast to reveal navigation and data model needs

### 9. Reward, Completion, Or Feedback Moment
Use when the app has learning loops, creativity loops, habit loops, games,
creation flows, or achievements.
- completion state
- celebration or encouragement
- next action
- non-manipulative reward language
- visual treatment for badges, progress, or saved work

### 10. Profile / Settings / Privacy
Use for apps with accounts, preferences, sensitive data, AI, notifications, or connected services.
- user profile or preferences
- connected sources
- privacy and deletion controls
- notification/settings hooks

## Prompt Requirements

Build every Stitch generation, variant, or edit prompt with
the sibling `ios-stitch-prompt-contract.md`. At minimum, include:
- platform and device type
- target user
- product purpose
- screen role
- desired visual tone
- content density
- primary actions
- navigation assumptions
- sensitive-domain guardrails
- "make this feel like a production-quality native iOS app concept"

## Guardrails

- Do not show unsupported compliance logos or claims.
- Do not imply live services exist unless the user says they do.
- Prefer native iOS mental models over web dashboard structure.
- Prefer fewer strong screens over many shallow ones.
- Prefer a coherent onboarding arc over a lone welcome screen when activation
  depends on trust, personalization, learning, or family/grown-up context.
- Make screenshots analyzable: visible labels, realistic data examples, clear states, and navigation.
- Make artwork analyzable: if the product needs custom visuals, include hero
  images, content imagery, reward art, or component motifs that can be
  translated into native assets or drawing tasks.

## Expansion Screen Sets

When the app already has a Stitch project and native implementation reveals an
artwork gap, generate a smaller expansion set instead of a full new app set.
Good expansion sets include:
- the missing core screen state in context
- one or two content/art variants using the same design system
- a reward, empty, or result state when the gap affects a loop
- visible labels and realistic data so the feature map can distinguish content,
  requirements, and decoration

The goal is to improve native visual alignment by producing better reference
screens and extractable artwork, not to restart product planning.
