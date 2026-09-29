# Quality Check Workflow

## Purpose

The Quality Check model is the construction QA/QC control point between execution and acceptance. It records the inspection scope, checkpoints, evidence, result, corrective action and re-inspection history.

## Workflow

```text
Draft
  |
  | Start Inspection (Inspector + checkpoints required)
  v
In Inspection
  |--------------------|----------------------|
  |                    |                      |
 Pass               Conditional             Fail
  |                    |                      |
  |                    |                Corrective Action
  |                    |                + Re-inspection Date
  |                    |                      |
  |                    |                 Re-inspection
  |                    |                      |
  |                    |              Pass / Conditional / Fail
  |                    |                      |
  +--------------------+----------------------+
                       |
                 Close (Manager)
                       |
                    Closed
```

## Rules

- A Quality Check must belong to a Project and Company.
- Sub Project, Phase and Work Order must belong to the same Project/Company.
- An Inspector must belong to the same Company.
- At least one checkpoint is required before starting.
- Every checkpoint must have a result before recording a final result.
- `Pass` is blocked if any checkpoint is failed.
- `Fail` requires at least one failed checkpoint, a corrective/preventive action, and a re-inspection date.
- `Conditional Pass` requires corrective/preventive action.
- A Failed check moves to `Re-inspection Required` before another final result is recorded.
- Only Passed or Conditional checks can be Closed, and closing requires a Construction Manager.
- Closed and Cancelled checks are read-only.
- Only Draft checks can be deleted.
- Direct state changes through ORM/RPC are blocked; workflow actions are the only supported transitions.
- Checkpoint/evidence changes are blocked after an inspection result is recorded.

## Integration with Work Orders

A Work Order cannot be completed while a related Quality Check is `In Inspection`, `Failed`, or `Conditional Pass`. This prevents execution from being treated as complete while QA/QC still has an unresolved result.

## Recommended UAT

1. Create a workmanship inspection for a Work Order.
2. Add checkpoints and evidence.
3. Start inspection.
4. Record all checkpoint results.
5. Test Pass and Manager Close.
6. Test Failed → Corrective Action → Re-inspection → Pass.
7. Test Conditional → Manager Close.
8. Verify a Work Order cannot be completed while the QC is unresolved.
9. Verify normal users cannot cancel/close/reset a QC through RPC or the UI.
10. Test the workflow in two companies.
