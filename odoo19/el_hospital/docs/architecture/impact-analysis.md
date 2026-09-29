# Impact Analysis — el_hospital

## Impact on Standard Odoo Models

| Model | Impact | Method |
|-------|--------|--------|
| `res.partner` | Low — add field `is_patient`, `is_physician` | classical inheritance via related |
| `hr.employee` | Low — add field `physician_id` (reverse) | optional, no required change |
| `product.template` | Low — add field `is_medicament` | used to flag medicament products |
| `account.move` | None — only reads via M2O | no extension |

## Impact on Standard Workflows

- **Accounting**: creating `account.move` via `action_create_invoice` follows
  the standard Odoo invoice creation pattern (journal + lines + post).
  No override of account.move methods.
- **Stock**: `hospital.medicament.stock_qty` is read-only computed from
  `stock.quant` — no writes to stock. Dispensing creates a stock.move
  (future enhancement, not in v1).
- **HR**: physicians link to `hr.employee` read-only; no HR workflow change.

## Multi-Company Considerations

- All models include `company_id` (Many2one res.company, default user company).
- Record rules ensure users see only their company's records.
- `hospital.invoice.billing` uses the patient's partner company for invoice.

## Security Impact

| Group | New Permissions |
|-------|----------------|
| Hospital User | read own department |
| Receptionist | patients + appointments (full) |
| Nurse | wards + beds + admissions (full) |
| Doctor | patients + appointments + EMR + prescriptions (full) |
| Lab Tech | lab tests + radiology (full) |
| Pharmacist | medicaments + prescriptions (full) |
| Admin | everything |

## Migration / Upgrade Risk

- **Low risk**: all new models (no existing data to migrate).
- **Sequences**: defined via `ir.sequence` records (stable across upgrades).
- **No overridden `create`/`write` on standard models** (no upgrade conflicts).
- **Views**: all custom views with `el_hospital_` prefix (no view overrides
  on standard models).

## Performance Considerations

- `appointment_count`, `admission_count` on patient are stored computed
  (not computed on-the-fly each time) — store=True with inverse triggers.
- Dashboard aggregates use `read_group` (SQL) not Python loops.
- Chart.js lazy-loaded via `loadJS()` — not bundled in assets.
- Bed occupancy recomputed on admission state change (trigger fields).
