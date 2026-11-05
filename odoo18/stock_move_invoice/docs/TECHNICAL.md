# Invoice From Stock Picking

- **المسار والإصدار:** `odoo18/stock_move_invoice` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Create invoice for stock picking

## المكونات المكتشفة

- Python: 9 file(s)
- XML: 4 file(s)

### نماذج وامتدادات Odoo

- Settings: model _inherit
- AccountMove: model _inherit
- StockPicking: model _inherit
- StockReturnInvoicePicking: model _inherit
- PickingInvoice: model _name

### الملفات المصدرية ذات الصلة

- `views/stock_picking_views.xml`
- `views/res_config_settings_views.xml`
- `views/account_move_views.xml`
- `models/res_config_settings.py`
- `models/account_move.py`
- `models/stock_picking.py`
- `models/stock_return_picking.py`
- `models/__init__.py`
- `security/ir.model.access.csv`
- `wizard/picking_invoice_views.xml`
- `wizard/__init__.py`
- `wizard/picking_invoice.py`

### حقول معلنة

- `customer_journal_id (Many2one)`
- `vendor_journal_id (Many2one)`
- `picking_id (Many2one)`
- `transfer_ids (Many2many)`
- `invoice_count (Integer)`
- `operation_code (Selection)`
- `is_return (Boolean)`

### XML IDs

- `views/stock_picking_views.xml::view_picking_form`
- `views/stock_picking_views.xml::action_create_invoice_for_multi_transfer`
- `views/res_config_settings_views.xml::res_config_settings_view_form`
- `views/account_move_views.xml::view_move_form`
- `wizard/picking_invoice_views.xml::picking_invoice_view_form`
- `wizard/picking_invoice_views.xml::action_picking_multi_invoice`