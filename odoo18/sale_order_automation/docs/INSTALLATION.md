# Sale Order Automation

- **المسار والإصدار:** `odoo18/sale_order_automation` — Odoo 18
- **إصدار الحزمة:** `1.1`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Enable auto sale workflow with sale order confirmation. Include operations like Auto Create Invoice, Auto Validate Invoice and Auto Transfer Delivery Order.

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `sale_stock`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `sale_order_automation` من Apps، أو شغّل: `./odoo-bin -d <database> -i sale_order_automation --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
