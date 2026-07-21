# Service Maturity Model

## Purpose
Evolve backend and integration work deliberately instead of jumping from placeholder UI to production assumptions.

## Levels
### Level 0 — UI placeholder
The app implies future remote behavior but no contract exists yet.

### Level 1 — App-facing contract
The native app has request/response models or protocol seams.

### Level 2 — Service client
The app can call a service abstraction or client layer.

### Level 3 — Local/dev path
A local stub, Worker dev path, or prototype backend route is exercised by the app.

### Level 4 — Integrated backend
A real backend or remote integration is connected for the intended flow.

### Level 5 — Production-ready service
Environment handling, error paths, observability, deployment assumptions, and operational expectations are clear enough for serious release use.

## Advancement rules
- Move one maturity step at a time unless the user clearly wants a deeper jump now.
- Record the current maturity level in task notes when it matters.
- Do not pretend a Level 2 or Level 3 seam is production integration.
- Prefer app-owned contracts before vendor-specific complexity leaks into the UI.
