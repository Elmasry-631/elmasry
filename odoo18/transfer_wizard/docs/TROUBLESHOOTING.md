# trade_paints_wizard

- **المسار والإصدار:** `odoo18/transfer_wizard` — Odoo 18
- **إصدار الحزمة:** `1.1`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Transfer Wizard

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `transfer_wizard`.
- خطأ تحميل dependency `sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `transfer_wizard`.
- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `transfer_wizard`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `transfer_wizard`.
- خطأ تحميل dependency `purchase`: تأكد من إضافته إلى addons_path وتثبيته قبل `transfer_wizard`.
- غياب مورد wizard/transfer_wizard.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
