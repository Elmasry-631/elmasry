# Meta Lead Ads

- **المسار والإصدار:** `odoo18/archer_meta_lead_ads` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Import Meta lead ads into CRM leads

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Meta Lead Ads
- المستخدم يبدأ من قائمة: Credentials
- المستخدم يبدأ من قائمة: Pages
- المستخدم يبدأ من قائمة: Forms
- المستخدم يبدأ من قائمة: Sync Issues
- النموذج/الامتداد المعني: MetaPage: model _name
- النموذج/الامتداد المعني: CrmLead: model _inherit
- النموذج/الامتداد المعني: MetaAppCredential: model _name
- النموذج/الامتداد المعني: MetaLeadForm: model _name
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: MetaSyncLog: model _name
- النموذج/الامتداد المعني: MetaLeadFieldMapping: model _name
- العملية البرمجية المتاحة: `_compute_counts` في `models/meta_page.py`
- العملية البرمجية المتاحة: `action_view_forms` في `models/meta_page.py`
- العملية البرمجية المتاحة: `action_view_leads` في `models/meta_page.py`
- العملية البرمجية المتاحة: `action_fetch_forms` في `models/meta_page.py`
- العملية البرمجية المتاحة: `_compute_redirect_uri` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `_compute_counts` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `_validate_oauth_state` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `action_generate_token` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `action_exchange_oauth_code` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `action_test_connection` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `action_fetch_pages` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `action_view_pages` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `action_view_sync_issues` في `models/meta_app_credential.py`
- العملية البرمجية المتاحة: `_compute_counts` في `models/meta_lead_form.py`
- العملية البرمجية المتاحة: `action_view_leads` في `models/meta_lead_form.py`
- العملية البرمجية المتاحة: `action_fetch_form_fields` في `models/meta_lead_form.py`
- العملية البرمجية المتاحة: `_import_meta_lead` في `models/meta_lead_form.py`
- العملية البرمجية المتاحة: `action_fetch_leads` في `models/meta_lead_form.py`
- العملية البرمجية المتاحة: `action_open_meta_lead_ads` في `models/res_config_settings.py`
- العملية البرمجية المتاحة: `_compute_name` في `models/meta_sync_log.py`
- العملية البرمجية المتاحة: `log` في `models/meta_sync_log.py`
- العملية البرمجية المتاحة: `_cron_cleanup_old_logs` في `models/meta_sync_log.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
