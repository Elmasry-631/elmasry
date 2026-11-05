# Button Access Control

- **المسار والإصدار:** `odoo19/el_button_access_control` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Control button visibility per user group — show/hide buttons in any view without editing XML

## المكونات المكتشفة

- Python: 7 file(s)
- XML: 4 file(s)
- JavaScript/TypeScript: 1 file(s)

### نماذج وامتدادات Odoo

- ElButtonAccessRule: model _name
- Base: model _inherit

### الملفات المصدرية ذات الصلة

- `views/button_access_rule_views.xml`
- `views/menus.xml`
- `models/button_access_rule.py`
- `models/base.py`
- `models/__init__.py`
- `security/el_button_access_control_groups.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `name (Char)`
- `sequence (Integer)`
- `active (Boolean)`
- `model_id (Many2one)`
- `model_name (Char)`
- `view_type (Selection)`
- `button_name (Selection)`
- `button_string (Char)`
- `mode (Selection)`
- `group_ids (Many2many)`
- `company_id (Many2one)`

### XML IDs

- `views/button_access_rule_views.xml::view_el_button_access_rule_form`
- `views/button_access_rule_views.xml::view_el_button_access_rule_list`
- `views/button_access_rule_views.xml::view_el_button_access_rule_search`
- `views/button_access_rule_views.xml::action_el_button_access_rule`
- `views/menus.xml::menu_el_button_access_root`
- `views/menus.xml::menu_el_button_access_rules`
- `views/menus.xml::menu_el_button_access_config`
- `views/menus.xml::menu_el_button_access_groups`
- `security/el_button_access_control_groups.xml::group_button_access_user`
- `security/el_button_access_control_groups.xml::group_button_access_manager`