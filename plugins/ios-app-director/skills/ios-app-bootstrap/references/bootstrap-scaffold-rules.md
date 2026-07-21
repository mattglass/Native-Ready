# Bootstrap Scaffold Rules

## Purpose
Ensure a newly bootstrapped repo starts with maturity-aware, evidence-aware, and regression-aware operating files.

## A bootstrap should establish
- repo instructions
- product brief
- `.stitch/APP.md`
- `.stitch/DESIGN.md`
- `.stitch/ROADMAP.md` using the current task template
- `.stitch/next-prompt.md` using baton schema
- `.stitch/metadata.json` including schema markers, app maturity, and evidence structures
- `docs/definition-of-done.md` aligned with the current closeout rules
- an app-specific native Xcode project and source root
- an app-derived planned test target
- a first XcodeBuildMCP scheme-discovery and simulator build/launch result
- `docs/bootstrap-receipt.md`

## First roadmap task rules
The first task should be:
- concrete
- dependency-safe
- easy to validate
- small enough to produce a believable first loop
- tagged with app maturity and evidence expectation

## First baton rules
The first baton should:
- point to exactly one active task
- include validation tier, app maturity, and evidence expectation
- explain non-goals so the first loop stays focused
- point to the best dependency-safe executable task rather than an optional timed-out operation

## Completion rule

Memory-only output is not complete bootstrap. Create the native scaffold, attempt
the first simulator build/launch, validate the active baton, and render the
non-blocking receipt. Stop after the receipt unless the user also authorized
product-feature delivery.

Missing optional Stitch or Cloudflare capabilities produce explicit degraded or
partial status; they do not block independent native scaffolding.

## Default maturity rule
If the user does not specify otherwise, bootstrap the repo at `prototype` maturity.
