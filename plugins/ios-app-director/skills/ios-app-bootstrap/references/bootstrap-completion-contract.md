# Bootstrap Completion Contract

## Purpose

Make READY bootstrap produce the same minimum outcome in Codex and Codex CLI without turning optional design or service gaps into false blockers.

## Required phases

1. Environment preflight
2. Product and repository identity
3. Design evidence or an explicitly degraded design path
4. Feature map, roadmap, metadata, and baton
5. Native SwiftUI Xcode scaffold
6. Scheme discovery and first simulator build/launch attempt
7. Bootstrap receipt

Bootstrap may delegate these phases to other READY skills, but `ios-app-bootstrap` remains the public entry point and owns the final outcome.

## Completion states

### `ready_for_delivery`

- the receipt records `toolchain_status: supported` for Xcode 16 or newer
- the native `.xcodeproj` or `.xcworkspace` exists
- target, module, scheme, source root, and bundle identifier are recorded
- XcodeBuildMCP discovered the scheme
- the first simulator build/launch succeeded
- the active baton validates and points to a dependency-safe delivery task
- the receipt records the result

### `partial`

Use when setup made meaningful progress but one or more checks remain incomplete, such as:

- Stitch is unavailable but the native scaffold and build can proceed
- Stitch reports `api_key_required` and is optional, with the secure setup and restart action recorded
- a non-critical Stitch screen or report timed out
- build tooling exists but launch evidence could not be captured
- a required signing or distribution identity decision is pending for device or release work

Keep independent phases moving. Put the unresolved item in the risk register or a dependency-correct roadmap task.

### `blocked`

Use only when a concrete condition prevents meaningful continuation, such as:

- Xcode or the required SDK/runtime is unavailable
- Xcode is older than 16 and is classified as `unsupported_toolchain`
- XcodeBuildMCP cannot be started or used after recovery attempts
- the native scaffold cannot be generated or repaired
- a required user product decision changes project identity or architecture

Do not classify optional Cloudflare access, an optional Stitch role, or receipt rendering as a bootstrap blocker.

## Baton invariant

The active baton must always represent the best dependency-safe executable task. A timed-out or missing optional operation may remain visible in the roadmap and receipt, but it must not replace an executable native task.

## Bounded concept acceptance

For each required core concept role:

1. inspect the first result
2. identify concrete hierarchy, clipping, overflow, fidelity, or product-identity defects
3. make at most two corrective edit/variant attempts during bootstrap
4. retain the strongest usable artifact
5. record remaining gaps for delivery

The bounded loop improves weak concepts without making perfect Stitch output a prerequisite for native scaffolding.

## Receipt behavior

`docs/bootstrap-receipt.md` is a generated status report, not a validator. It must render even when metadata or evidence is incomplete and must list unknown or missing fields explicitly. A failed receipt field creates remediation work; it does not erase completed setup work.

The receipt must distinguish a successful build from a successful launch. A simulator boot spinner, installed app bundle, or booted device is failure/diagnostic evidence until the app process or visible app UI is verified.

## Delivery boundary

Bootstrap stops after the first validated app launch and receipt unless the user also requested implementation or activated a delivery goal. The recommended next prompt is:

```text
/goal Build autonomously toward the v1 app until the planned features work, the roadmap is reconciled, validation evidence is captured, and the app is ready for real user testing.

Use $ios-app-director to continue from the active baton.
```
