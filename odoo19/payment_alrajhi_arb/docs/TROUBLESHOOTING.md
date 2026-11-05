# Al Rajhi Bank (ARB) Payment Gateway

- **المسار والإصدار:** `odoo19/payment_alrajhi_arb` — Odoo 19
- **إصدار الحزمة:** `19.0.1.4.12`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Official-style ARB integration: token API, encrypted trandata, bank-hosted redirect, KSA Card/Mada checkout (Odoo 19).

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `payment`: تأكد من إضافته إلى addons_path وتثبيته قبل `payment_alrajhi_arb`.
- غياب مورد views/arb_redirect_form_templates.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/payment_provider_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/payment_provider_data.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
