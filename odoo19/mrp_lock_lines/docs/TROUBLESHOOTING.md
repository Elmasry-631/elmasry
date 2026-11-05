# MRP Lock Lines

- **المسار والإصدار:** `odoo19/mrp_lock_lines` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Lock all component lines in Manufacturing Order except the last one

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `mrp`: تأكد من إضافته إلى addons_path وتثبيته قبل `mrp_lock_lines`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `mrp_lock_lines`.
- غياب مورد views/mrp_production_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
