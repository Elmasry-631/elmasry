# Vehicle Installment Management

- **المسار والإصدار:** `odoo19/vehicle_installment` — Odoo 19
- **إصدار الحزمة:** `19.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage vehicle installments with automatic calculation

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `base`, `mail`, `fleet`, `hr`, `hr_payroll`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `vehicle_installment` من Apps، أو شغّل: `./odoo-bin -d <database> -i vehicle_installment --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
