# Quality Check Audit & Hardening Report — V7

## Scope

Full review of `el_construction.quality.check`, its checkpoint/image child models, views, workflow integration with Work Orders, company consistency, CRUD protection, and regression tests.

## Recommended construction QA/QC lifecycle

```text
Draft
  |
  | Start Inspection
  v
In Inspection
  |---------|----------------|------------------|
  |         |                |                  |
 Pass   Conditional       Failed               Cancel
  |         |                |                  |
  |         |          Corrective Action        |
  |         |          + Re-inspection Date    |
  |         |                |                  |
  |         |          Re-inspection            |
  |         |                |                  |
  |         |       Pass / Conditional / Fail   |
  |         |                |                  |
  +---------+----------------+                  |
             |                                  |
       Close (Manager)                     Cancelled
             |                                  |
          Closed                         Reset (Manager)
```

This separates inspection execution from acceptance/closure and gives failed inspections a controlled corrective-action/reinspection loop.

## Key improvements

### Workflow and controls

- Centralized valid transitions using the module workflow mixin.
- Direct state writes through ORM/RPC are blocked.
- Starting inspection requires an Inspector and at least one checkpoint.
- Every checkpoint must have a result before a final inspection result is recorded.
- Pass is blocked when any checkpoint is failed.
- Fail requires at least one failed checkpoint, corrective/preventive action, and a re-inspection date.
- Conditional Pass requires corrective/preventive action.
- Failed inspections must explicitly enter Re-inspection Required before another final result.
- Only Passed or Conditional checks can be Closed.
- Closing is Construction Manager-only.
- Cancellation and reset are Construction Manager-only.
- Closed and Cancelled records are read-only.
- Only Draft records can be deleted.

### Data integrity

- Project is mandatory.
- Company is mandatory and must match the Project.
- Sub Project, Phase and Work Order are checked against Project and Company.
- Inspector company is checked against the Quality Check company.
- Re-inspection and closure dates cannot precede the inspection date.
- Quality Check references have a database uniqueness constraint.
- Child checkpoints require a parent and are protected after a result is recorded.
- Evidence images require a description and binary image and are protected after a result is recorded.

### Inspection visibility

Added stored result KPIs:

- Total Check Points
- Passed Check Points
- Failed Check Points
- Pending Check Points
- Completion Percentage

These make the inspection status understandable before a final result is selected.

### Work Order integration

Existing Work Order completion logic already prevents completion while a related Quality Check is `in_progress`, `fail`, or `conditional`. The enhanced QC lifecycle preserves that safety gate; a QC must reach an acceptable result and then be closed before the project team can treat the related work as fully accepted.

## Security review

The workflow actions that materially change acceptance/cancellation status are protected server-side. UI visibility is treated as convenience only; authorization is enforced in Python.

## Regression coverage added

- Start requires inspector/checkpoints.
- Normal successful inspection: Start → Pass → Manager Close.
- Incomplete checkpoint results are rejected.
- Failed inspection requires failed checkpoint + corrective action + reinspection date.
- Failed → Re-inspection → Pass.
- Direct state manipulation is blocked.
- Closed records are read-only.
- Cancel/reset are Manager-only.

## Static validation

- Python AST parsing: PASS
- XML parsing: PASS
- Duplicate method scan: PASS
- Deprecated Odoo view syntax scan (`tree`, `attrs`, `states`): PASS
- Manifest version/reference checks: PASS
- ZIP integrity: PASS
- Python cache cleanup: PASS

## Runtime validation status

Odoo 19 runtime/registry/database execution was not available in the current environment. Therefore this package is **not claimed as runtime-certified**.

## Required staging/UAT gate

1. Restore a clone of the production database.
2. Upgrade the module to `19.0.1.6.0`.
3. Run Odoo automated tests including `test_quality_check`.
4. Execute Pass, Conditional, Fail → Re-inspection → Pass, Cancel, and Reset scenarios.
5. Verify Manager-only Close/Cancel/Reset from both UI and RPC.
6. Verify Work Order completion is blocked by unresolved QC.
7. Test two companies and cross-company references.
8. Verify evidence/checkpoint immutability after result/closure.
9. Validate chatter/activity behavior and translations in the real Odoo registry.
