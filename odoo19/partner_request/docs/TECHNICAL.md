# Partner Request

- **المسار والإصدار:** `odoo19/partner_request` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for creating new customers via sales requests.

## المكونات المكتشفة

- Python: 4 file(s)
- XML: 4 file(s)

### نماذج وامتدادات Odoo

- PartnerRequest: model _name
- ResPartner: model _inherit

### الملفات المصدرية ذات الصلة

- `views/partner_request_views.xml`
- `views/partner_request_menus.xml`
- `models/partner_request.py`
- `models/__init__.py`
- `security/partner_request_security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `name (Char)`
- `customer_code (Char)`
- `classification_id (Many2one)`
- `contact_person (Char)`
- `partner_id (Many2one)`
- `sequence (Char)`
- `country_id (Many2one)`
- `state_id (Many2one)`
- `city (Char)`
- `area (Char)`
- `street (Char)`
- `zip (Char)`
- `pobox (Char)`
- `phone (Char)`
- `email (Char)`
- `vat (Char)`
- `sales_supervisor_id (Many2one)`
- `salesperson_id (Many2one)`
- `state (Selection)`
- `rejection_reason (Text)`
- `send_back_reason (Text)`

### XML IDs

- `views/partner_request_views.xml::view_partner_request_list`
- `views/partner_request_views.xml::view_partner_request_form`
- `views/partner_request_views.xml::view_partner_request_search`
- `views/partner_request_views.xml::action_partner_request`
- `views/partner_request_menus.xml::menu_partner_request`
- `data/partner_request_data.xml::seq_partner_request`
- `data/partner_request_data.xml::seq_partner_request_date_range`
- `security/partner_request_security.xml::module_category_partner_request`
- `security/partner_request_security.xml::res_groups_privilege_partner_request`
- `security/partner_request_security.xml::group_partner_request_user`
- `security/partner_request_security.xml::sales_team.group_sale_salesman`
- `security/partner_request_security.xml::group_partner_request_manager`
- `security/partner_request_security.xml::sales_team.group_sale_manager`