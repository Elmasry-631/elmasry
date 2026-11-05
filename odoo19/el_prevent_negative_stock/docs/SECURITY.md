# Prevent Negative Stock

- **المسار والإصدار:** `odoo19/el_prevent_negative_stock` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Prevent negative stock — block stock moves AND sales orders when stock is insufficient

## الصلاحيات والحماية المكتشفة

### ACL

- access_el_stock_alert_user: model=model_el_stock_alert, group=group_alert_user, read/write/create/delete=1/0/0/0
- access_el_stock_alert_manager: model=model_el_stock_alert, group=group_alert_manager, read/write/create/delete=1/1/1/1
- access_el_stock_alert_system: model=model_el_stock_alert, group=base.group_system, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_alert_user`, `group_alert_manager`
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.