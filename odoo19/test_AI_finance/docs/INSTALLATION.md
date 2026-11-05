# AI Finance V1

- **المسار والإصدار:** `odoo19/test_AI_finance` — Odoo 19
- **إصدار الحزمة:** `1.8`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Advanced AI Finance Module: Virtual CFO & OCR Engine

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `base`, `mail`, `account`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `test_AI_finance` من Apps، أو شغّل: `./odoo-bin -d <database> -i test_AI_finance --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
