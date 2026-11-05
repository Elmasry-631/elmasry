# Inter Company Internal Transfer

- **المسار والإصدار:** `odoo20/el_inter_company_transfer` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Request stock transfers between warehouses of different companies

## المتطلبات

- Odoo 20 متوافق مع هذا المجلد.
- الإضافات: `base`, `stock`, `mail`, `portal`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo20` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `el_inter_company_transfer` من Apps، أو شغّل: `./odoo-bin -d <database> -i el_inter_company_transfer --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
