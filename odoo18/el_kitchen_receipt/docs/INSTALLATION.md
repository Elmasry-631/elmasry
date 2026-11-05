# Kitchen Receipt from Quotation

- **المسار والإصدار:** `odoo18/el_kitchen_receipt` — Odoo 18
- **إصدار الحزمة:** `18.0.4.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `sale`, `sale_stock`, `account`, `stock`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `el_kitchen_receipt` من Apps، أو شغّل: `./odoo-bin -d <database> -i el_kitchen_receipt --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
