# GAP Analysis — el_hospital

## Requirement → Standard Module Mapping

| # | Requirement | Standard Module | Coverage | Custom Work Needed? |
|---|-------------|-----------------|----------|---------------------|
| 1 | Patient registration | `base` (res.partner) | ⚠ Partial | ✅ YES — hospital.patient wrapper |
| 2 | Appointment scheduling | None (calendar exists but not medical) | ❌ None | ✅ YES — hospital.appointment |
| 3 | Medical records (EMR) | None | ❌ None | ✅ YES — hospital.medical.record |
| 4 | Prescriptions | None | ❌ None | ✅ YES — hospital.prescription |
| 5 | Departments | None (hr.department is HR, not medical) | ❌ None | ✅ YES — hospital.department |
| 6 | Physicians/Doctors | `hr` (hr.employee) | ⚠ Partial | ✅ YES — hospital.physician (wraps hr) |
| 7 | Wards & Beds | None | ❌ None | ✅ YES — hospital.ward, hospital.bed |
| 8 | Admission/Discharge | None | ❌ None | ✅ YES — hospital.admission |
| 9 | Lab tests | None | ❌ None | ✅ YES — hospital.lab.test |
| 10 | Radiology orders | None | ❌ None | ✅ YES — hospital.radiology.order |
| 11 | Medicaments | `product` (product.product) | ⚠ Partial | ✅ YES — hospital.medicament (wraps product) |
| 12 | Billing/Invoicing | `account` (account.move) | ✅ Full | ⚠ MINIMAL — hospital.invoice.billing wrapper |
| 13 | Email notifications | `mail` | ✅ Full | ❌ NO — use mail.template |
| 14 | Multi-company | `base` | ✅ Full | ❌ NO — use record rules |
| 15 | PDF reports | `web` (QWeb) | ✅ Full | ❌ NO — use QWeb templates |
| 16 | Dashboard | `board` / `web` | ⚠ Basic | ✅ YES — custom OWL dashboard |
| 17 | Sequences (codes) | `base` (ir.sequence) | ✅ Full | ❌ NO — use ir.sequence records |

## Build Scope (Custom Work)

Based on the GAP analysis, the actual custom build scope is:

### Models to build (14 models + sub-models)
1. `hospital.department`
2. `hospital.physician`
3. `hospital.patient` (+ allergy, disease sub-models)
4. `hospital.appointment`
5. `hospital.medical.record`
6. `hospital.prescription` (+ line)
7. `hospital.ward`
8. `hospital.bed`
9. `hospital.admission`
10. `hospital.lab.test`
11. `hospital.radiology.order`
12. `hospital.medicament`
13. `hospital.invoice.billing` (+ line)
14. `hospital.dashboard`

### Models to extend
- `res.partner` — add `is_patient`, `is_physician` boolean flags (minimal)
- `product.template` — add `is_medicament` flag (minimal)

### Standard modules to depend on
`base`, `mail`, `hr`, `stock`, `account`, `sale_management`

### Configuration-only (no code)
- Multi-company (record rules)
- Mail templates (data records)
- Sequences (data records)
- Security groups + ACL (data records)

## Dependency Decision

| Module | Action | Reason |
|--------|--------|--------|
| `base` | depend | Required |
| `mail` | depend | chatter + templates |
| `hr` | depend | physicians as employees |
| `stock` | depend | medicament inventory |
| `account` | depend | billing/invoicing |
| `sale_management` | depend | product.template for medicaments |

## Estimated Effort Reduction
- Requirements fully covered by Odoo: 5/17 (~29%)
- Effort saved: ~30% (no reinventing invoicing, mail, multi-company, PDF, sequences)
- Actual custom scope: 14 models + 2 minimal extensions
