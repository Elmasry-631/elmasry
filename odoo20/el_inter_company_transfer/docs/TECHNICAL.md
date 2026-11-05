# Inter Company Internal Transfer

- **المسار والإصدار:** `odoo20/el_inter_company_transfer` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Request stock transfers between warehouses of different companies

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 3 file(s)

### نماذج وامتدادات Odoo

- StockWarehouse: model _inherit
- InterCompanyTransferRequest: model _name
- InterCompanyTransferRequestLine: model _name

### الملفات المصدرية ذات الصلة

- `views/transfer_request_menus.xml`
- `views/transfer_request_views.xml`
- `models/stock_warehouse.py`
- `models/__init__.py`
- `models/transfer_request.py`
- `models/transfer_request_line.py`
- `security/ir.access.csv`

### حقول معلنة

- `name (Char)`
- `state (Selection)`
- `company_id (Many2one)`
- `source_warehouse_id (Many2one)`
- `dest_company_id (Many2one)`
- `dest_warehouse_id (Many2one)`
- `line_ids (One2many)`
- `user_id (Many2one)`
- `confirmed_by (Many2one)`
- `confirmed_date (Datetime)`
- `picking_id (Many2one)`
- `incoming_picking_id (Many2one)`
- `note (Text)`
- `is_draft (Boolean)`
- `can_confirm (Boolean)`
- `request_id (Many2one)`
- `sequence (Integer)`
- `product_id (Many2one)`
- `product_uom_id (Many2one)`
- `product_qty (Float)`
- `available_qty (Float)`
- `company_id (Many2one)`

### XML IDs

- `views/transfer_request_menus.xml::menu_inter_company_transfer_root`
- `views/transfer_request_menus.xml::menu_inter_company_transfer_request`
- `views/transfer_request_views.xml::view_inter_company_transfer_request_tree`
- `views/transfer_request_views.xml::view_inter_company_transfer_request_form`
- `views/transfer_request_views.xml::view_inter_company_transfer_request_search`
- `views/transfer_request_views.xml::view_inter_company_transfer_request_kanban`
- `views/transfer_request_views.xml::action_inter_company_transfer_request`
- `data/ir_sequence_data.xml::seq_inter_company_transfer_request`