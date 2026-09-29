# Construction Task Workflow

## Business states

```text
Draft
  ├── Start ───────────────> In Progress
  └── Cancel (Manager) ────> Cancelled

In Progress
  ├── Complete (Manager) ──> Done
  └── Cancel (Manager) ────> Cancelled

Cancelled
  └── Reset to Draft (Manager) -> Draft

Done
  └── Terminal state
```

## Completion rules

- A Task must be `In Progress` before completion.
- If Planned Hours are greater than zero, completed timesheet hours must reach Planned Hours.
- If Planned Hours are zero, Progress must be 100%.
- A running timer must be stopped before completion.
- Completed Tasks are read-only for planning fields and cannot be deleted.
- Cancelled Tasks are locked until a Construction Manager resets them to Draft.

## Timer rules

- The timer can start only on an In Progress Task.
- One running timer is allowed per Task.
- Running Timesheets can only be created by the Task timer.
- Stopping the timer converts the running Timesheet to Done.
- Timer activity cannot be created for Done or Cancelled Tasks.

## Security

- State transitions are server-side protected; hiding a button in the UI is not the security mechanism.
- Complete, Cancel, and Reset are Manager operations.
- Task, Timesheet, Project, Sub Project, Phase, and Work Order references are company/project consistent.
- The Task workflow does not modify Odoo core models.

## Design intent

The Task workflow is deliberately smaller than Project/Work Order workflows:
Task is an execution tracking record, not an approval document. Its lifecycle is therefore
Draft -> In Progress -> Done, with a controlled Cancelled branch.
