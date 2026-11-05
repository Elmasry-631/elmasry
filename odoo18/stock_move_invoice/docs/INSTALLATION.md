# Invoice From Stock Picking

- **المسار والإصدار:** `odoo18/stock_move_invoice` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Create invoice for stock picking

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `stock`, `account`
- الترخيص المعلن: `AGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `stock_move_invoice` من Apps، أو شغّل: `./odoo-bin -d <database> -i stock_move_invoice --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
