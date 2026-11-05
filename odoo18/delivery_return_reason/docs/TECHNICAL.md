# Delivery Return Reasons

- **المسار والإصدار:** `odoo18/delivery_return_reason` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** تتبع أسباب رجوع الطلبات مع إحصائيات وتحليلات

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 6 file(s)

### نماذج وامتدادات Odoo

- DeliveryReturnReason: model _name
- StockPicking: model _inherit
- StockReturnPicking: model _inherit

### الملفات المصدرية ذات الصلة

- `views/stock_picking_views.xml`
- `views/stock_picking_analysis.xml`
- `views/stock_picking_search.xml`
- `views/stock_picking_return_views.xml`
- `views/delivery_return_reason_views.xml`
- `models/delivery_return_reason.py`
- `models/stock_picking.py`
- `models/__init__.py`
- `models/stock_picking_return.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `name (Char)`
- `sequence (Integer)`
- `active (Boolean)`
- `company_id (Many2one)`
- `x_returned (Boolean)`
- `x_return_reason_id (Many2one)`
- `x_return_note (Text)`
- `x_return_reason_id (Many2one)`
- `x_return_note (Text)`

### XML IDs

- `views/stock_picking_views.xml::stock_picking_form_inherit_return`
- `views/stock_picking_analysis.xml::view_stock_picking_return_pivot`
- `views/stock_picking_analysis.xml::view_stock_picking_return_graph`
- `views/stock_picking_analysis.xml::action_delivery_return_analysis`
- `views/stock_picking_analysis.xml::action_delivery_return_analysis_pivot`
- `views/stock_picking_analysis.xml::action_delivery_return_analysis_graph`
- `views/stock_picking_analysis.xml::menu_delivery_return_analysis`
- `views/stock_picking_search.xml::stock_picking_search_inherit_return`
- `views/stock_picking_return_views.xml::view_stock_return_picking_form_inherit_reason`
- `views/delivery_return_reason_views.xml::view_delivery_return_reason_tree`
- `views/delivery_return_reason_views.xml::view_delivery_return_reason_form`
- `views/delivery_return_reason_views.xml::view_delivery_return_reason_search`
- `views/delivery_return_reason_views.xml::action_delivery_return_reason`
- `views/delivery_return_reason_views.xml::menu_delivery_return_root`
- `views/delivery_return_reason_views.xml::menu_delivery_return_reason_config`
- `data/delivery_return_reason_data.xml::reason_client_refused`
- `data/delivery_return_reason_data.xml::reason_client_unavailable`
- `data/delivery_return_reason_data.xml::reason_wrong_address`
- `data/delivery_return_reason_data.xml::reason_late_delivery`
- `data/delivery_return_reason_data.xml::reason_damaged_product`
- `data/delivery_return_reason_data.xml::reason_missing_product`
- `data/delivery_return_reason_data.xml::reason_wrong_order`
- `data/delivery_return_reason_data.xml::reason_duplicate_order`
- `data/delivery_return_reason_data.xml::reason_client_phone_off`
- `data/delivery_return_reason_data.xml::reason_other`