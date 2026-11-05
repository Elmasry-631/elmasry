# Balance Confirmation

- **المسار والإصدار:** `odoo19/partner_balance_confirmation` — Odoo 19
- **إصدار الحزمة:** `19.0.3.6.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Customer Balance Confirmation (Imdad / Namo templates)

## المكونات المكتشفة

- Python: 7 file(s)
- XML: 5 file(s)

### نماذج وامتدادات Odoo

- ResPartner: model _inherit
- BalanceConfirmationWizard: model _name

### الملفات المصدرية ذات الصلة

- `views/res_partner_views.xml`
- `models/res_partner.py`
- `models/__init__.py`
- `models/arabic_amount_to_text.py`
- `security/ir.model.access.csv`
- `wizard/balance_confirmation_wizard.py`
- `wizard/__init__.py`
- `wizard/balance_confirmation_wizard_views.xml`

### حقول معلنة

- `partner_id (Many2one)`
- `confirmation_date (Date)`
- `template_type (Selection)`
- `notes (Text)`
- `printed_by (Many2one)`
- `balance (Monetary)`
- `balance_text (Char)`
- `currency_id (Many2one)`

### XML IDs

- `reports/balance_confirmation_report.xml::paperformat_balance_confirmation`
- `reports/balance_confirmation_report.xml::action_report_balance_confirmation`
- `reports/balance_confirmation_templates.xml::report_balance_confirmation_document`
- `views/res_partner_views.xml::view_partner_form_balance_confirmation`
- `data/mail_template.xml::mail_template_balance_confirmation`
- `wizard/balance_confirmation_wizard_views.xml::view_balance_confirmation_wizard_form`