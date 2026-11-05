# eBook Serial Delivery

- **المسار والإصدار:** `odoo19/ebook_serial_delivery` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.

## المكونات المكتشفة

- Python: 12 file(s)
- XML: 4 file(s)

### نماذج وامتدادات Odoo

- ResCompany: model _inherit
- ResConfigSettings: model _inherit
- StockPicking: model _inherit
- StockMove: model _inherit
- SaleOrder: model _inherit
- ProductTemplate: model _inherit
- StockPickingJawalySms: model _name

### الملفات المصدرية ذات الصلة

- `report/ebook_serial_report_templates.xml`
- `views/res_config_settings_views.xml`
- `views/product_template_views.xml`
- `models/res_company.py`
- `models/res_config_settings.py`
- `models/stock_picking.py`
- `models/__init__.py`
- `models/stock_move.py`
- `models/sale_order.py`
- `models/product_template.py`
- `models/ebook_activation_code.py`

### حقول معلنة

- `ebook_serial_mail_template_id (Many2one)`
- `ebook_serial_mail_template_id (Many2one)`
- `ebook_email_sent (Boolean)`
- `ebook_serial_numbers_html (Html)`
- `is_ebook_with_codes (Boolean)`

### XML IDs

- `report/ebook_serial_report_templates.xml::action_report_ebook_serial`
- `report/ebook_serial_report_templates.xml::report_ebook_serial_document`
- `views/res_config_settings_views.xml::res_config_settings_view_form_ebook_serial`
- `views/res_config_settings_views.xml::ebook_serial_email`
- `views/product_template_views.xml::view_product_template_form_ebook_serial`
- `views/product_template_views.xml::ebook_serial_section`
- `views/product_template_views.xml::view_picking_form_ebook_resend`
- `data/mail_template_data.xml::mail_template_ebook_serial`