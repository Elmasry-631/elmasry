# HR Attendance Sheet And Policies

> Odoo 19 module that calculates overtime, lateness and absence from raw attendance
> records and feeds the results to the payroll system via dedicated salary rules.

## Description

`el_hr_attendance_sheet` provides an attendance-sheet and policy layer on top of Odoo's
`hr_attendance`. It closes the gap between Odoo's `hr_attendance` (which only records
check-in/out) and `hr_payroll` (which needs overtime/lateness/absence inputs to compute
the payslip).

The module covers the full lifecycle:

1. **Configuration** — define overtime rules (per day type), lateness penalty matrix
   (multi-step), absence penalty rules (multi-step), and bundle them into an
   Attendance Policy.
2. **Public holidays** — define holidays scoped to employees / departments / tags.
3. **Sheet computation** — per employee per period, day-by-day breakdown with planned
   hours, worked hours, overtime, late-in minutes, absence flag, leave flag and
   difference hours. Handles multi-interval attendance records.
4. **Manual correction** — a wizard lets HR officers override computed values on any
   line, with a mandatory reason note that is preserved in the line's history.
5. **Payslip integration** — one click creates a payslip from an approved sheet, using
   the included "Attendance Structure" salary structure with 4 rules (OVERT, LATE,
   ABS, DIFF).
6. **Batch by department** — generate sheets for an entire department in one go.

## Odoo Version

- **Target:** Odoo 19.0
- **Runtime validation:** Not executed as part of this documentation review.

## Installation

1. Copy the `el_hr_attendance_sheet` folder to your Odoo `addons` directory.
2. Restart Odoo with `-u all` or update the app list.
3. Go to **Apps** → search "Attendance Sheet" → Install.
4. Dependencies (`hr_attendance`, `hr`, `hr_payroll`, `hr_holidays`, `mail`, `calendar`)
   will be installed automatically if missing.

## Features

- ✅ Public holidays with employee/department/tag scoping + active flag
- ✅ Overtime rules per day type (working_day / weekend / public_holiday) + apply_after
- ✅ Multi-step lateness penalty matrix (rate-based or amount-based)
- ✅ Multi-step absence penalty rules
- ✅ Attendance policy aggregator linked to `hr.contract`
- ✅ Per-employee per-period attendance sheet with day-by-day breakdown
- ✅ Multi-interval attendance handling (multiple check-in/out per day)
- ✅ Overlapping interval tolerance
- ✅ Manual data correction wizard with reason logging
- ✅ Create payslip directly from approved sheet
- ✅ Salary rules + structure (OVERT, LATE, ABS, DIFF)
- ✅ Batch generation by department
- ✅ Multi-company aware (record rules + company_id on every model)
- ✅ Full chatter + activity mixin on transactional models
- ✅ PDF report (QWeb)
- ✅ Pivot + Graph analysis views
- ✅ 3-tier security (User / Officer / Manager)
- ✅ Employee-self record rule is defined for users in `base.group_user`; the current ACL matrix still requires the Attendance Sheet User group for model read access (see Security Notes)

## Models

| Model | Description |
|-------|-------------|
| `hr.attendance.public.holiday` | Public holiday definition |
| `hr.attendance.public.holiday.line` | Per-employee/dept/tag scoping |
| `hr.attendance.rule.overtime` | Overtime rule (3 types) |
| `hr.attendance.rule.lateness` + `.step` | Lateness rule with multi-step penalty |
| `hr.attendance.rule.absence` + `.step` | Absence rule with multi-step penalty |
| `hr.attendance.policy` | Policy combining all rules |
| `hr.attendance.sheet` | Main sheet (per employee per period) |
| `hr.attendance.sheet.line` | Per-day breakdown |
| `hr.attendance.sheet.batch` + `.line` | Batch by department |
| 3 wizard TransientModels | Change data / Batch wizard / Create payslip |
| `hr.contract` (extended) | Adds `attendance_policy_id` |
| `hr.payslip` (extended) | Adds `attendance_sheet_id` + 4 computed inputs |

See [docs/models.md](docs/models.md) for the full field reference.

## Security

| Group | Access |
|-------|--------|
| Attendance Sheet User | Read-only on sheets, policies, rules |
| Attendance Sheet Officer | Create/write sheets + batches; no delete |
| Attendance Sheet Manager | Full CRUD on everything |

Regular employees can read their own sheets via the `rule_hr_attendance_sheet_personal`
record rule (no special group needed).

See [docs/security.md](docs/security.md) for the full matrix.

## State Machines

### Sheet: `draft → computed → approved → done / cancelled`

### Batch: `draft → confirmed → done / cancelled`

### Public Holiday: `draft → active / cancelled`

See [docs/workflows.md](docs/workflows.md) for full diagrams and transition rules.

## Author

**Ibrahim Elmasry** — Senior Odoo Developer + DevOps + Implementation Consultant

## License

GNU Lesser General Public License v3.0 — see [LICENSE](LICENSE) file.

## Documentation

| File | Purpose |
|------|---------|
| [docs/architecture/](docs/architecture/) | 7 architecture docs (GAP, impact, alignment, model design, data flow, state machines, dependencies) |
| [docs/models.md](docs/models.md) | Full field/method reference |
| [docs/security.md](docs/security.md) | Access rights matrix + record rules |
| [docs/workflows.md](docs/workflows.md) | State machines + business workflows |
| [docs/views.md](docs/views.md) | View layouts + button map |
| [docs/api.md](docs/api.md) | Public Python API for extension |
| [docs/configuration.md](docs/configuration.md) | Setup steps |
| [docs/testing.md](docs/testing.md) | Test plan (50+ test cases) |
| [docs/icon-design.md](docs/icon-design.md) | Module icon design rationale |
