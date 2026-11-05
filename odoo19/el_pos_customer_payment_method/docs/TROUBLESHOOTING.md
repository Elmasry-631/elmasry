# POS Customer Payment Method

- **المسار والإصدار:** `odoo19/el_pos_customer_payment_method` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Restrict POS payment methods per customer, with POS-level defaults for customers without a specific list.

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `point_of_sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_pos_customer_payment_method`.
- غياب مورد views/res_partner_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/res_config_settings_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
