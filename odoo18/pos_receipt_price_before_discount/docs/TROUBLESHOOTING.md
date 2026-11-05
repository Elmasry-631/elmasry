# POS Receipt: Price Before Discount

- **المسار والإصدار:** `odoo18/pos_receipt_price_before_discount` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Show product list price (before discount) under each receipt line when discounted

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `point_of_sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `pos_receipt_price_before_discount`.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
