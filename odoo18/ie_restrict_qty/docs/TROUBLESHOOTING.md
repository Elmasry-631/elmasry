# Ie Restrict Qty

- **المسار والإصدار:** `odoo18/ie_restrict_qty` — Odoo 18
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Brief description of the module

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_restrict_qty`.
- خطأ تحميل dependency `mail`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_restrict_qty`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_restrict_qty`.
- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_restrict_qty`.
- غياب مورد views/ie_restrict_qty_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
