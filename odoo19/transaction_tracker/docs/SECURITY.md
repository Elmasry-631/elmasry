# Transaction Tracker

- **المسار والإصدار:** `odoo19/transaction_tracker` — Odoo 19
- **إصدار الحزمة:** `1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track all user transactions across every Odoo module

## الصلاحيات والحماية المكتشفة

### ACL

- access_transaction_log_manager: model=model_transaction_log, group=group_transaction_tracker_manager, read/write/create/delete=1/0/0/0
- access_transaction_log_user: model=model_transaction_log, group=group_transaction_tracker_user, read/write/create/delete=1/0/0/0
- access_tracker_config_manager: model=model_transaction_tracker_config, group=group_transaction_tracker_manager, read/write/create/delete=1/1/1/0

### المجموعات وقواعد السجلات

- المجموعات: `group_transaction_tracker_manager`, `group_transaction_tracker_user`
- قواعد السجلات: `transaction_log_manager_rule`, `transaction_log_user_rule`, `tracker_config_manager_rule`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/tracker_config.py`
- `models/transaction_log.py`
- `models/base_hook.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.