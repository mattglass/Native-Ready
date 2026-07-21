# Closeout Checklist

## Purpose
Turn changed code or concept work into a responsibly closed roadmap unit with evidence, regression, and risk discipline.

## Checklist
1. identify task type and app maturity
2. apply the right done criteria
3. validate to the required tier
4. satisfy the required regression scope
5. update roadmap notes with what changed, what was validated, and remaining risk
6. update baton to the next best task in current format
7. update metadata evidence when structured evidence matters
8. record or resolve meaningful risk
9. trigger an architecture review follow-up when shared coherence drift is visible
10. for design-translation work, update any affected `.stitch/screen-packets/`
    with adoption outcome, simulator evidence, and remaining visual gaps
11. before any prototype-complete, dogfood-ready, user-testing-ready, beta-ready,
    or exact-parity claim, run the prototype visual exit audit for core
    Stitch-backed screens; if any core screen remains `same_family_only`,
    `partially_adopted`, `generic_substitute`, or `parity_unproven`, inject or
    activate the smallest visual-spine task instead of promoting maturity
12. before writing a no-next-task handoff, audit `.stitch/APP.md`, design intake,
    metadata, risk, service maturity, and any new Stitch screen evidence for
    unmet buildable scope
13. run the maturity-transition audit; if closeout proves the current stage is
    coherent, promote the active maturity target and activate the smallest
    next-stage task instead of stopping
14. inject the smallest justified coherent task when those audits find a current-
    maturity or newly activated next-maturity gap; only pause when the remaining
    work is explicitly blocked, iceboxed behind an unsatisfied gate, or requires
    a product/maturity decision
15. for `stitch_art_expansion`, reconcile the operation journal and live/artifact
    evidence before closing; submitted, polling, and `ambiguous_timeout` are not
    completion states
16. ensure every required concept role used by the task is live, adequately
    artifact-only, or explicitly deferred; keep missing roles linked to an
    actionable expansion task and do not pass their dependent visual gates
