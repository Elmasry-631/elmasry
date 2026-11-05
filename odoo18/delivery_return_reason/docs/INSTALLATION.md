# Delivery Return Reasons

- **المسار والإصدار:** `odoo18/delivery_return_reason` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** تتبع أسباب رجوع الطلبات مع إحصائيات وتحليلات

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `stock`, `el_kitchen_receipt`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `delivery_return_reason` من Apps، أو شغّل: `./odoo-bin -d <database> -i delivery_return_reason --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
