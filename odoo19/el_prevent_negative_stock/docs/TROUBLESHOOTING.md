# Prevent Negative Stock

- **المسار والإصدار:** `odoo19/el_prevent_negative_stock` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Prevent negative stock — block stock moves AND sales orders when stock is insufficient

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `base`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_prevent_negative_stock`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_prevent_negative_stock`.
- خطأ تحميل dependency `mail`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_prevent_negative_stock`.
- خطأ تحميل dependency `sale_management`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_prevent_negative_stock`.
- خطأ تحميل dependency `nmo_sale_order_approval_workflow`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_prevent_negative_stock`.
- خطأ تحميل dependency `nmo_stock_user_restriction`: تأكد من إضافته إلى addons_path وتثبيته قبل `el_prevent_negative_stock`.
- غياب مورد security/el_prevent_negative_stock_groups.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/mail_template.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/sequence.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/el_stock_alert_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/menus.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
