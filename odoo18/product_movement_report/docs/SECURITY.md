# Product Movement Lifecycle Report

- **المسار والإصدار:** `odoo18/product_movement_report` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Full movement history of a product/lot from first receipt until fully sold

## الصلاحيات والحماية المكتشفة

### ACL

- access_product_movement_line: model=model_product_movement_line, group=base.group_user, read/write/create/delete=1/1/1/1
- access_product_movement_wizard: model=model_product_movement_wizard, group=base.group_user, read/write/create/delete=1/1/1/0
- access_product_movement_summary: model=model_product_movement_summary, group=base.group_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.