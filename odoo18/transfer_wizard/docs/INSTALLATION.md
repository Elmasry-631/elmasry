# trade_paints_wizard

- **المسار والإصدار:** `odoo18/transfer_wizard` — Odoo 18
- **إصدار الحزمة:** `1.1`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Transfer Wizard

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `base`, `sale`, `sale_management`, `stock`, `purchase`
- الترخيص المعلن: `غير محدد في manifest`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `transfer_wizard` من Apps، أو شغّل: `./odoo-bin -d <database> -i transfer_wizard --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
