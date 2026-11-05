# El-Nmo - Customer Classification

- **المسار والإصدار:** `odoo19/el_nmo_classification` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Customer classification tiers (A-E) with auto-classification criteria.

## المكونات المكتشفة

- Python: 8 file(s)
- XML: 6 file(s)

### نماذج وامتدادات Odoo

- ResPartner: model _inherit
- CustomerClassification: model _name
- AccountMove: model _inherit
- ClassificationCriteria: model _name
- SaleOrder: model _inherit

### الملفات المصدرية ذات الصلة

- `views/sale_order_views.xml`
- `views/customer_classification_views.xml`
- `views/res_partner_views.xml`
- `models/res_partner.py`
- `models/customer_classification.py`
- `models/account_move.py`
- `models/__init__.py`
- `models/classification_criteria.py`
- `models/sale_order.py`
- `security/security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `classification_id (Many2one)`
- `override_pricelist (Boolean)`
- `override_credit_limit (Boolean)`
- `override_payment_term (Boolean)`
- `manual_pricelist_id (Many2one)`
- `classification_pricelist_id (Many2one)`
- `classification_credit_limit (Float)`
- `classification_payment_term_id (Many2one)`
- `credit_policy (Selection)`
- `effective_credit_limit (Float)`
- `effective_payment_term_id (Many2one)`
- `payment_type (Selection)`
- `payment_gateway_id (Many2one)`
- `remaining_credit (Float)`
- `name (Char)`
- `description (Text)`
- `sequence (Integer)`
- `active (Boolean)`
- `pricelist_id (Many2one)`
- `credit_limit (Float)`
- `payment_term_id (Many2one)`
- `credit_policy (Selection)`
- `company_id (Many2one)`
- `partner_ids (One2many)`
- `partner_count (Integer)`
- `criteria_ids (One2many)`
- `has_active_criteria (Boolean)`
- `partner_classification_id (Many2one)`
- `partner_effective_credit_limit (Float)`
- `partner_credit_policy (Selection)`
- `classification_id (Many2one)`
- `sequence (Integer)`
- `model_field (Selection)`
- `operator (Selection)`
- `value (Float)`
- `value_to (Float)`
- `active (Boolean)`
- `partner_payment_type (Selection)`
- `partner_classification_id (Many2one)`
- `partner_effective_credit_limit (Float)`
- `partner_credit_policy (Selection)`
- `partner_outstanding (Monetary)`
- `partner_remaining_credit (Float)`
- `payment_gateway_id (Many2one)`

### XML IDs

- `views/sale_order_views.xml::view_sale_order_form_classification`
- `views/sale_order_views.xml::view_sale_order_search_classification`
- `views/customer_classification_views.xml::view_customer_classification_list`
- `views/customer_classification_views.xml::view_customer_classification_form`
- `views/customer_classification_views.xml::view_customer_classification_search`
- `views/customer_classification_views.xml::action_customer_classification`
- `views/customer_classification_views.xml::menu_customer_classification_root`
- `views/customer_classification_views.xml::menu_customer_classification`
- `views/res_partner_views.xml::view_partner_form_classification`
- `views/res_partner_views.xml::view_partner_search_classification`
- `data/default_data.xml::default_classification_a`
- `data/default_data.xml::default_classification_b`
- `data/default_data.xml::default_classification_c`
- `data/default_data.xml::default_classification_d`
- `data/default_data.xml::default_classification_e`
- `data/classification_cron.xml::ir_cron_auto_classify_action`
- `data/classification_cron.xml::ir_cron_auto_classify`