# Invoice Tracking

- **المسار والإصدار:** `odoo19/invoice_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Brief description of the module

## المكونات المكتشفة

- Python: 13 file(s)
- XML: 9 file(s)

### نماذج وامتدادات Odoo

- ResCompany: model _inherit
- InvoiceTracking: model _name
- PartnerCode: model _name
- ResPartner: model _inherit
- PurchaseOrder: model _inherit
- ResConfigSettings: model _inherit
- AccountMove: model _inherit
- Well: model _name
- CheckTracking: model _name

### الملفات المصدرية ذات الصلة

- `views/check_tracking_views.xml`
- `views/well_view.xml`
- `views/res_config_settings_views.xml`
- `views/invoice_tracking_views.xml`
- `views/res_partner_views.xml`
- `views/account_move_views.xml`
- `views/menu_item.xml`
- `views/purchase_order_views.xml`
- `models/res_company.py`
- `models/invoice_tracking.py`
- `models/res_partner.py`
- `models/purshase_order.py`
- `models/res_config_settings.py`
- `models/account_move.py`
- `models/__init__.py`
- `models/well.py`
- `models/check_tracking.py`
- `security/ir.model.access.csv`

### حقول معلنة

- `cheque_received_account_id (Many2one)`
- `cheque_under_collection_account_id (Many2one)`
- `cheque_issued_account_id (Many2one)`
- `name (Char)`
- `bill_reference (Char)`
- `code_id (Many2one)`
- `partner_id (Many2one)`
- `purchase_id (Many2one)`
- `vendor_bill_id (Many2one)`
- `purchase_reference (Char)`
- `received_date (Date)`
- `bill_date (Date)`
- `del_to_administration (Date)`
- `rec_from_administration (Date)`
- `purchase_line_ids (One2many)`
- `currency_id (Many2one)`
- `egp_currency_id (Many2one)`
- `usd_currency_id (Many2one)`
- `total_invoice_amount (Monetary)`
- `approved_egp_amount (Monetary)`
- `approved_usd_amount (Monetary)`
- `rate_today (Float)`
- `usd_percentage (Float)`
- `egp_percentage (Float)`
- `is_egp_currency (Boolean)`
- `total_invoice_amount_egp (Monetary)`
- `total_invoice_amount_usd (Monetary)`
- `well_number (Many2one)`
- `status_id (Many2one)`
- `check_status (Selection)`
- `status (Selection)`
- `name (Char)`
- `code_id (Many2one)`
- `tracking_count (Integer)`
- `cheque_received_account_id (Many2one)`
- `cheque_under_collection_account_id (Many2one)`
- `cheque_issued_account_id (Many2one)`
- `code_id (Many2one)`
- `check_tracking_id (Many2one)`
- `check_stage (Selection)`
- `name (Char)`
- `name (Char)`
- `company_id (Many2one)`
- `check_type (Selection)`
- `partner_id (Many2one)`
- `amount (Monetary)`
- `currency_id (Many2one)`
- `secondary_amount (Monetary)`
- `secondary_currency_id (Many2one)`
- `date_issue (Date)`
- `date_due (Date)`
- `bank_id (Many2one)`
- `journal_id (Many2one)`
- `attachment_ids (Many2many)`
- `receivable_account_id (Many2one)`
- `payable_account_id (Many2one)`
- `bank_account_id (Many2one)`
- `move_ids (One2many)`
- `move_count (Integer)`
- `status (Selection)`

### XML IDs

- `views/check_tracking_views.xml::check_track_action`
- `views/check_tracking_views.xml::view_check_tracking_tree`
- `views/check_tracking_views.xml::view_check_tracking_form`
- `views/well_view.xml::well_number_action`
- `views/well_view.xml::view_oil_well_tree`
- `views/well_view.xml::view_oil_well_form`
- `views/res_config_settings_views.xml::res_config_settings_view_form_inherit_check_tracking`
- `views/res_config_settings_views.xml::check_tracking_cheque_accounts`
- `views/invoice_tracking_views.xml::action_invoice_tracking`
- `views/invoice_tracking_views.xml::view_invoice_tracking_form`
- `views/invoice_tracking_views.xml::view_invoice_tracking_tree`
- `views/invoice_tracking_views.xml::add_purchase_order_button_in_invoice_tracking`
- `views/res_partner_views.xml::vendor_code_action`
- `views/res_partner_views.xml::inherit_res_partner_form_view`
- `views/res_partner_views.xml::vedor_code_view_form`
- `views/res_partner_views.xml::vendor_code_view_list`
- `views/account_move_views.xml::account_move_view_form`
- `views/menu_item.xml::menu_invoice_tracking_main`
- `views/menu_item.xml::vendor_code_id`
- `views/menu_item.xml::well_number_code`
- `views/menu_item.xml::checks_track`
- `views/purchase_order_views.xml::view_purchase_order_form_inherit`
- `views/purchase_order_views.xml::view_purchase_order_form_inherit_btn_box`
- `data/invoice_tracking_sequence.xml::seq_invoice_tracking`