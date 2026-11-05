# Commission Types

- **المسار والإصدار:** `odoo19/el_commission_type` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage sales commission types by team member role

## الصلاحيات والحماية المكتشفة

### ACL

- access_commission_type_all: model=model_sales_commission_type, group=base.group_user, read/write/create/delete=1/0/0/0
- access_commission_type_user: model=model_sales_commission_type, group=group_commission_user, read/write/create/delete=1/1/1/0
- access_commission_type_manager: model=model_sales_commission_type, group=group_commission_manager, read/write/create/delete=1/1/1/1
- access_commission_all: model=model_sales_commission, group=base.group_user, read/write/create/delete=1/0/0/0
- access_commission_user: model=model_sales_commission, group=group_commission_user, read/write/create/delete=1/1/1/0
- access_commission_manager: model=model_sales_commission, group=group_commission_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_commission_user`, `group_commission_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.