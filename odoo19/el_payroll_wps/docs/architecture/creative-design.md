# Creative Design — el_payroll_wps

## 1. The 5 Lenses (per skill workflow §04)

### Lens 1: Pattern Discovery
**Pattern:** *Form Inheritance + Transient Wizard* — one of the most common Odoo patterns. We extend a standard model with one informational field, and add a single-purpose wizard for the export. No new persistent model, no new state machine, no new security group.

### Lens 2: UX Innovation
**Strategy applied:** *Zero-friction export*.
- The wizard opens with `month` pre-filled to today → the HR officer can usually just click "Export CSV" without typing anything.
- The download is a single click → no intermediate "preview" step.
- Errors are surfaced as `UserError` (red modal) so the officer immediately knows why nothing came back.

### Lens 3: Smart Automation
**Type:** *Computed field on existing lifecycle*.
- `x_others` recomputes automatically whenever the sheet is recomputed — no manual refresh button, no cron.
- We deliberately did NOT automate the export itself (no cron) because WPS submissions happen once a month and require human review before sending to the bank.

### Lens 4: Future-Proofing
**Strategies applied:**
1. *Forward-compatible field access* — `_get_bank_account` checks `if 'primary_bank_account_id' in employee._fields` before accessing it, so the module survives a future Odoo version that renames the field again.
2. *Runtime menu reparenting safety net* — even though the static XML pins `parent="hr_work_entry_enterprise.menu_hr_payroll_root"`, the `post_init_hook` will reparent by name if that xmlid does not exist on a custom build.
3. *UTF-8 BOM* — the CSV opens correctly in Excel on Windows, Mac, and older versions.

### Lens 5: Wow Factor
**Differentiators:**
1. *Manual-edit-safe compute* — `x_others` is recomputed ONLY when the sheet is recomputed, so an HR officer's manual override survives form saves.
2. *Bank-ready filename* — `Salary_July_2026.csv` is named so the file sorts chronologically in any file manager.
3. *Excel-safe Arabic* — the BOM ensures Arabic names open correctly in Excel without the "wrong encoding" garbled-text problem.

## 2. Visual Identity
- **Module icon:** an HR-themed 3D icon in the red/purple family (matches the standard `hr_payroll` icon palette).
- **No custom CSS/SCSS** — the wizard uses Odoo's standard `btn-primary` / `btn-secondary` classes.

## 3. Naming Conventions
- Field: `x_others` (custom prefix per Odoo convention)
- Model: `wps.export.wizard` (lowercase dots, matches Odoo's transient naming)
- Menu xmlid: `menu_wps_export`
- Action xmlid: `action_wps_export_wizard`
- View xmlids: `view_hr_payslip_form_inherit_wps` (inherit) and `view_wps_export_wizard_form` (new)
