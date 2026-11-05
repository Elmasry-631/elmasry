# Meta Lead Ads

- **المسار والإصدار:** `odoo18/archer_meta_lead_ads` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Import Meta lead ads into CRM leads

## المكونات المكتشفة

- Python: 12 file(s)
- XML: 9 file(s)

### نماذج وامتدادات Odoo

- MetaPage: model _name
- CrmLead: model _inherit
- MetaAppCredential: model _name
- MetaLeadForm: model _name
- ResConfigSettings: model _inherit
- MetaSyncLog: model _name
- MetaLeadFieldMapping: model _name

### الملفات المصدرية ذات الصلة

- `controllers/__init__.py`
- `controllers/oauth.py`
- `views/res_config_settings_views.xml`
- `views/meta_lead_form_views.xml`
- `views/menus.xml`
- `views/meta_app_credential_views.xml`
- `views/crm_lead_views.xml`
- `views/meta_page_views.xml`
- `views/meta_sync_log_views.xml`
- `models/meta_page.py`
- `models/crm_lead.py`
- `models/meta_app_credential.py`
- `models/meta_lead_form.py`
- `models/res_config_settings.py`
- `models/meta_sync_log.py`
- `models/__init__.py`
- `models/meta_lead_field_mapping.py`
- `security/security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `name (Char)`
- `company_id (Many2one)`
- `credential_id (Many2one)`
- `page_id (Char)`
- `page_access_token (Text)`
- `category (Char)`
- `platform (Selection)`
- `instagram_account_id (Char)`
- `fan_count (Integer)`
- `is_active (Boolean)`
- `form_ids (One2many)`
- `form_count (Integer)`
- `lead_count (Integer)`
- `x_meta_leadgen_id (Char)`
- `x_meta_platform (Selection)`
- `x_meta_page_id (Many2one)`
- `x_meta_form_id (Many2one)`
- `x_meta_campaign_name (Char)`
- `x_meta_ad_name (Char)`
- `x_meta_created_time (Datetime)`
- `name (Char)`
- `company_id (Many2one)`
- `app_id (Char)`
- `app_secret (Char)`
- `user_access_token (Text)`
- `token_expiry_date (Datetime)`
- `state (Selection)`
- `redirect_uri (Char)`
- `page_ids (One2many)`
- `page_count (Integer)`
- `sync_issue_count (Integer)`
- `last_sync_date (Datetime)`
- `notes (Html)`
- `active (Boolean)`
- `name (Char)`
- `company_id (Many2one)`
- `page_id (Many2one)`
- `form_id (Char)`
- `status (Char)`
- `locale (Char)`
- `created_time (Datetime)`
- `crm_team_id (Many2one)`
- `utm_source_id (Many2one)`
- `utm_medium_id (Many2one)`
- `fetch_frequency_minutes (Selection)`
- `mapping_ids (One2many)`
- `mapping_count (Integer)`
- `lead_count (Integer)`
- `last_fetch_date (Datetime)`
- `questions_json (Text)`
- `active (Boolean)`
- `name (Char)`
- `company_id (Many2one)`
- `level (Selection)`
- `category (Char)`
- `message (Text)`
- `credential_id (Many2one)`
- `page_id (Many2one)`
- `form_id (Many2one)`
- `lead_id (Many2one)`
- `sequence (Integer)`
- `form_id (Many2one)`
- `company_id (Many2one)`
- `meta_field_key (Char)`
- `odoo_field_id (Many2one)`
- `odoo_field_name (Char)`
- `odoo_field_ttype (Selection)`
- `relation (Char)`
- `lookup_field (Char)`
- `transform (Selection)`
- `is_default (Boolean)`
- `active (Boolean)`

### XML IDs

- `views/res_config_settings_views.xml::view_res_config_settings_meta_lead_ads`
- `views/meta_lead_form_views.xml::view_meta_lead_form_list`
- `views/meta_lead_form_views.xml::view_meta_lead_form_form`
- `views/meta_lead_form_views.xml::view_meta_lead_form_search`
- `views/meta_lead_form_views.xml::action_meta_lead_form`
- `views/menus.xml::menu_meta_lead_ads_root`
- `views/menus.xml::menu_meta_lead_ads_credentials`
- `views/menus.xml::menu_meta_lead_ads_pages`
- `views/menus.xml::menu_meta_lead_ads_forms`
- `views/menus.xml::menu_meta_lead_ads_logs`
- `views/meta_app_credential_views.xml::view_meta_app_credential_list`
- `views/meta_app_credential_views.xml::view_meta_app_credential_search`
- `views/meta_app_credential_views.xml::view_meta_app_credential_form`
- `views/meta_app_credential_views.xml::action_meta_app_credential`
- `views/crm_lead_views.xml::view_crm_lead_form_meta_inherit`
- `views/crm_lead_views.xml::view_crm_lead_search_meta_inherit`
- `views/meta_page_views.xml::view_meta_page_list`
- `views/meta_page_views.xml::view_meta_page_form`
- `views/meta_page_views.xml::view_meta_page_search`
- `views/meta_page_views.xml::action_meta_page`
- `views/meta_sync_log_views.xml::view_meta_sync_log_list`
- `views/meta_sync_log_views.xml::view_meta_sync_log_form`
- `views/meta_sync_log_views.xml::view_meta_sync_log_search`
- `views/meta_sync_log_views.xml::action_meta_sync_log`
- `data/ir_cron_data.xml::ir_cron_meta_fetch_leads`
- `data/ir_cron_data.xml::ir_cron_meta_check_token_expiry`
- `data/ir_cron_data.xml::ir_cron_meta_cleanup_sync_logs`
- `security/security.xml::module_category_meta_lead_ads`
- `security/security.xml::group_meta_lead_ads_user`
- `security/security.xml::group_meta_lead_ads_manager`
- `security/security.xml::rule_meta_app_credential_company`
- `security/security.xml::rule_meta_page_company`
- `security/security.xml::rule_meta_lead_form_company`
- `security/security.xml::rule_meta_lead_field_mapping_company`
- `security/security.xml::rule_meta_sync_log_company`