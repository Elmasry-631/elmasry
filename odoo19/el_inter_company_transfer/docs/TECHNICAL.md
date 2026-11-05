# Inter Company Transfer

- **المسار والإصدار:** `odoo19/el_inter_company_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automate inter-company stock, sale, purchase, and accounting documents

## المكونات المكتشفة

- Python: 11 file(s)
- XML: 11 file(s)

### نماذج وامتدادات Odoo

- PurchaseOrder: model _inherit
- ResCompany: model _inherit
- AccountMove: model _inherit
- StockPicking: model _inherit
- StockInterCompanyTransfer: model _name
- StockInterCompanyTransferLine: model _name
- SaleOrder: model _inherit
- InterCompanyConfig: model _name
- ReturnInterCompanyTransfer: model _name
- ReturnInterCompanyTransferLine: model _name

### الملفات المصدرية ذات الصلة

- `views/res_company_views.xml`
- `views/stock_picking_views.xml`
- `views/sale_order_views.xml`
- `views/inter_company_menus.xml`
- `views/account_move_views.xml`
- `views/stock_inter_company_transfer_views.xml`
- `views/return_inter_company_transfer_views.xml`
- `views/purchase_order_views.xml`
- `views/inter_company_config_views.xml`
- `models/purchase_order.py`
- `models/res_company.py`
- `models/account_move.py`
- `models/stock_picking.py`
- `models/__init__.py`
- `models/stock_inter_company_transfer.py`
- `models/sale_order.py`
- `models/inter_company_config.py`
- `models/return_inter_company_transfer.py`
- `security/ir.model.access.csv`
- `security/security_groups.xml`

### حقول معلنة

- `inter_company_transfer_id (Many2one)`
- `inter_company_sale_order_id (Many2one)`
- `inter_company_warehouse_id (Many2one)`
- `inter_company_transfer_id (Many2one)`
- `inter_company_transfer_id (Many2one)`
- `name (Char)`
- `source_company_id (Many2one)`
- `dest_company_id (Many2one)`
- `from_warehouse_id (Many2one)`
- `to_warehouse_id (Many2one)`
- `state (Selection)`
- `sale_order_id (Many2one)`
- `purchase_order_id (Many2one)`
- `delivery_picking_id (Many2one)`
- `receipt_picking_id (Many2one)`
- `customer_invoice_id (Many2one)`
- `vendor_bill_id (Many2one)`
- `partner_id (Many2one)`
- `date (Date)`
- `config_id (Many2one)`
- `transfer_line_ids (One2many)`
- `company_id (Many2one)`
- `transfer_id (Many2one)`
- `product_id (Many2one)`
- `quantity (Float)`
- `uom_id (Many2one)`
- `price_unit (Float)`
- `company_id (Many2one)`
- `inter_company_transfer_id (Many2one)`
- `inter_company_purchase_order_id (Many2one)`
- `source_company_id (Many2one)`
- `dest_company_id (Many2one)`
- `display_name (Char)`
- `apply_on (Selection)`
- `link_document (Boolean)`
- `auto_validate_picking (Boolean)`
- `auto_create_invoice (Boolean)`
- `auto_validate_invoice (Boolean)`
- `active (Boolean)`
- `name (Char)`
- `source_ict_id (Many2one)`
- `source_company_id (Many2one)`
- `dest_company_id (Many2one)`
- `from_warehouse_id (Many2one)`
- `to_warehouse_id (Many2one)`
- `state (Selection)`
- `sale_order_id (Many2one)`
- `purchase_order_id (Many2one)`
- `delivery_picking_id (Many2one)`
- `receipt_picking_id (Many2one)`
- `customer_invoice_id (Many2one)`
- `vendor_bill_id (Many2one)`
- `partner_id (Many2one)`
- `date (Date)`
- `return_line_ids (One2many)`
- `company_id (Many2one)`
- `transfer_id (Many2one)`
- `product_id (Many2one)`
- `quantity (Float)`
- `uom_id (Many2one)`
- `price_unit (Float)`
- `company_id (Many2one)`

### XML IDs

- `views/res_company_views.xml::view_company_form_inter_company_transfer`
- `views/stock_picking_views.xml::view_picking_form_inter_company_transfer`
- `views/sale_order_views.xml::view_order_form_inter_company_transfer`
- `views/inter_company_menus.xml::menu_inter_company_root`
- `views/inter_company_menus.xml::menu_stock_inter_company_transfer`
- `views/inter_company_menus.xml::menu_return_inter_company_transfer`
- `views/inter_company_menus.xml::action_inter_company_inventory_breakdown`
- `views/inter_company_menus.xml::menu_inter_company_inventory_breakdown`
- `views/inter_company_menus.xml::menu_inter_company_config`
- `views/account_move_views.xml::view_move_form_inter_company_transfer`
- `views/stock_inter_company_transfer_views.xml::view_stock_inter_company_transfer_list`
- `views/stock_inter_company_transfer_views.xml::view_stock_inter_company_transfer_form`
- `views/stock_inter_company_transfer_views.xml::action_stock_inter_company_transfer`
- `views/return_inter_company_transfer_views.xml::view_return_inter_company_transfer_list`
- `views/return_inter_company_transfer_views.xml::view_return_inter_company_transfer_form`
- `views/return_inter_company_transfer_views.xml::action_return_inter_company_transfer`
- `views/purchase_order_views.xml::purchase_order_form_inter_company_transfer`
- `views/inter_company_config_views.xml::view_inter_company_config_list`
- `views/inter_company_config_views.xml::view_inter_company_config_form`
- `views/inter_company_config_views.xml::action_inter_company_config`
- `data/inter_company_sequence.xml::seq_stock_inter_company_transfer`
- `data/inter_company_sequence.xml::seq_return_inter_company_transfer`
- `security/security_groups.xml::group_inter_company_transaction_manager`
- `security/security_groups.xml::rule_stock_inter_company_transfer_multi_company`
- `security/security_groups.xml::rule_stock_inter_company_transfer_line_multi_company`
- `security/security_groups.xml::rule_return_inter_company_transfer_multi_company`
- `security/security_groups.xml::rule_return_inter_company_transfer_line_multi_company`
- `security/security_groups.xml::rule_inter_company_config_multi_company`