# Alignment Decision — el_hr_attendance_sheet

> Alignment with Odoo 20 standard design patterns.

## Odoo Pattern Compliance Checklist

| Pattern | Status | Implementation |
|---|---|---|
| Model naming convention `<prefix>.<name>` | ✅ | All models prefixed `hr.attendance.` |
| Inheritance over modification | ✅ | `_inherit = 'hr.contract'` instead of editing source |
| Active/Archive pattern | ✅ | `active` field on all config models (overtime/lateness/absence rules, policy, public holiday) |
| Tracking & Chatter | ✅ | `mail.thread` + `mail.activity.mixin` on sheet, policy, batch, public holiday |
| State machines with validation | ✅ | All state transitions validate current state before write |
| Multi-company considerations | ✅ | `company_id` on sheet/policy/batch via `hr.contract.company_id`; record rules restrict to user's company |
| Access rights layering | ✅ | 3 groups: User / Officer / Manager (CRUD matrix) |
| Translation support | ✅ | `_()` on all user-facing strings; English-only PO file shipped |
| Standard module interactions | ✅ | hr_payroll salary rules + structure follow standard `hr.salary.rule` model |
| OWL 2.x patterns | N/A | No OWL components needed |
| `<list>` not `<tree>` | ✅ | All list views use `<list>` (Odoo 18+) |
| `invisible=` not `states=`/`attrs=` | ✅ | All visibility via `invisible="..."` |
| `<chatter/>` not `<div class="oe_chatter">` | ✅ | All forms use `<chatter/>` |
| `models.Constraint()` not `_sql_constraints` | ✅ | Python-side `models.Constraint` for unique constraints |
| `groups` not `groups_id` | ✅ | Standard `groups="..."` attribute |
| `privilege_id` not `category_id` | ✅ | Security groups use `privilege_id` for Odoo 20 |

## Design Decisions

### 1. Public Holidays as Separate Model
**Decision:** Build new `hr.attendance.public.holiday` model instead of using `resource.calendar.leaves`.
**Reason:** The standard model lacks employee/tag scoping and an "active" flag for overtime calc inclusion. We need to selectively apply holidays per employee/dept/tag, which `resource.calendar.leaves` doesn't support cleanly.

### 2. Policy Linked to Contract, Not Employee
**Decision:** `hr.attendance.policy` linked via `hr.contract.attendance_policy_id`.
**Reason:** Contracts already carry payroll-relevant config (wage, working schedule, schedule_pay). Attendance policy is a natural fit there. Employees may have multiple contracts over time; linking to contract keeps historical accuracy.

### 3. Reuse resource.calendar for Planned Hours
**Decision:** Don't build a new "planned schedule" model.
**Reason:** `hr.contract.resource_calendar_id` already points to `resource.calendar`. The sheet reads planned hours from there.

### 4. Salary Rules via Data XML (not Python)
**Decision:** Create the 4 attendance salary rules + structure as data XML files.
**Reason:** Standard Odoo pattern — salary rules are user-configurable after install. Using data XML with `noupdate="1"` allows users to modify them post-install without losing changes on upgrade.

### 5. Sheet State Machine
**Decision:** `draft → computed → approved → done / cancelled`
**Reason:** Mirrors payslip state machine for consistency. `computed` = calculation done but not yet reviewed; `approved` = HR reviewed; `done` = payslip generated.

## Anti-Patterns Avoided

- ❌ Positional xpath (`//field[1]`) — use `@name` everywhere
- ❌ `_sql_constraints` — use `models.Constraint` (Odoo 20)
- ❌ `@api.multi` / `@api.one` — removed in Odoo 17+
- ❌ Hardcoded group IDs — use `ref()` references
- ❌ Direct SQL — all data access via ORM
- ❌ Manual chatter divs — use `<chatter/>`
