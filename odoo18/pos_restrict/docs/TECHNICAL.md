# POS User Restrict

- **المسار والإصدار:** `odoo18/pos_restrict` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Restricts User access to pos and orders.

## المكونات المكتشفة

- Python: 5 file(s)
- XML: 2 file(s)

### نماذج وامتدادات Odoo

- PosConfig: model _inherit
- ResUsers: model _inherit

### الملفات المصدرية ذات الصلة

- `views/res_users_views.xml`
- `models/pos_config.py`
- `models/__init__.py`
- `models/res_users.py`
- `security/pos_restrict_groups.xml`

### حقول معلنة

- `users_allowed (Many2many)`
- `allowed_pos (Many2many)`
- `show_users (Boolean)`

### XML IDs

- `views/res_users_views.xml::view_users_form`
- `views/res_users_views.xml::view_pos_config_kanban`
- `security/pos_restrict_groups.xml::restrict_user`
- `security/pos_restrict_groups.xml::restrict_manager`
- `security/pos_restrict_groups.xml::order_user`
- `security/pos_restrict_groups.xml::order_manager`