# Delivery Return Reasons

- **المسار والإصدار:** `odoo18/delivery_return_reason` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** تتبع أسباب رجوع الطلبات مع إحصائيات وتحليلات

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `stock`: تأكد من إضافته إلى addons_path وتثبيته قبل `delivery_return_reason`.
- خطأ تحميل dependency `el_kitchen_receipt`: تأكد من إضافته إلى addons_path وتثبيته قبل `delivery_return_reason`.
- غياب مورد security/ir.model.access.csv: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد data/delivery_return_reason_data.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/delivery_return_reason_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/stock_picking_return_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/stock_picking_views.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/stock_picking_search.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- غياب مورد views/stock_picking_analysis.xml: تحقق من ملفات manifest الموجودة تحت `data` و`assets` ومطابقتها لمسارات الملفات.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
