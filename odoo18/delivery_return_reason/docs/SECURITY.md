# Delivery Return Reasons

- **المسار والإصدار:** `odoo18/delivery_return_reason` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** تتبع أسباب رجوع الطلبات مع إحصائيات وتحليلات

## الصلاحيات والحماية المكتشفة

### ACL

- access_delivery_return_reason: model=model_delivery_return_reason, group=base.group_user, read/write/create/delete=1/1/1/0

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/stock_picking.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.