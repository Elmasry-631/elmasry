# eBook Serial Delivery

- **المسار والإصدار:** `odoo19/ebook_serial_delivery` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `website_sale`, `sale_stock`, `mail`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `ebook_serial_delivery` من Apps، أو شغّل: `./odoo-bin -d <database> -i ebook_serial_delivery --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
