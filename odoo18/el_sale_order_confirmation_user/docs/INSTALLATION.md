# Sale Order Confirmation User

- **المسار والإصدار:** `odoo18/el_sale_order_confirmation_user` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track which user actually confirmed each sales order

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `sale`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `el_sale_order_confirmation_user` من Apps، أو شغّل: `./odoo-bin -d <database> -i el_sale_order_confirmation_user --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
