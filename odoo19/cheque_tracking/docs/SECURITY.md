# Cheque Tracking

- **المسار والإصدار:** `odoo19/cheque_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track received and issued cheques with accounting lifecycle entries

## الصلاحيات والحماية المكتشفة

### ACL

- access_cheque_cheque_user: model=model_cheque_cheque, group=cheque_tracking.group_cheque_user, read/write/create/delete=1/1/1/0
- access_cheque_cheque_manager: model=model_cheque_cheque, group=cheque_tracking.group_cheque_manager, read/write/create/delete=1/1/1/1
- access_cheque_deposit_user: model=model_cheque_deposit, group=cheque_tracking.group_cheque_user, read/write/create/delete=1/1/1/0
- access_cheque_deposit_manager: model=model_cheque_deposit, group=cheque_tracking.group_cheque_manager, read/write/create/delete=1/1/1/1
- access_cheque_return_user: model=model_cheque_return, group=cheque_tracking.group_cheque_user, read/write/create/delete=1/0/0/0
- access_cheque_return_manager: model=model_cheque_return, group=cheque_tracking.group_cheque_manager, read/write/create/delete=1/1/1/1
- access_cheque_return_reason_user: model=model_cheque_return_reason, group=cheque_tracking.group_cheque_user, read/write/create/delete=1/0/0/0
- access_cheque_return_reason_admin: model=model_cheque_return_reason, group=cheque_tracking.group_cheque_admin, read/write/create/delete=1/1/1/1
- access_cheque_deposit_wizard: model=model_cheque_deposit_wizard, group=cheque_tracking.group_cheque_user, read/write/create/delete=1/1/1/1
- access_cheque_return_wizard: model=model_cheque_return_wizard, group=cheque_tracking.group_cheque_manager, read/write/create/delete=1/1/1/1
- access_cheque_print_wizard: model=model_cheque_print_wizard, group=cheque_tracking.group_cheque_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_cheque_user`, `group_cheque_manager`, `group_cheque_admin`
- قواعد السجلات: `cheque_cheque_company_rule`, `cheque_deposit_company_rule`, `cheque_return_company_rule`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/deposit.py`
- `models/cheque_return.py`
- `models/cheque.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.