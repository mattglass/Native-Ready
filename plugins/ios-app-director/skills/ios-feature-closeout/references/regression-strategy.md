# Regression Strategy

## Purpose
Scale regression checks to the blast radius of the change instead of treating every task the same.

## Regression scope values
- `none`
- `local`
- `adjacent`
- `feature_family`
- `critical_path`

## Choosing scope
### none
Use only when the task is documentation-only or purely conceptual with no downstream change risk.

### local
Use when the change is isolated to one screen or one interaction path.

### adjacent
Use when the change may affect nearby screens, shared components, or navigation into/out of the changed flow.

### feature_family
Use when the change affects shared state, service seams, reusable components, or multiple screens in the same feature area.

### critical_path
Use when the change affects high-trust flows, app-wide navigation, authentication, checkout/orders, dosing, rewards, or other product-critical paths.

## Mandatory checks by scope
### local
- retest the changed flow

### adjacent
- retest the changed flow
- spot-check one upstream or downstream adjacent flow

### feature_family
- retest the changed flow
- retest at least one other surface using the same seam or state
- verify persistence/integration if relevant

### critical_path
- retest the changed flow
- retest adjacent and sibling trust flows
- verify persistence and integration when relevant
- note remaining risk explicitly if broad verification is incomplete

## Task creation rule
If the required regression scope is too large for the active task, split out a regression or hardening follow-up task instead of pretending it was covered.
