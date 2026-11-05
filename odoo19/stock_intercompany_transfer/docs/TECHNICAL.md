# Inter Company Stock Transfer

- **المسار والإصدار:** `odoo19/stock_intercompany_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Create counterpart Receipt/Delivery Orders between     companies.

## المكونات المكتشفة

- Python: 7 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- ResCompany: model _inherit
- StockPickingInherit: model _inherit
- StockBackorderConfirmation: model _inherit

### الملفات المصدرية ذات الصلة

- `views/res_company_views.xml`
- `models/res_company.py`
- `models/stock_picking.py`
- `models/__init__.py`
- `wizard/stock_backorder_confirmation.py`
- `wizard/__init__.py`

### حقول معلنة

- `enable_inter_company_transfer (Boolean)`
- `destination_warehouse_id (Many2one)`
- `apply_transfer_type (Selection)`
- `message (Text)`
- `auto_generated (Boolean)`
- `is_backorder_button_clicked (Boolean)`
- `stock_id (Many2one)`

### XML IDs

- `views/res_company_views.xml::view_company_form`