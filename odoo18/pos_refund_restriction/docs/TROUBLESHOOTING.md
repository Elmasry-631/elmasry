# POS Refund Restriction

- **المسار والإصدار:** `odoo18/pos_refund_restriction` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Restrict refund operations in POS to administrators only

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `point_of_sale`: تأكد من إضافته إلى addons_path وتثبيته قبل `pos_refund_restriction`.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
