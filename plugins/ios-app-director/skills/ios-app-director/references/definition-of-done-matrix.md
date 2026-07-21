# Definition of Done Matrix

## Purpose
Different task types need different closeout standards.

## Native feature
Done when:
- the feature exists in the native app
- the changed flow builds and launches
- the primary interaction path was verified in Simulator
- relevant shared state or seams are coherent
- roadmap and baton notes reflect the real state

## Service task
Done when:
- the app-facing contract exists or was updated
- the current service maturity level is clear
- the implemented service path was exercised at the intended level
- docs capture important environment or integration assumptions
- the next maturity step is clearer than before

## Integration task
Done when:
- the client and remote seam are connected at the intended level
- success and failure states are represented clearly enough for the current phase
- the integrated path was validated end to end
- roadmap notes record any remaining maturity gaps

## Design-translation task
Done when:
- the design source was identified
- native interpretation is visible in code
- the output is not a literal copy of concept UI
- adoption outcome is recorded: adopted, partially adopted, deferred, or rejected
- the resulting screen was validated live
- a simulator screenshot was compared with the relevant Stitch screenshot when
  Stitch is the design source
- product-critical artwork, image treatment, color energy, and component
  personality are either implemented or captured in an explicit ready follow-up
  task before maturity/release-readiness work continues

If the native screen keeps the feature layout but loses the concept's core
visual identity, mark the adoption as `partially_adopted`, not done-without-risk.

## Debug / fix task
Done when:
- the issue was reproduced or directly observed
- the cause was understood well enough to justify the fix
- the fix was validated in the affected flow
- nearby regression risk was checked when relevant
- notes explain what changed and why confidence is reasonable

## Production-readiness task
Done when:
- the targeted readiness concern was improved materially
- the relevant evidence exists (performance, memory, observability, error handling, etc.)
- the improvement is documented in the roadmap notes
- any remaining risk is explicitly called out
