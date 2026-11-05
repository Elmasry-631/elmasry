# Sale Payment Gateway

- **المسار والإصدار:** `odoo19/el_nmo_sale_payment_gateway` — Odoo 19
- **إصدار الحزمة:** `19.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Payment Gateway on Sales/Invoice/Delivery + auto-sync Receivable & Payable accounts from gateway to partner

## الصلاحيات والحماية المكتشفة

### ACL

- access_payment_gateway_user: model=model_sale_payment_gateway, group=base.group_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/sale_payment_gateway.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.