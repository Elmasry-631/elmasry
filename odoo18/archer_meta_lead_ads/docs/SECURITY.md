# Meta Lead Ads

- **المسار والإصدار:** `odoo18/archer_meta_lead_ads` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Import Meta lead ads into CRM leads

## الصلاحيات والحماية المكتشفة

### ACL

- access_meta_app_credential_user: model=model_meta_app_credential, group=archer_meta_lead_ads.group_meta_lead_ads_user, read/write/create/delete=1/0/0/0
- access_meta_app_credential_manager: model=model_meta_app_credential, group=archer_meta_lead_ads.group_meta_lead_ads_manager, read/write/create/delete=1/1/1/1
- access_meta_page_user: model=model_meta_page, group=archer_meta_lead_ads.group_meta_lead_ads_user, read/write/create/delete=1/1/0/0
- access_meta_page_manager: model=model_meta_page, group=archer_meta_lead_ads.group_meta_lead_ads_manager, read/write/create/delete=1/1/1/1
- access_meta_lead_form_user: model=model_meta_lead_form, group=archer_meta_lead_ads.group_meta_lead_ads_user, read/write/create/delete=1/1/0/0
- access_meta_lead_form_manager: model=model_meta_lead_form, group=archer_meta_lead_ads.group_meta_lead_ads_manager, read/write/create/delete=1/1/1/1
- access_meta_lead_field_mapping_user: model=model_meta_lead_field_mapping, group=archer_meta_lead_ads.group_meta_lead_ads_user, read/write/create/delete=1/1/1/0
- access_meta_lead_field_mapping_manager: model=model_meta_lead_field_mapping, group=archer_meta_lead_ads.group_meta_lead_ads_manager, read/write/create/delete=1/1/1/1
- access_meta_sync_log_user: model=model_meta_sync_log, group=archer_meta_lead_ads.group_meta_lead_ads_user, read/write/create/delete=1/0/0/0
- access_meta_sync_log_manager: model=model_meta_sync_log, group=archer_meta_lead_ads.group_meta_lead_ads_manager, read/write/create/delete=1/0/0/1

### المجموعات وقواعد السجلات

- المجموعات: `group_meta_lead_ads_user`, `group_meta_lead_ads_manager`
- قواعد السجلات: `rule_meta_app_credential_company`, `rule_meta_page_company`, `rule_meta_lead_form_company`, `rule_meta_lead_field_mapping_company`, `rule_meta_sync_log_company`

### واجهات HTTP ورفع الصلاحيات

- '/meta_lead_ads/oauth/callback' (auth=public, csrf=False)

مواضع `sudo()` المرصودة:

- `controllers/oauth.py`
- `models/meta_app_credential.py`
- `models/meta_lead_form.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.