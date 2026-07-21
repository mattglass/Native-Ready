# Validation Ladder

## Purpose
Choose the right validation depth for the task instead of treating every task the same.

## Tiers
### Tier 1 — Compile
- the project builds successfully

### Tier 2 — Launch
- the app launches on the intended simulator/device

### Tier 3 — Interaction
- the changed feature flow is manually exercised

### Tier 4 — Persistence / continuity
- relaunch, navigation continuity, or shared-state survival is verified when relevant

### Tier 5 — Integration
- service or backend path is exercised at the intended maturity level

### Tier 6 — Regression confidence
- nearby surfaces or adjacent flows are spot-checked when the change has meaningful blast radius

## Recommended minimums by task type
- native feature: Tiers 1-3
- native feature with persisted/shared state: Tiers 1-4
- service task with local/dev or live path: Tiers 1-2 and 5
- integration task: Tiers 1-3 and 5
- debug fix: Tiers 1-3, plus 4/5/6 when relevant
- production-readiness task: use the tier that best proves the claimed improvement

## Evidence expectations
Roadmap notes should say enough to answer:
- what was validated
- how deep validation went
- what still remains unverified

## Simulator UI automation notes

- Runtime UI element refs expire. After `build_run_sim`, a navigation action, or
  any failed tap/swipe, refresh with `snapshot_ui` before reusing refs.
- A build/run plus home snapshot does not prove a nested detail, modal,
  persistence, or visual parity claim. Navigate to the claimed state and capture
  evidence there.
- For exact or prototype-gate visual parity, capture the first viewport and the
  main scrolled content sections, not only one screenshot.
