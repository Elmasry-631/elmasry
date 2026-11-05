# POS Customer Payment Method

- **المسار والإصدار:** `odoo19/el_pos_customer_payment_method` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

## المكونات المكتشفة

- Python: 8 file(s)
- XML: 2 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- ResPartner: model _inherit
- ResConfigSettings: model _inherit
- PosConfig: model _inherit

### الملفات المصدرية ذات الصلة

- `views/res_config_settings_views.xml`
- `views/res_partner_views.xml`
- `models/res_partner.py`
- `models/res_config_settings.py`
- `models/pos_config.py`
- `models/__init__.py`

### حقول معلنة

- `el_allowed_pos_payment_method_ids (Many2many)`
- `pos_el_default_payment_method_ids (Many2many)`
- `el_pos_default_payment_method_ids (Many2many)`

### XML IDs

- `views/res_config_settings_views.xml::res_config_settings_view_form_el_pos_default_pm`
- `views/res_config_settings_views.xml::el_pos_default_payment_methods`
- `views/res_partner_views.xml::view_partner_form_el_pos_payment`