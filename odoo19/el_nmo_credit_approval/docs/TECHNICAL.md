# El-Nmo - Credit Limit Approval Workflow

- **المسار والإصدار:** `odoo19/el_nmo_credit_approval` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for sale orders exceeding customer credit limits.

## المكونات المكتشفة

- Python: 10 file(s)
- XML: 7 file(s)

### نماذج وامتدادات Odoo

- CreditApprovalRequest: model _name
- CreditRejectionReason: model _name
- SaleOrder: model _inherit
- CreditApprovalWizard: model _name

### الملفات المصدرية ذات الصلة

- `views/menu.xml`
- `views/credit_rejection_reason_views.xml`
- `views/sale_order_views.xml`
- `views/credit_approval_request_views.xml`
- `models/credit_approval_request.py`
- `models/__init__.py`
- `models/credit_rejection_reason.py`
- `models/sale_order.py`
- `security/groups.xml`
- `security/ir.model.access.csv`
- `wizard/credit_approval_wizard.py`
- `wizard/__init__.py`
- `wizard/credit_approval_wizard_views.xml`

### حقول معلنة

- `name (Char)`
- `sale_order_id (Many2one)`
- `partner_id (Many2one)`
- `requested_by (Many2one)`
- `supervisor_id (Many2one)`
- `state (Selection)`
- `credit_limit (Float)`
- `credit_used (Float)`
- `order_amount (Monetary)`
- `exceeded_by (Float)`
- `currency_id (Many2one)`
- `rejection_reason_id (Many2one)`
- `rejection_notes (Text)`
- `approval_date (Datetime)`
- `company_id (Many2one)`
- `name (Char)`
- `description (Text)`
- `sequence (Integer)`
- `active (Boolean)`
- `company_id (Many2one)`
- `credit_approval_id (Many2one)`
- `credit_approval_state (Selection)`
- `is_credit_blocked (Boolean)`
- `sale_order_id (Many2one)`
- `request_id (Many2one)`
- `request_state (Selection)`
- `customer_id (Many2one)`
- `credit_limit (Float)`
- `credit_used (Float)`
- `order_amount (Monetary)`
- `exceeded_by (Float)`
- `currency_id (Many2one)`
- `rejection_reason_id (Many2one)`
- `rejection_notes (Text)`

### XML IDs

- `views/menu.xml::menu_credit_approval_root`
- `views/menu.xml::menu_credit_approval_requests`
- `views/menu.xml::menu_credit_rejection_reasons`
- `views/credit_rejection_reason_views.xml::view_credit_rejection_reason_list`
- `views/credit_rejection_reason_views.xml::view_credit_rejection_reason_form`
- `views/credit_rejection_reason_views.xml::view_credit_rejection_reason_search`
- `views/credit_rejection_reason_views.xml::action_credit_rejection_reason`
- `views/sale_order_views.xml::view_sale_order_form_credit_approval`
- `views/sale_order_views.xml::view_sale_order_list_credit_approval`
- `views/sale_order_views.xml::view_sale_order_search_credit_approval`
- `views/credit_approval_request_views.xml::seq_credit_approval_request`
- `views/credit_approval_request_views.xml::email_template_credit_approval`
- `views/credit_approval_request_views.xml::view_credit_approval_request_list`
- `views/credit_approval_request_views.xml::view_credit_approval_request_form`
- `views/credit_approval_request_views.xml::view_credit_approval_request_search`
- `views/credit_approval_request_views.xml::action_credit_approval_request`
- `data/default_rejection_reasons.xml::rejection_reason_insufficient_payment_history`
- `data/default_rejection_reasons.xml::rejection_reason_overdue_payments`
- `data/default_rejection_reasons.xml::rejection_reason_credit_limit_exceeded`
- `data/default_rejection_reasons.xml::rejection_reason_high_risk_customer`
- `data/default_rejection_reasons.xml::rejection_reason_classification_downgrade`
- `data/default_rejection_reasons.xml::rejection_reason_management_decision`
- `data/default_rejection_reasons.xml::rejection_reason_incomplete_documents`
- `data/default_rejection_reasons.xml::rejection_reason_other`
- `security/groups.xml::privilege_credit_approval`
- `security/groups.xml::group_credit_approval_salesperson`
- `security/groups.xml::group_credit_approval_supervisor`
- `security/groups.xml::group_credit_approval_manager`
- `wizard/credit_approval_wizard_views.xml::credit_approval_wizard_form_view`
- `wizard/credit_approval_wizard_views.xml::credit_approval_wizard_action`