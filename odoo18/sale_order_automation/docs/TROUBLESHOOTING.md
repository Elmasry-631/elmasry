# Sale Order Automation

- **المسار والإصدار:** `odoo18/sale_order_automation` — Odoo 18
- **إصدار الحزمة:** `1.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Enable auto sale workflow with sale order confirmation. Include operations like Auto Create Invoice, Auto Validate Invoice and Auto Transfer Delivery Order.

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `sale_stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `sale_order_automation`.
- غياب مورد views/stock_warehouse.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
