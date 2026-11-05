# IE Print Document Linked Order

- **المسار والإصدار:** `odoo17/ie_print_document_linked_order` — Odoo 17
- **إصدار الحزمة:** `0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Show all product attachments directly from Quotation.

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_print_document_linked_order`.
- خطأ تحميل dependency `sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_print_document_linked_order`.
- غياب مورد views/sale_order_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 17: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
