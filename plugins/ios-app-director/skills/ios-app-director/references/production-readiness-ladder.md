# Production Readiness Ladder

## Purpose
Give the engine a way to contemplate release quality without overloading early prototype work.

## Stages
### Stage 1 — Prototype
Focus on believable UX, service seams, and basic validation.

### Stage 2 — Dogfood / internal testing
Start tightening:
- state persistence
- error feedback
- core flow reliability
- local integration paths

### Stage 3 — Beta / active tester phase
Start adding or prioritizing tasks around:
- regression confidence
- analytics or event instrumentation
- performance hotspots
- memory or lifecycle issues
- sharper service integration behavior

### Stage 4 — Release candidate
Prioritize:
- error-state completeness
- environment/config hardening
- observability
- crash-risk reduction
- flow polish and readiness gaps

### Stage 5 — Production maturity
Prioritize:
- service resilience
- release discipline
- stronger readiness evidence
- long-tail UX reliability

## Engine behavior
The engine should not front-load all readiness work.
It should introduce readiness tasks when the app's maturity and product goals justify them.

When a user asks to build autonomously toward a production-ready v1 from a fresh
prototype, treat that as the long-range objective, not permission to skip
prototype and dogfood gates. Build the product spine first:
- native scaffold and memory coherence
- design-first visual identity
- core feature loops
- prototype visual exit gate
- persistence and local reliability
- beta/release hardening only after those gates are satisfied

Do not create App Store, release-candidate, or submission-readiness tasks while
core Stitch-backed screens are still visually generic or parity-unproven unless
the user explicitly chooses that tradeoff.
