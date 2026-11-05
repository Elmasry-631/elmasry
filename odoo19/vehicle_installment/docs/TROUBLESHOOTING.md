# Vehicle Installment Management

- **المسار والإصدار:** `odoo19/vehicle_installment` — Odoo 19
- **إصدار الحزمة:** `19.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage vehicle installments with automatic calculation

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `vehicle_installment`.
- خطأ تحميل dependency `mail`: تأكد من إضافته إلى addons_path وتثبيته قبل `vehicle_installment`.
- خطأ تحميل dependency `fleet`: تأكد من إضافته إلى addons_path وتثبيته قبل `vehicle_installment`.
- خطأ تحميل dependency `hr`: تأكد من إضافته إلى addons_path وتثبيته قبل `vehicle_installment`.
- خطأ تحميل dependency `hr_payroll`: تأكد من إضافته إلى addons_path وتثبيته قبل `vehicle_installment`.
- غياب مورد security/security.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/vehicle_installment_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
