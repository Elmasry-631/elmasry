# Sale Order Automation

- **المسار والإصدار:** `odoo18/sale_order_automation` — Odoo 18
- **إصدار الحزمة:** `1.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Enable auto sale workflow with sale order confirmation. Include operations like Auto Create Invoice, Auto Validate Invoice and Auto Transfer Delivery Order.

## المكونات المكتشفة

- Python: 5 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- StockWarehouse: model _inherit
- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/stock_warehouse.xml`
- `models/warehouse.py`
- `models/__init__.py`
- `models/sale_order.py`

### حقول معلنة

- `is_delivery_set_to_done (Boolean)`
- `create_invoice (Boolean)`
- `validate_invoice (Boolean)`

### XML IDs

- `views/stock_warehouse.xml::sale_confirm_extended_for_warehouse`