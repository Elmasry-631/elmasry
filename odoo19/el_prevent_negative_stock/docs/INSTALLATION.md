# Prevent Negative Stock

- **المسار والإصدار:** `odoo19/el_prevent_negative_stock` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Prevent negative stock — block stock moves AND sales orders when stock is insufficient

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `base`, `stock`, `mail`, `sale_management`, `nmo_sale_order_approval_workflow`, `nmo_stock_user_restriction`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `el_prevent_negative_stock` من Apps، أو شغّل: `./odoo-bin -d <database> -i el_prevent_negative_stock --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
