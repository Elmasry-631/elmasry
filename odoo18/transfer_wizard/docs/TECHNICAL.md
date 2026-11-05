# trade_paints_wizard

- **المسار والإصدار:** `odoo18/transfer_wizard` — Odoo 18
- **إصدار الحزمة:** `1.1`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Transfer Wizard

## المكونات المكتشفة

- Python: 4 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- TransferWizard: model _name
- StockPicking: model _inherit

### الملفات المصدرية ذات الصلة

- `security/ir.model.access.csv`
- `wizard/transfer_wizard.py`
- `wizard/transfer_wizard.xml`
- `wizard/__init__.py`

### حقول معلنة

- `expected_weight (Float)`
- `driver_name (Many2one)`
- `car_number (Char)`
- `driver_name (Many2one)`
- `car_number (Char)`
- `printed_before (Boolean)`

### XML IDs

- `wizard/transfer_wizard.xml::transfer_wizard_form_view`
- `wizard/transfer_wizard.xml::server_action_open_transfer_wizard`