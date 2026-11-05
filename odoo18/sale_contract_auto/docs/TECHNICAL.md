# Sale Contract Auto

- **المسار والإصدار:** `odoo18/sale_contract_auto` — Odoo 18
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically generate contracts from sale orders

## المكونات المكتشفة

- Python: 15 file(s)
- XML: 10 file(s)

### نماذج وامتدادات Odoo

- ContractDocument: model _name
- SaleContract: model _name
- AccountMove: model _inherit
- ContractTitle: model _name
- ContractAmendment: model _name
- ContractTemplate: model _name
- SaleOrder: model _inherit
- ResPartner: model _inherit
- SaleContractLine: model _name
- ContractClause: model _name
- ContractPaymentSchedule: model _name

### الملفات المصدرية ذات الصلة

- `report/contract_report.xml`
- `report/contract_print_template.xml`
- `controllers/__init__.py`
- `controllers/controllers.py`
- `views/contract_template_views.xml`
- `views/sale_contract_views.xml`
- `views/res_partner_view.xml`
- `views/ir_sequence.xml`
- `views/templates.xml`
- `models/contract_document.py`
- `models/sale_contract.py`
- `models/account_move.py`
- `models/contract_title.py`
- `models/contract_amendment.py`
- `models/__init__.py`
- `models/contract_template.py`
- `models/sale_order.py`
- `models/sale_contract_line.py`
- `models/contract_clause.py`
- `models/payment_schedule.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `contract_id (Many2one)`
- `name (Char)`
- `required (Boolean)`
- `document_type (Selection)`
- `attachment_id (Many2one)`
- `uploaded (Boolean)`
- `notes (Text)`
- `name (Char)`
- `partner_id (Many2one)`
- `sale_order_id (Many2one)`
- `contract_date (Date)`
- `amount_total (Monetary)`
- `currency_id (Many2one)`
- `agreement_terms (Text)`
- `contract_line_ids (One2many)`
- `contract_title_name (Many2one)`
- `contract_template_id (Many2one)`
- `state (Selection)`
- `first_party_name (Char)`
- `first_party_registry (Char)`
- `first_party_address (Char)`
- `second_party_name (Char)`
- `second_party_address (Char)`
- `second_party_id_card (Char)`
- `first_party_signature (Binary)`
- `second_party_signature (Binary)`
- `first_party_id (Many2one)`
- `second_party_id (Many2one)`
- `subtotal_total (Monetary)`
- `company_representative (Char)`
- `access_token (Char)`
- `note (Text)`
- `contract_id (Many2one)`
- `name (Char)`
- `contract_id (Many2one)`
- `name (Char)`
- `date (Date)`
- `description (Text)`
- `previous_value (Text)`
- `new_value (Text)`
- `user_id (Many2one)`
- `name (Char)`
- `content (Html)`
- `contract_count (Integer)`
- `contract_template_id (Many2one)`
- `contract_id (Many2one)`
- `contract_title_name (Many2one)`
- `card_id (Char)`
- `contract_id (Many2one)`
- `product_id (Many2one)`
- `name (Char)`
- `quantity (Float)`
- `price_unit (Monetary)`
- `price_subtotal (Monetary)`
- `currency_id (Many2one)`
- `name (Char)`
- `clause_type (Selection)`
- `content (Html)`
- `active (Boolean)`
- `notes (Text)`
- `contract_id (Many2one)`
- `installment_number (Integer)`
- `amount (Monetary)`
- `currency_id (Many2one)`
- `due_date (Date)`
- `invoice_id (Many2one)`
- `state (Selection)`

### XML IDs

- `report/contract_report.xml::paperformat_sale_contract`
- `report/contract_report.xml::action_print_sale_contract`
- `report/contract_print_template.xml::contract_custom_print_template`
- `views/contract_template_views.xml::view_contract_template_tree`
- `views/contract_template_views.xml::view_contract_template_form`
- `views/contract_template_views.xml::action_contract_templates`
- `views/contract_template_views.xml::menu_contract_templates`
- `views/sale_contract_views.xml::view_sale_contract_tree`
- `views/sale_contract_views.xml::view_sale_contract_form`
- `views/sale_contract_views.xml::view_sale_contract_kanban`
- `views/sale_contract_views.xml::view_contract_title_tree`
- `views/sale_contract_views.xml::view_contract_title_form`
- `views/sale_contract_views.xml::view_order_form_inherit_contract_button`
- `views/sale_contract_views.xml::view_order_form_inherit_contract_fields`
- `views/sale_contract_views.xml::action_sale_contracts`
- `views/sale_contract_views.xml::action_contract_title`
- `views/sale_contract_views.xml::menu_contract_root`
- `views/sale_contract_views.xml::menu_contracts`
- `views/sale_contract_views.xml::menu_contract_titles`
- `views/sale_contract_views.xml::menu_contract_customers`
- `views/res_partner_view.xml::added_card_id`
- `views/ir_sequence.xml::seq_sale_contract`
- `views/templates.xml::portal_contract_page`
- `views/templates.xml::signature-pad`
- `views/templates.xml::signature-data`
- `data/contract_data.xml::seq_contract_amendment`
- `data/contract_data.xml::ir_cron_check_contract_expiry`
- `data/contract_data.xml::email_template_contract_state_change`
- `data/contract_data.xml::clause_payment_terms`
- `data/contract_data.xml::clause_warranty`
- `data/contract_data.xml::clause_termination`
- `data/contract_data.xml::clause_confidentiality`
- `data/contract_data.xml::clause_dispute`
- `data/contract_data.xml::clause_penalty`
- `data/contract_data.xml::clause_liability`
- `data/contract_data.xml::ir_cron_auto_invoice_installments`
- `data/mail_templates.xml::email_template_contract_link`