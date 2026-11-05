# CRM Project Linker

- **المسار والإصدار:** `odoo19/crm_project_linker` — Odoo 19
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Create and link projects from CRM opportunities.

## المكونات المكتشفة

- Python: 4 file(s)
- XML: 1 file(s)

### نماذج وامتدادات Odoo

- CrmLead: model _inherit
- Project: model _inherit
- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/crm_lead_view.xml`
- `models/crm_lead.py`
- `models/__init__.py`

### حقول معلنة

- `project_id (Many2one)`
- `sale_order_id (Many2one)`
- `crm_lead_id (Many2one)`
- `sale_order_id (Many2one)`
- `sale_order_ids (One2many)`
- `project_id (Many2one)`

### XML IDs

- `views/crm_lead_view.xml::crm_lead_view_form_inherit_project`
- `views/crm_lead_view.xml::crm_lead_view_form_inherit_project_button`
- `views/crm_lead_view.xml::project_project_view_form_inherit_crm`
- `views/crm_lead_view.xml::view_project_form_inherit_sale_orders`
- `views/crm_lead_view.xml::action_project_quotation_list`