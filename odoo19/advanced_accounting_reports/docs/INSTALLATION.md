# Advanced Accounting Reports

- **المسار والإصدار:** `odoo19/advanced_accounting_reports` — Odoo 19
- **إصدار الحزمة:** `1.20.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `account`, `account_reports`, `base`, `web`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `advanced_accounting_reports` من Apps، أو شغّل: `./odoo-bin -d <database> -i advanced_accounting_reports --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
