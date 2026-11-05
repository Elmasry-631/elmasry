# Sale Order Barcode Scanner

- **المسار والإصدار:** `odoo18/sale_barcode_scanner` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Scan products by Barcode/QRCode in sales orders using mobile camera or webcam

## الصلاحيات والحماية المكتشفة

### ACL

- access_sale_order_barcode: model=sale.model_sale_order, group=sales_team.group_sale_salesman, read/write/create/delete=1/1/1/0
- access_sale_order_line_barcode: model=sale.model_sale_order_line, group=sales_team.group_sale_salesman, read/write/create/delete=1/1/1/1
- access_product_product_barcode: model=product.model_product_product, group=sales_team.group_sale_salesman, read/write/create/delete=1/0/0/0

### المجموعات وقواعد السجلات

- المجموعات: لا توجد سجلات مجموعات ظاهرة في XML.
- قواعد السجلات: لا توجد سجلات ir.rule ظاهرة في XML.

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.