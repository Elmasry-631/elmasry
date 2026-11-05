# Commission Types

- **المسار والإصدار:** `odoo19/el_commission_type` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage sales commission types by team member role

## المكونات المكتشفة

- Python: 6 file(s)
- XML: 5 file(s)

### نماذج وامتدادات Odoo

- ResPartner: model _inherit
- SalesCommission: model _name
- SalesCommissionType: model _name

### الملفات المصدرية ذات الصلة

- `views/commission_type_views.xml`
- `views/menu.xml`
- `views/sales_commission_views.xml`
- `views/res_partner_views.xml`
- `models/res_partner.py`
- `models/sales_commission.py`
- `models/commission_type.py`
- `models/__init__.py`
- `security/security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `sales_commission_type (Many2one)`
- `name (Char)`
- `partner_id (Many2one)`
- `team_member_type (Selection)`
- `commission_percentage (Float)`
- `company_id (Many2one)`
- `team_member_type (Selection)`
- `commission_percentage (Float)`
- `company_id (Many2one)`
- `name (Char)`

### XML IDs

- `views/commission_type_views.xml::view_commission_type_tree`
- `views/commission_type_views.xml::view_commission_type_form`
- `views/commission_type_views.xml::view_commission_type_search`
- `views/commission_type_views.xml::action_commission_type`
- `views/menu.xml::menu_commissions_root`
- `views/menu.xml::menu_commission`
- `views/menu.xml::menu_commission_type`
- `views/sales_commission_views.xml::view_sales_commission_tree`
- `views/sales_commission_views.xml::view_sales_commission_form`
- `views/sales_commission_views.xml::view_sales_commission_search`
- `views/sales_commission_views.xml::action_sales_commission`
- `views/res_partner_views.xml::view_partner_form_commission_type`
- `security/security.xml::module_category_commissions`
- `security/security.xml::privilege_commissions`
- `security/security.xml::group_commission_user`
- `security/security.xml::group_commission_manager`