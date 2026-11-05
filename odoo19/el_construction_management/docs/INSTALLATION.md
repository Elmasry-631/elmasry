# Construction Management

- **المسار والإصدار:** `odoo19/el_construction_management` — Odoo 19
- **إصدار الحزمة:** `19.0.1.24.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Construction Management \| Job Costing \| BOQ \| Work Orders \| RA Billing \| Material Requisition \| Subcontracting \| Budget

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `base`, `mail`, `contacts`, `hr`, `stock`, `stock_account`, `purchase`, `account`, `project`, `web_gantt`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `el_construction_management` من Apps، أو شغّل: `./odoo-bin -d <database> -i el_construction_management --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
