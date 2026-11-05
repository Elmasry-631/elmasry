# Sale Order Contract

- **المسار والإصدار:** `odoo18/sale_order_contract` — Odoo 18
- **إصدار الحزمة:** `0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically generate contracts from sale orders.

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_order_contract`.
- خطأ تحميل dependency `sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_order_contract`.
- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_order_contract`.
- غياب مورد report/contract_report.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد report/contract_print_template.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
