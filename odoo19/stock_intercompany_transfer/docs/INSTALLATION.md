# Inter Company Stock Transfer

- **المسار والإصدار:** `odoo19/stock_intercompany_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Create counterpart Receipt/Delivery Orders between     companies.

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `stock`, `account`
- الترخيص المعلن: `AGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `stock_intercompany_transfer` من Apps، أو شغّل: `./odoo-bin -d <database> -i stock_intercompany_transfer --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
