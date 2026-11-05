# Restrict Journal for Users (Whitelist)

- **المسار والإصدار:** `odoo18/el_restrict_journal` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Per-user journal whitelist — only allowed journals are visible

## الصلاحيات والحماية المكتشفة

### ACL

- access_res_users_restrict_journal_admin: model=base.model_res_users, group=base.group_system, read/write/create/delete=1/1/1/1
- access_res_users_restrict_journal_manager: model=base.model_res_users, group=el_restrict_journal.group_restrict_journal_manager, read/write/create/delete=1/1/0/0

### المجموعات وقواعد السجلات

- المجموعات: `group_restrict_journal_user`, `group_restrict_journal_manager`
- قواعد السجلات: `rule_journal_allowed_only`, `rule_move_allowed_only`, `rule_payment_allowed_only`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/res_users.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.