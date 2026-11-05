# Purchase Actual Quantity

- **المسار والإصدار:** `odoo18/el_purchase_actual_qty` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Actual purchase quantity with preserved value, dashboard and reporting

## الصلاحيات والحماية المكتشفة

### ACL

- access_purchase_actual_report_user: model=model_el_purchase_actual_report, group=purchase.group_purchase_user, read/write/create/delete=1/0/0/0
- access_purchase_actual_report_manager: model=model_el_purchase_actual_report, group=purchase.group_purchase_manager, read/write/create/delete=1/0/0/0

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- '/purchase_actual_qty/export/csv' (auth=user)

مواضع `sudo()` المرصودة:

- `models/purchase_order_line.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.