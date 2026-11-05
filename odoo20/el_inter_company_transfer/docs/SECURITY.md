# Inter Company Internal Transfer

- **المسار والإصدار:** `odoo20/el_inter_company_transfer` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Request stock transfers between warehouses of different companies

## الصلاحيات والحماية المكتشفة

### ACL

- لا توجد عناصر معلنة في ملفات الموديول.

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/stock_warehouse.py`
- `models/transfer_request.py`
- `models/transfer_request_line.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.