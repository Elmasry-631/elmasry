# Sale Order Barcode Scanner

- **المسار والإصدار:** `odoo18/sale_barcode_scanner` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Scan products by Barcode/QRCode in sales orders using mobile camera or webcam

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_barcode_scanner`.
- خطأ تحميل dependency `product`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_barcode_scanner`.
- خطأ تحميل dependency `barcodes`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_barcode_scanner`.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/sale_order_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
