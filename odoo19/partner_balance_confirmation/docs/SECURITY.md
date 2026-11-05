# Balance Confirmation

- **المسار والإصدار:** `odoo19/partner_balance_confirmation` — Odoo 19
- **إصدار الحزمة:** `19.0.3.6.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Customer Balance Confirmation (Imdad / Namo templates)

## الصلاحيات والحماية المكتشفة

### ACL

- access_balance_confirmation_wizard: model=model_balance_confirmation_wizard, group=base.group_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.