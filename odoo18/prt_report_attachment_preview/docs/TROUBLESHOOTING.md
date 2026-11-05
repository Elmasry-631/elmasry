# Open PDF Reports and PDF Attachments in Browser

- **المسار والإصدار:** `odoo18/prt_report_attachment_preview` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Preview reports and pdf attachments in browser instead of downloading them.     Open Report or PDF Attachment in new tab instead of downloading.

## أعراض مرتبطة بتبعيات ومكونات هذا الموديول

- خطأ تحميل dependency `web`: تأكد من إضافته إلى addons_path وتثبيته قبل `prt_report_attachment_preview`.
- تعذر اختبار إصدار Odoo 18: استخدم نفس سلسلة الإصدار وراجع APIs التي يرثها الموديول.

## تشخيص الصلاحيات

راجع [SECURITY.md](SECURITY.md) وملفات `security/`؛ اختلاف المجموعة الفعالة أو الشركة النشطة قد يمنع الوصول. لا تعالج ذلك بإضافة `sudo()` قبل تحديد العملية والصلاحية المطلوبة.
