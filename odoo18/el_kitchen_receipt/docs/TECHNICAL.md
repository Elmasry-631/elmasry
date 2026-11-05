# Kitchen Receipt from Quotation

- **المسار والإصدار:** `odoo18/el_kitchen_receipt` — Odoo 18
- **إصدار الحزمة:** `18.0.4.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery

## المكونات المكتشفة

- Python: 11 file(s)
- XML: 10 file(s)

### نماذج وامتدادات Odoo

- ResPartner: model _inherit
- AccountMove: model _inherit
- StockPicking: model _inherit
- XPilot: model _name
- PilotReportWizard: model _name
- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/stock_picking_views.xml`
- `views/sale_order_views.xml`
- `views/x_pilot_views.xml`
- `views/sale_order_search.xml`
- `views/pilot_report_buttons.xml`
- `views/res_partner_views.xml`
- `views/account_move_views.xml`
- `views/pilot_report_wizard.xml`
- `models/res_partner.py`
- `models/account_move.py`
- `models/stock_picking.py`
- `models/x_pilot.py`
- `models/__init__.py`
- `models/pilot_report_wizard.py`
- `models/sale_order.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `x_building_floor (Char)`
- `x_landmark (Char)`
- `x_driver_name (Many2one)`
- `x_driver_name (Many2one)`
- `x_driver_name (Many2one)`
- `name (Char)`
- `x_driver_name (Many2many)`
- `date_from (Date)`
- `date_to (Date)`
- `sale_order_id (Many2one)`
- `x_building_floor (Char)`
- `x_landmark (Char)`
- `x_driver_name (Many2one)`

### XML IDs

- `reports/pilot_report.xml::action_pilot_report`
- `reports/pilot_report.xml::pilot_report_template`
- `reports/kitchen_receipt.xml::paperformat_kitchen_receipt`
- `reports/kitchen_receipt.xml::action_kitchen_receipt_report`
- `reports/kitchen_receipt.xml::kitchen_receipt_template`
- `views/stock_picking_views.xml::view_picking_form_inherit_driver`
- `views/stock_picking_views.xml::view_picking_tree_inherit_driver`
- `views/sale_order_views.xml::sale_order_form_inherit_kitchen`
- `views/x_pilot_views.xml::x_pilot_list_view`
- `views/x_pilot_views.xml::x_pilot_form_view`
- `views/x_pilot_views.xml::x_pilot_search_view`
- `views/x_pilot_views.xml::action_x_pilot`
- `views/x_pilot_views.xml::menu_x_pilot`
- `views/sale_order_search.xml::sale_order_search_inherit_kitchen`
- `views/pilot_report_buttons.xml::menu_pilot_report`
- `views/res_partner_views.xml::view_partner_form_inherit_kitchen`
- `views/account_move_views.xml::account_move_form_inherit_kitchen_driver`
- `views/account_move_views.xml::account_move_search_inherit_kitchen`
- `views/account_move_views.xml::account_move_tree_inherit_kitchen`
- `views/pilot_report_wizard.xml::pilot_report_wizard_form`
- `views/pilot_report_wizard.xml::action_pilot_report_wizard`