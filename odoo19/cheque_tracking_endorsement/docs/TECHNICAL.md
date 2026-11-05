# Cheque Tracking Endorsement

- **المسار والإصدار:** `odoo19/cheque_tracking_endorsement` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Cheque endorsement workflow for cheque tracking

## المكونات المكتشفة

- Python: 10 file(s)
- XML: 8 file(s)

### نماذج وامتدادات Odoo

- ResCompany: model _inherit
- ResConfigSettings: model _inherit
- AccountMove: model _inherit
- ChequeEndorsement: model _name
- ChequeCheque: model _inherit
- ChequeEndorseWizard: model _name

### الملفات المصدرية ذات الصلة

- `views/cheque_views.xml`
- `views/res_config_settings_views.xml`
- `views/menus.xml`
- `views/account_move_views.xml`
- `views/endorsement_views.xml`
- `models/res_company.py`
- `models/res_config_settings.py`
- `models/account_move.py`
- `models/cheque_endorsement.py`
- `models/__init__.py`
- `models/cheque.py`
- `security/groups.xml`
- `security/ir.model.access.csv`
- `security/endorsement_security.xml`

### حقول معلنة

- `cheque_allow_post_dated_endorsement (Boolean)`
- `cheque_endorsement_reminder_days (Integer)`
- `cheque_endorsement_payable_account_id (Many2one)`
- `cheque_endorsement_bill_account_id (Many2one)`
- `cheque_allow_post_dated_endorsement (Boolean)`
- `cheque_endorsement_reminder_days (Integer)`
- `cheque_endorsement_payable_account_id (Many2one)`
- `cheque_endorsement_bill_account_id (Many2one)`
- `cheque_endorsement_id (Many2one)`
- `cheque_stage (Selection)`
- `name (Char)`
- `cheque_id (Many2one)`
- `company_id (Many2one)`
- `currency_id (Many2one)`
- `amount (Monetary)`
- `endorser_id (Many2one)`
- `endorsee_id (Many2one)`
- `endorsement_date (Date)`
- `reason (Text)`
- `sequence (Integer)`
- `move_id (Many2one)`
- `vendor_bill_id (Many2one)`
- `state (Selection)`
- `user_id (Many2one)`
- `is_endorsable (Boolean)`
- `is_crossed (Boolean)`
- `original_beneficiary_id (Many2one)`
- `current_endorsee_id (Many2one)`
- `endorsement_ids (One2many)`
- `endorsement_count (Integer)`
- `state (Selection)`
- `cheque_id (Many2one)`
- `current_beneficiary_id (Many2one)`
- `endorsee_partner_id (Many2one)`
- `endorsement_date (Date)`
- `reason (Text)`
- `create_vendor_bill (Boolean)`

### XML IDs

- `views/cheque_views.xml::view_cheque_cheque_list_endorsement`
- `views/cheque_views.xml::view_cheque_cheque_form_endorsement`
- `views/cheque_views.xml::view_cheque_cheque_search_endorsement`
- `views/res_config_settings_views.xml::res_config_settings_view_form_endorsement`
- `views/menus.xml::menu_cheque_endorsements`
- `views/account_move_views.xml::view_move_form_cheque_endorsement`
- `views/endorsement_views.xml::view_cheque_endorsement_list`
- `views/endorsement_views.xml::view_cheque_endorsement_form`
- `views/endorsement_views.xml::view_cheque_endorsement_search`
- `views/endorsement_views.xml::action_cheque_endorsement`
- `wizards/endorse_wizard_views.xml::view_cheque_endorse_wizard_form`
- `security/groups.xml::group_cheque_endorse`
- `security/endorsement_security.xml::cheque_endorsement_company_rule`