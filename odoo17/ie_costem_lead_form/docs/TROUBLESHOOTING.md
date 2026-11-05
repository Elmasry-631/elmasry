# ie_costem_lead_form

- **المسار والإصدار:** `odoo17/ie_costem_lead_form` — Odoo 17
- **إصدار الحزمة:** `0.1`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Short (1 phrase/line) summary of the module's purpose

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_costem_lead_form`.
- خطأ تحميل dependency `crm`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_costem_lead_form`.
- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `ie_costem_lead_form`.
- غياب مورد views/form_site_visit_view.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/check_box_fields_view.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 17: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
