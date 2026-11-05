# Cheque Tracking Endorsement

- **المسار والإصدار:** `odoo19/cheque_tracking_endorsement` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Cheque endorsement workflow for cheque tracking

## الصلاحيات والحماية المكتشفة

### ACL

- access_cheque_endorsement_user: model=model_cheque_endorsement, group=cheque_tracking.group_cheque_user, read/write/create/delete=1/0/0/0
- access_cheque_endorsement_manager: model=model_cheque_endorsement, group=cheque_tracking_endorsement.group_cheque_endorse, read/write/create/delete=1/1/1/0
- access_cheque_endorsement_cheque_manager: model=model_cheque_endorsement, group=cheque_tracking.group_cheque_manager, read/write/create/delete=1/1/1/0
- access_cheque_endorsement_cheque_admin: model=model_cheque_endorsement, group=cheque_tracking.group_cheque_admin, read/write/create/delete=1/1/1/1
- access_cheque_endorse_wizard: model=model_cheque_endorse_wizard, group=cheque_tracking_endorsement.group_cheque_endorse, read/write/create/delete=1/1/1/1
- access_cheque_endorse_wizard_manager: model=model_cheque_endorse_wizard, group=cheque_tracking.group_cheque_manager, read/write/create/delete=1/1/1/1
- access_cheque_endorse_wizard_admin: model=model_cheque_endorse_wizard, group=cheque_tracking.group_cheque_admin, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_cheque_endorse`
- قواعد السجلات: `cheque_endorsement_company_rule`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.