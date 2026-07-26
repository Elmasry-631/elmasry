# Stakeholder Analysis — el_payroll_wps

## Stakeholder Matrix

| # | Name/Title | Role | Influence | Impact | Attitude | Engagement |
|---|-----------|------|-----------|--------|----------|------------|
| 1 | HR Manager (Sponsor) | Sponsor | High | High | Supportive | Weekly demo, sign-off on CSV format |
| 2 | HR Officer (Payroll) | Key User | Medium | High | Supportive | Training + feedback after first month |
| 3 | IT Admin | IT Admin | Medium | Medium | Supportive | Technical docs, install + upgrade plan |
| 4 | Bank WPS Coordinator | External | Low | High | Neutral | Receive CSV, give feedback on format |
| 5 | Employees | Affected | Low | Low | Neutral | Informed via existing payslip flow |

## RACI Matrix

| Task / Deliverable | HR Manager | HR Officer | IT Admin | Bank Coordinator |
|-------------------|-----------|-----------|----------|------------------|
| Requirements approval | A | R | I | C |
| Architecture design | A | C | R | I |
| CSV column order sign-off | A | R | I | C |
| Security rules | I | C | R | I |
| User acceptance testing | A | R | I | C |
| Training materials | I | R | C | I |
| Deployment decision | A | I | R | I |
| Go-live approval | A | R | I | C |

## Key Concerns to Address
- **HR Officer:** "Will `x_others` be overwritten if I edit it manually?" → Addressed: only `compute_sheet()` rewrites it; manual edits persist until next recompute.
- **HR Manager:** "Is the CSV accepted by the bank as-is?" → Addressed: column order matches the WPS submission template; UTF-8 BOM ensures Arabic opens correctly in Excel.
- **IT Admin:** "Will this survive Odoo 19 upgrades?" → Addressed: uses Odoo 19 fields (`primary_bank_account_id`, `private_state_id`, `validated`/`paid` states); no deprecated patterns.
- **Bank Coordinator:** "Are deductions shown as positive or negative?" → Addressed: per the user's correct spec, `discount` is positive (e.g. `200.00`).

## User Roles → Security Groups Mapping
| Stakeholder | Security Group | Permissions |
|-------------|---------------|-------------|
| HR Officer | hr_payroll.group_hr_payroll_user | read, write, create, unlink on wps.export.wizard |
| HR Manager | hr_payroll.group_hr_payroll_manager | inherits above (via group hierarchy) |
| IT Admin | base.group_system | implicit admin access |
| Employees | (no access) | cannot see the wizard or the export |
