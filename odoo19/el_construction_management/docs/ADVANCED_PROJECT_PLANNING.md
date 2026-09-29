# Advanced Construction Project Planning

## Planning architecture

```text
Project
  └── Phase / WBS
       └── Task
            ├── Dependencies (Finish-to-Start)
            ├── Baseline
            ├── Actual Start / Actual Finish
            ├── Critical Path / Slack
            └── Schedule Health / Early Warning
```

## Baseline

A Construction Manager can capture a frozen snapshot of the current Task plan:
- Baseline Start
- Baseline End
- Baseline Hours
- Baseline Set On

The baseline is not silently overwritten by later drag/drop planning changes.
Current plan dates remain separate from the baseline, enabling variance analysis.

## Actuals

Actual Start is captured when the Task enters `In Progress`. Actual Finish is
captured when the Task is completed. Timesheets remain the workload/effort source.

## Critical Path

The module calculates project-level Critical Path using the current Task dependency
network and planned dates. Tasks with zero calculated float are marked Critical Path.
Tasks with positive float expose the number of slack days/hours. The calculation is
read-time and does not silently move user-entered dates.

## Schedule Health

- `No Schedule`: missing planned dates.
- `On Track`: no current warning.
- `At Risk`: an active task is approaching its planned finish/deadline.
- `Delayed`: an active task is past its planned finish/deadline.
- `Completed`: task is closed as Done.

## Early-warning controls

Gantt and list views expose Critical Path, Slack, Schedule Health, Delay, and Baseline
Finish Variance. Managers can filter delayed and at-risk tasks before they become
project-level schedule failures.

## Milestones

Tasks can be marked as milestones. A milestone is required to use a single calendar date
(`Start Date == End Date`). This module keeps milestone semantics server-side rather than
relying on a UI-only flag.

## Gantt

The native Odoo Enterprise `web_gantt` view provides Day/Week/Month/Year scales,
dependencies, drag/drop planning, progress, grouping by Project/Sub Project/Phase/Assignee,
popovers, and schedule-slack visualization. The project form includes a direct Schedule
entry point.

## Runtime certification

A live Odoo 19 Enterprise registry/database is still required to certify browser rendering,
drag/drop persistence, dependency arrows, security, and full ORM test execution.
