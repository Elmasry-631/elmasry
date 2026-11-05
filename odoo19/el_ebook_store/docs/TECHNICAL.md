# E-Book Store

- **المسار والإصدار:** `odoo19/el_ebook_store` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Sell e-books with unique access codes — online reader + download

## المكونات المكتشفة

- Python: 14 file(s)
- XML: 9 file(s)

### نماذج وامتدادات Odoo

- EbookCode: model _name
- EbookAccessLog: model _name
- SaleOrder: model _inherit
- EbookLibrary: model _name
- ProductTemplate: model _inherit
- GenerateCodesWizard: model _name

### الملفات المصدرية ذات الصلة

- `controllers/portal.py`
- `controllers/__init__.py`
- `views/ebook_code_views.xml`
- `views/ebook_library_views.xml`
- `views/ebook_dashboard_views.xml`
- `views/ebook_menus.xml`
- `views/product_template_views.xml`
- `views/portal_ebook_views.xml`
- `models/ebook_code.py`
- `models/ebook_access_log.py`
- `models/__init__.py`
- `models/sale_order.py`
- `models/ebook_library.py`
- `models/product_template.py`
- `security/ir.model.access.csv`
- `security/security_groups.xml`
- `wizard/__init__.py`
- `wizard/generate_codes_wizard_views.xml`
- `wizard/generate_codes_wizard.py`

### حقول معلنة

- `name (Char)`
- `product_tmpl_id (Many2one)`
- `partner_id (Many2one)`
- `order_id (Many2one)`
- `state (Selection)`
- `generated_by (Selection)`
- `access_count (Integer)`
- `max_access (Integer)`
- `create_date (Datetime)`
- `used_date (Datetime)`
- `expiry_date (Datetime)`
- `library_id (Many2one)`
- `partner_id (Many2one)`
- `product_tmpl_id (Many2one)`
- `access_date (Datetime)`
- `ip_address (Char)`
- `user_agent (Char)`
- `partner_id (Many2one)`
- `product_tmpl_id (Many2one)`
- `code_id (Many2one)`
- `order_id (Many2one)`
- `state (Selection)`
- `purchase_date (Datetime)`
- `last_access (Datetime)`
- `access_count (Integer)`
- `is_ebook (Boolean)`
- `ebook_file (Binary)`
- `ebook_filename (Char)`
- `ebook_sample (Binary)`
- `ebook_sample_filename (Char)`
- `ebook_access_type (Selection)`
- `ebook_author (Char)`
- `ebook_pages (Integer)`
- `ebook_isbn (Char)`
- `ebook_total_codes (Integer)`
- `ebook_codes_used (Integer)`
- `ebook_codes_available (Integer)`
- `product_tmpl_id (Many2one)`
- `generation_mode (Selection)`
- `code_count (Integer)`
- `manual_codes (Text)`
- `max_access (Integer)`

### XML IDs

- `views/ebook_code_views.xml::view_ebook_code_form`
- `views/ebook_code_views.xml::view_ebook_code_list`
- `views/ebook_code_views.xml::view_ebook_code_search`
- `views/ebook_code_views.xml::action_ebook_code`
- `views/ebook_library_views.xml::view_ebook_library_form`
- `views/ebook_library_views.xml::view_ebook_library_list`
- `views/ebook_library_views.xml::action_ebook_library`
- `views/ebook_dashboard_views.xml::view_ebook_access_log_list`
- `views/ebook_dashboard_views.xml::action_ebook_access_log`
- `views/ebook_menus.xml::menu_ebook_root`
- `views/ebook_menus.xml::menu_ebook_codes`
- `views/ebook_menus.xml::menu_ebook_library`
- `views/ebook_menus.xml::menu_ebook_logs`
- `views/product_template_views.xml::view_product_template_form_ebook`
- `views/portal_ebook_views.xml::portal_my_library`
- `data/email_templates.xml::mail_template_ebook_code_delivery`
- `security/security_groups.xml::module_category_ebook_store`
- `security/security_groups.xml::group_ebook_user`
- `security/security_groups.xml::group_ebook_manager`
- `wizard/generate_codes_wizard_views.xml::view_generate_codes_wizard_form`
- `wizard/generate_codes_wizard_views.xml::action_generate_codes_wizard`