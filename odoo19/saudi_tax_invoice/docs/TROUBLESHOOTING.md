# Saudi Tax Invoice

- **المسار والإصدار:** `odoo19/saudi_tax_invoice` — Odoo 19
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Saudi-style tax invoice PDF with action button

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `saudi_tax_invoice`.
- غياب مورد report/templates.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
