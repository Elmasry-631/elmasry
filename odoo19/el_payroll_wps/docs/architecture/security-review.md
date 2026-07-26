# Security Review — el_payroll_wps

## 1. User Groups
This module does **NOT** create any new security group. It re-uses the standard
`hr_payroll.group_hr_payroll_user` group.

| Group (existing) | Stakeholder | Permissions on this module |
|-------------------|-------------|----------------------------|
| `hr_payroll.group_hr_payroll_user` | HR Officer | RWCD on `wps.export.wizard` |
| `hr_payroll.group_hr_payroll_manager` | HR Manager | (inherits via group hierarchy) RWCD |
| `base.group_system` | IT Admin | RWCD (full system access) |

## 2. Models Access Matrix

| Model | Payroll User | Payroll Manager | System Admin |
|-------|--------------|-----------------|--------------|
| `hr.payslip` (inherited) | (inherits from hr_payroll) RWCD own company | RWCD own company | RWCD all |
| `wps.export.wizard` | RWCD | RWCD | RWCD |
| `ir.attachment` (CSV file) | R (own) | R (own) | RWCD all |

## 3. Record Rules
**None needed.** Rationale:
- `wps.export.wizard` is a TransientModel — records live for only a few hours.
- `hr.payslip` already has multi-company and personal-record rules from `hr_payroll`.
- The CSV `ir.attachment` is owned by the user who created it; standard `ir.attachment` rules restrict read to the creator.

## 4. Field-Level Security
**No field-level restrictions added.** Rationale:
- `x_others` is informational.
- PII in the CSV is only ever written into an `ir.attachment` whose own ACL restricts access.

## 5. Workflow Security
**No state machine on this module.** The payslip's own state machine (Odoo 19: `draft → verify → validated → paid → cancel`) is owned by `hr_payroll` and unchanged. The export wizard only reads payslips in `validated` or `paid` states.

## 6. CSV Download Security
The download URL `/web/content/<attachment_id>?download=true` is governed by `ir.attachment`'s standard ACL:
- The user who created the attachment can download it.
- Other Payroll users cannot download someone else's CSV unless they have system-admin rights.

## 7. Potential Attack Surface

| Vector | Risk | Mitigation |
|--------|------|------------|
| User without Payroll group opens wizard URL directly | Medium | ACL denies access — `AccessError` |
| User manipulates `month` to export future-month payslips | Low | Payslips must exist AND be `validated`/`paid` |
| CSV leaked via shared download URL | Medium | `ir.attachment` is owned by creator |
| SQL injection via `month` field | None | ORM `.search()` with parameterized domain |

## 8. Verdict
**PASS** — the module re-uses standard `hr_payroll` groups, adds no new attack surface, and relies on `ir.attachment`'s existing ACL for the CSV file.
