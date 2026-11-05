# Inventory All In One Report Generator

- **المسار والإصدار:** `odoo18/inventory_report_generator` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Dynamic Inventory Report Generator for Odoo 17

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `stock`
- الترخيص المعلن: `AGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `inventory_report_generator` من Apps، أو شغّل: `./odoo-bin -d <database> -i inventory_report_generator --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
