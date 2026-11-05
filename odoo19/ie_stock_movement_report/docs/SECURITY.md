# Stock Movement Report

- **المسار والإصدار:** `odoo19/ie_stock_movement_report` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** PDF report of inventory movements with opening/closing balance and running value.

## الصلاحيات والحماية المكتشفة

### ACL

- access_stock_movement_report_wizard_user: model=model_stock_movement_report_wizard, group=group_stock_movement_report_user, read/write/create/delete=1/1/1/0
- access_stock_movement_report_wizard_manager: model=model_stock_movement_report_wizard, group=group_stock_movement_report_manager, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_stock_movement_report_user`, `group_stock_movement_report_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.