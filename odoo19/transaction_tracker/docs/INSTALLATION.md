# Transaction Tracker

- **المسار والإصدار:** `odoo19/transaction_tracker` — Odoo 19
- **إصدار الحزمة:** `1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track all user transactions across every Odoo module

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `base`, `web`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `transaction_tracker` من Apps، أو شغّل: `./odoo-bin -d <database> -i transaction_tracker --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
