# Partner Request

- **المسار والإصدار:** `odoo19/partner_request` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for creating new customers via sales requests.

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `partner_request`.
- خطأ تحميل dependency `sales_team`: تأكد من إضافته إلى addons_path وتثبيته قبل `partner_request`.
- خطأ تحميل dependency `customer_classification`: تأكد من إضافته إلى addons_path وتثبيته قبل `partner_request`.
- غياب مورد security/partner_request_security.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/partner_request_data.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/partner_request_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/partner_request_menus.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
