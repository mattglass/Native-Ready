# iOS App Director Toolchain Map

## Native app layer
- SwiftUI implementation
- local design tokens
- on-device state and feature logic

## Validation layer
- XcodeBuildMCP for build, run, logs, screenshots, and simulator verification

## Concept / design layer
- Stitch for concept generation and design exploration
- `.stitch/` workspace for local design memory

## Service layer
- Cloudflare Workers / APIs for production endpoints, orchestration, and app data flows

## Memory layer
- `AGENTS.md`
- `docs/app-build-spec.md`
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/ROADMAP.md`
- `.stitch/next-prompt.md`

## Loop rule
Always prefer validated runtime truth over assumptions.
