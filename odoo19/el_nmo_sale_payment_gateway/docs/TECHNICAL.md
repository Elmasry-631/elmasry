# Sale Payment Gateway

- **المسار والإصدار:** `odoo19/el_nmo_sale_payment_gateway` — Odoo 19
- **إصدار الحزمة:** `19.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Payment Gateway on Sales/Invoice/Delivery + auto-sync Receivable & Payable accounts from gateway to partner

## المكونات المكتشفة

- Python: 8 file(s)
- XML: 5 file(s)

### نماذج وامتدادات Odoo

- ResPartner: model _inherit
- AccountMove: model _inherit
- StockPicking: model _inherit
- StockMove: model _inherit
- SalePaymentGateway: model _name
- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/stock_picking_views.xml`
- `views/sale_order_views.xml`
- `views/res_partner_views.xml`
- `views/account_move_views.xml`
- `views/payment_gateway_views.xml`
- `models/res_partner.py`
- `models/account_move.py`
- `models/stock_picking.py`
- `models/sale_payment_gateway.py`
- `models/__init__.py`
- `models/sale_order.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `payment_gateway_id (Many2one)`
- `payment_gateway_id (Many2one)`
- `carrier_id (Many2one)`
- `payment_gateway_id (Many2one)`
- `payment_gateway_id (Many2one)`
- `name (Char)`
- `active (Boolean)`
- `property_account_receivable_id (Many2one)`
- `property_account_payable_id (Many2one)`
- `payment_gateway_id (Many2one)`

### XML IDs

- `views/stock_picking_views.xml::view_picking_payment_gateway`
- `views/sale_order_views.xml::view_sale_order_payment_gateway`
- `views/res_partner_views.xml::view_partner_payment_gateway`
- `views/account_move_views.xml::view_invoice_payment_gateway`
- `views/payment_gateway_views.xml::view_payment_gateway_tree`
- `views/payment_gateway_views.xml::view_payment_gateway_form`
- `views/payment_gateway_views.xml::action_payment_gateway`
- `views/payment_gateway_views.xml::menu_payment_gateway`