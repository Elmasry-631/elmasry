# Investment Clubs Management

- **المسار والإصدار:** `odoo18/investment_club` — Odoo 18
- **إصدار الحزمة:** `18.0.12.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Complete investment management system with Unified Return System

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `base`, `mail`, `account`, `analytic`, `product`, `contacts`, `crm`, `sale_contract_auto`, `web`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `investment_club` من Apps، أو شغّل: `./odoo-bin -d <database> -i investment_club --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
