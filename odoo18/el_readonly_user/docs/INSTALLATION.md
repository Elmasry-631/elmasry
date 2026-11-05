# EL Readonly User Access

- **المسار والإصدار:** `odoo18/el_readonly_user` — Odoo 18
- **إصدار الحزمة:** `18.0.1.2.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Grant controlled read-only access to users

## المتطلبات

- Odoo 18 متوافق مع هذا المجلد.
- الإضافات: `base`, `web`
- الترخيص المعلن: `LGPL-3`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo18` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `el_readonly_user` من Apps، أو شغّل: `./odoo-bin -d <database> -i el_readonly_user --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
