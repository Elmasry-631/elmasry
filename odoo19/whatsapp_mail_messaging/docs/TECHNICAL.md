# Odoo Whatsapp Connector

- **المسار والإصدار:** `odoo19/whatsapp_mail_messaging` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Odoo18 Whatsapp, Whatsapp Odoo Integration, Odoo Whatsapp Connector,       Odoo Whatsapp, Whatsapp Connector, Whatsapp Integration, Odoo18, Whatsapp,      Odoo Apps

## المكونات المكتشفة

- Python: 14 file(s)
- XML: 11 file(s)
- JavaScript/TypeScript: 4 file(s)

### نماذج وامتدادات Odoo

- ResCompany: model _inherit
- ResConfigSettings: model _inherit
- AccountMove: model _inherit
- SelectionMessage: model _name
- SaleOrder: model _inherit
- Website: model _inherit
- WhatsappSendMessage: model _name
- PortalShare: model _inherit

### الملفات المصدرية ذات الصلة

- `controllers/whatsapp_mail_messaging.py`
- `controllers/__init__.py`
- `views/selection_message_views.xml`
- `views/website_templates.xml`
- `views/res_company_views.xml`
- `views/res_config_settings_views.xml`
- `views/sale_order_views.xml`
- `views/account_move_views.xml`
- `views/website_views.xml`
- `security/ir.model.access.csv`
- `wizard/whatsapp_send_message.py`
- `wizard/portal_share_views.xml`
- `wizard/portal_share.py`
- `wizard/whatsapp_send_message_views.xml`
- `wizard/__init__.py`

### حقول معلنة

- `whatsapp_message (Text)`
- `whatsapp_message (Text)`
- `name (Char)`
- `message (Text)`
- `mobile_number (Char)`
- `partner_id (Many2one)`
- `mobile (Char)`
- `message (Text)`
- `image_1920 (Binary)`
- `share_type (Selection)`
- `mobile_number (Char)`
- `partner_id (Many2one)`

### XML IDs

- `views/selection_message_views.xml::selection_message_view_tree`
- `views/selection_message_views.xml::selection_message_view_form`
- `views/selection_message_views.xml::selection_message_action`
- `views/selection_message_views.xml::menu_website_selection_message`
- `views/website_templates.xml::ChatToCompany`
- `views/website_templates.xml::ModalWhatsapp`
- `views/website_templates.xml::exampleModalLabel`
- `views/website_templates.xml::CustomSelect`
- `views/website_templates.xml::DefaultSelect`
- `views/website_templates.xml::phoneMessage`
- `views/website_templates.xml::myFormControl`
- `views/website_templates.xml::exampleFormControlTextarea1`
- `views/res_company_views.xml::res_company_view_form`
- `views/res_config_settings_views.xml::res_config_settings_view_form`
- `views/res_config_settings_views.xml::whatsapp_message`
- `views/sale_order_views.xml::view_order_form`
- `views/sale_order_views.xml::view_quotation_tree_with_onboarding`
- `views/account_move_views.xml::view_move_form`
- `views/account_move_views.xml::view_out_invoice_tree`
- `views/website_views.xml::view_website_form`
- `wizard/portal_share_views.xml::portal_share_wizard`
- `wizard/whatsapp_send_message_views.xml::whatsapp_send_message_view_form`
- `static/src/xml/whatsapp_icon_template.xml::fa-icon`
- `static/src/xml/mail_icon_template.xml::fa-icon`