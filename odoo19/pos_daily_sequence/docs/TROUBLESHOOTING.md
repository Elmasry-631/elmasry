# POS Daily Sequence

- **المسار والإصدار:** `odoo19/pos_daily_sequence` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically reset POS order numbering every day

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `point_of_sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `pos_daily_sequence`.
- خطأ تحميل dependency `mail`: تأكد من إضافته إلى addons_path وتثبيته قبل `pos_daily_sequence`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `pos_daily_sequence`.
- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `pos_daily_sequence`.
- غياب مورد data/ir_sequence_data.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/pos_config_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
