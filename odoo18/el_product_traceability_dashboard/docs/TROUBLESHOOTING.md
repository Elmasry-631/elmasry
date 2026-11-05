# Product Traceability Dashboard

- **المسار والإصدار:** `odoo18/el_product_traceability_dashboard` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Product traceability dashboard with returns, scrap and manufacturing genealogy

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_product_traceability_dashboard`.
- خطأ تحميل dependency `purchase`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_product_traceability_dashboard`.
- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_product_traceability_dashboard`.
- خطأ تحميل dependency `mrp`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_product_traceability_dashboard`.
- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_product_traceability_dashboard`.
- غياب مورد security/security.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/product_traceability_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/product_traceability_report_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/product_traceability_menus.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد report/traceability_report_templates.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
