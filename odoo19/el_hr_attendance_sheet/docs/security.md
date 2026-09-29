# Security — el_hr_attendance_sheet

> Access rights matrix, groups, and record rules.

## Privilege

**Privilege:** `module_privilege_hr_attendance_sheet` — "Attendance Sheets"
(Replaces `category_id` which was removed in Odoo 19.)

## Groups (3 levels)

| Group | XML ID | Implied By | Description |
|-------|--------|------------|-------------|
| Attendance Sheet User | `group_hr_attendance_sheet_user` | hr_attendance.group_hr_attendance_user | Read-only access to sheets, policies, rules |
| Attendance Sheet Officer | `group_hr_attendance_sheet_officer` | User | Create/write sheets + batches; cannot delete |
| Attendance Sheet Manager | `group_hr_attendance_sheet_manager` | Officer | Full CRUD on all objects |

The admin user (`base.user_admin`) is automatically added to the Manager group on install.

## Access Rights Matrix

| Model | User | Officer | Manager |
|---|---|---|---|
| hr.attendance.public.holiday | R | RWC | RWCD |
| hr.attendance.public.holiday.line | R | RWC | RWCD |
| hr.attendance.rule.overtime | R | — | RWCD |
| hr.attendance.rule.lateness | R | — | RWCD |
| hr.attendance.rule.lateness.step | R | — | RWCD |
| hr.attendance.rule.absence | R | — | RWCD |
| hr.attendance.rule.absence.step | R | — | RWCD |
| hr.attendance.policy | R | — | RWCD |
| hr.attendance.sheet | R | RWC | RWCD |
| hr.attendance.sheet.line | R | RWC | RWCD |
| hr.attendance.sheet.batch | — | RWC | RWCD |
| hr.attendance.sheet.batch.line | — | RWC | RWCD |
| hr.attendance.change.data.wizard | — | RWCD | RWCD |
| hr.attendance.sheet.batch.wizard | — | RWCD | RWCD |
| hr.attendance.create.payslip.wizard | — | RWCD | RWCD |

Legend: R=Read, W=Write, C=Create, D=Delete

## Record Rules

### Multi-company rules

Each major model has a record rule restricting access to the user's companies:

| Rule | Model | Domain |
|------|-------|--------|
| `rule_hr_attendance_sheet_company` | hr.attendance.sheet | `\|', ('company_id', '=', False), ('company_id', 'in', company_ids)]` |
| `rule_hr_attendance_policy_company` | hr.attendance.policy | same |
| `rule_hr_attendance_public_holiday_company` | hr.attendance.public.holiday | same |
| `rule_hr_attendance_sheet_batch_company` | hr.attendance.sheet.batch | same |
| `rule_hr_attendance_rule_overtime_company` | hr.attendance.rule.overtime | same |

### Employee-self rule

| Rule | Model | Group | Access |
|------|-------|-------|--------|
| `rule_hr_attendance_sheet_personal` | hr.attendance.sheet | `base.group_user` | Read-only on own sheets |

This allows regular employees to view their own attendance sheets without needing the Attendance Sheet User group.

## Salary Rules

The 4 salary rules (OVERT, LATE, ABS, DIFF) are created via data XML with `noupdate="1"` to prevent re-creation on upgrade. Users can modify them post-install without losing changes.

## Sequences

Three sequences created with `noupdate="1"`:
- `seq_hr_attendance_sheet` — prefix `AS/%(year)s/%(month)s/`, padding 4
- `seq_hr_attendance_sheet_batch` — prefix `ASB/%(year)s/`, padding 4
- `seq_hr_attendance_policy` — prefix `POL/`, padding 4

All sequences have `company_id = False` (shared across companies).

---

*Author: Ibrahim Elmasry*
