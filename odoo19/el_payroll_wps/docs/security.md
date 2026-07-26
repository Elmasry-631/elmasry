# Security — el_payroll_wps

## 1. Groups
This module does **NOT** create any new security group. It re-uses `hr_payroll.group_hr_payroll_user`.

| Group (existing) | Stakeholder | Module Use |
|-------------------|-------------|------------|
| `hr_payroll.group_hr_payroll_user` | HR Officer | Run the WPS Export wizard |
| `hr_payroll.group_hr_payroll_manager` | HR Manager | (Inherits from User) Run the wizard |
| `base.group_system` | IT Admin | Full system access (incl. wizard) |

## 2. Access Rights (`security/ir.model.access.csv`)

| Model | Group | Read | Write | Create | Unlink |
|-------|-------|------|-------|--------|--------|
| `wps.export.wizard` | `hr_payroll.group_hr_payroll_user` | ✅ | ✅ | ✅ | ✅ |
| `wps.export.wizard` | `base.group_system` | ✅ | ✅ | ✅ | ✅ |
| `hr.payslip` (inherited) | (unchanged — owned by `hr_payroll`) | — | — | — | — |

## 3. Record Rules
**None added.** Rationale:
- `wps.export.wizard` is transient.
- `hr.payslip` already has multi-company rules from `hr_payroll`.
- CSV `ir.attachment` is owned by creator.

## 4. Field-Level Security
**No field-level restrictions.** Rationale:
- `x_others` is informational.
- PII in the CSV is only ever written into an `ir.attachment` whose own ACL restricts access.

## 5. Workflow Security
**No state machine** → no workflow security. Payslip's state machine is owned by `hr_payroll` and unchanged.

## 6. CSV Download Security
The download URL `/web/content/<attachment_id>?download=true` is governed by `ir.attachment`'s standard ACL:
- Creator can download.
- Other Payroll users get 403 (unless they have system-admin rights).

## 7. Threat Model

| Threat | Likelihood | Impact | Mitigation |
|--------|-----------|--------|------------|
| Non-Payroll user opens wizard URL | Low | Medium | ACL denies — `AccessError` |
| User exports future-month payslips | Low | Low | Future payslips are typically `draft` — excluded |
| CSV leaked via shared download URL | Medium | High | `ir.attachment` is creator-only |
| SQL injection via `month` field | Very Low | High | ORM `.search()` with parameterized domain |
