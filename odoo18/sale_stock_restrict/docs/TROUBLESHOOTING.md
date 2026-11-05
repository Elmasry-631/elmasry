# Sale Stock Restrict

- **المسار والإصدار:** `odoo18/sale_stock_restrict` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Module helps to restrict out of stock products

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_stock_restrict`.
- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_stock_restrict`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_stock_restrict`.
- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_stock_restrict`.
- غياب مورد views/res_config_settings_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/sale_order.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
