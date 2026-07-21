# Metadata Evidence Schema

## Purpose
Add stronger structured memory for evidence, risk, architecture review, and anticipatory roadmap behavior.

## Recommended top-level additions
- `engineVersion`
- `appMaturity`
- `operatingModeDefaults`
- `taskEvidence`
- `designAdoptions`
- `visualParityAudits`
- `stitchArtExpansions`
- `stitchOperations`
- `conceptCoverage`
- `serviceMaturity`
- `architectureReviewLog`
- `riskRegister`
- `taskInjectionHistory`
- `scaffoldSchemas`
- `setupRun`

## taskEvidence item
```json
{
  "task": "TASK-ID",
  "validationTier": "tier4_persistence",
  "evidenceQuality": "standard",
  "validatedFlows": ["Profile persistence survives relaunch"],
  "regressionChecks": ["Orders header still reflects persisted profile"],
  "artifacts": ["screenshot-path-or-note"],
  "remainingRisk": ["optional"],
  "followUpRequired": false
}
```

## setupRun object

```json
{
  "nativeScaffoldCreated": true,
  "nativeTestTarget": "AppTargetTests",
  "schemeDiscovered": true,
  "firstBuildResult": "succeeded | failed | not_run | unknown",
  "firstLaunchEvidence": ".stitch/evidence/bootstrap/launch.png or null",
  "batonValidation": "passed | failed | not_run | unknown",
  "completionState": "ready_for_delivery | partial | blocked",
  "receipt": "docs/bootstrap-receipt.md"
}
```

The receipt renderer may report these values from the active run even before
all fields have been persisted. Missing receipt data is remediation evidence,
not a standalone blocker.

## architectureReviewLog item
```json
{
  "scope": ["orders", "rewards", "coach"],
  "finding": "Shared editorial card pattern is drifting",
  "followUpTask": "TASK-ID or null"
}
```

## visualParityAudits item
```json
{
  "task": "TASK-ID",
  "screen": "Recipe Detail",
  "referenceScreens": ["Stitch screen title/path/id"],
  "sourceAssets": [".stitch/intake/assets/example.jpg"],
  "simulatorEvidence": [".stitch/evidence/TASK-ID/screen.jpg"],
  "visualParityTarget": "same_product_family | prototype_visual_gate | exact_reference",
  "status": "pass | blocked | in_progress_not_verified_exact | intentionally_deferred",
  "blockingGaps": ["brief gap"],
  "followUpTask": "TASK-ID or null"
}
```

## stitchArtExpansions item
```json
{
  "task": "TASK-ID",
  "project": "Stitch project id or name",
  "reason": "missing artwork, variant, screen state, or exact parity blocker",
  "referenceScreens": ["existing Stitch screen title/path/id"],
  "newScreens": ["new Stitch screen title/path/id"],
  "generatedAssets": [".stitch/intake/assets/example.jpg"],
  "nativeDestination": "SwiftUI file or feature folder",
  "adoptionStatus": "pending | adopted | partially_adopted | rejected | deferred",
  "followUpTask": "TASK-ID or null"
}
```

## stitchOperations summary
```json
{
  "journal": ".stitch/operations/current.json",
  "activeProjectId": "project id or null",
  "lastStatus": "succeeded | polling | ambiguous_timeout | failed | null",
  "unresolvedOperationIds": []
}
```

Keep detailed mutation state in the operation journal. Metadata stores only the
durable handoff summary needed by future sessions.

## conceptCoverage item
```json
{
  "role": "Primary detail",
  "requirementSource": "user_prompt | feature_map | visual_exit_gate",
  "required": true,
  "status": "live | artifact_only | missing | deferred | not_needed",
  "projectId": "project id or null",
  "screenIds": [],
  "artifactPaths": [],
  "linkedTask": "TASK-ID or null",
  "note": "brief provenance or deferral reason"
}
```

## riskRegister item
```json
{
  "id": "risk-id",
  "surface": "orders",
  "level": "medium",
  "status": "open | accepted | resolved",
  "note": "brief explanation",
  "linkedTask": "TASK-ID"
}
```

## taskInjectionHistory item
```json
{
  "task": "TASK-ID",
  "trigger": "architecture_review_loop | app_maturity_transition | regression_risk | evidence_gap",
  "reason": "brief explanation",
  "createdForMaturity": "prototype | dogfood | beta | release_candidate | production"
}
```
