# Stock Picking From Invoice

- **المسار والإصدار:** `odoo19/invoice_stock_move` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Stock Picking From Customer/Supplier Invoice

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `account`: تأكد من إضافته إلى addons_path وتثبيته قبل `invoice_stock_move`.
- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `invoice_stock_move`.
- خطأ تحميل dependency `payment`: تأكد من إضافته إلى addons_path وتثبيته قبل `invoice_stock_move`.
- غياب مورد views/account_move_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 19: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
