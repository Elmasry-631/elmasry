# Construction Task Gantt Planning

## Scope

The module now provides an Odoo Enterprise Gantt planning view for `el_construction.task` using the native `web_gantt` view.

## Scheduling fields

- `date_start`: task planned start date.
- `date_end`: task planned finish date.
- `date_deadline`: contractual/management deadline shown in the task popover and used for overdue highlighting.
- `progress`: completion percentage shown on the Gantt pill.
- `planned_hours`: planned workload and timesheet capacity reference.
- `assigned_to`: responsible employee and Gantt grouping/thumbnail context.
- `project_id`: default Gantt grouping.
- `phase_id` / `sub_project_id`: additional planning context.

## Dependencies

Dependencies are Finish-to-Start:

```text
Predecessor ───────────────► Successor
       finishes                  starts
```

The model exposes:

- `predecessor_ids` (`Blocked By`)
- `successor_ids` (`Blocking Tasks`)

The server rejects:

- self-dependencies,
- circular dependency chains,
- cross-project dependencies,
- cross-company dependencies,
- a successor starting before its predecessor finishes.

The native Odoo Gantt dependency arrows use these fields to visualize the schedule and allow dependency planning.

## Gantt capabilities

- Day / Week / Month / Year scales.
- Default Month scale.
- Project grouping.
- Progress visualization.
- Status-based decoration.
- Employee thumbnails.
- Dependency arrows.
- Drag/drop date planning for editable open tasks.
- Planning mode without creating tasks directly from blank cells.
- Total row.
- Dynamic range.
- Detailed task popover.

## Security and workflow

Task workflow protections remain server-side. Closed tasks cannot be modified through the Gantt because the Task model rejects planning writes after Done/Cancelled. Dependency changes are also validated server-side and cannot bypass the workflow/data-integrity rules through RPC.

## Runtime gate

The view requires the Odoo Enterprise `web_gantt` module. Static XML/Python validation can confirm syntax and references, but a live Odoo 19 registry/database is required to certify drag/drop behavior, dependency arrows, access rights, and browser rendering.
