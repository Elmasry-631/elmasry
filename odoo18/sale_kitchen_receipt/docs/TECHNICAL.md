# Kitchen Receipt from Quotation

- **المسار والإصدار:** `odoo18/sale_kitchen_receipt` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Print kitchen receipt from sales quotation

## المكونات المكتشفة

- Python: 4 file(s)
- XML: 2 file(s)

### نماذج وامتدادات Odoo

- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/sale_order_views.xml`
- `models/__init__.py`
- `models/sale_order.py`

### حقول معلنة

- `x_building_floor (Char)`
- `x_landmark (Char)`
- `x_driver_name (Char)`

### XML IDs

- `reports/kitchen_receipt.xml::paperformat_kitchen_receipt`
- `reports/kitchen_receipt.xml::action_kitchen_receipt_report`
- `reports/kitchen_receipt.xml::kitchen_receipt_template`
- `views/sale_order_views.xml::sale_order_form_inherit_kitchen`
- `views/sale_order_views.xml::account_move_form_inherit_kitchen`