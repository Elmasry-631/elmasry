# TechScope | ZK Attendance Integration

- **المسار والإصدار:** `odoo19/zk_attendance_integration_v19` — Odoo 19
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `غير محدد في manifest`
- **الملخص المعلن:** Integration with ZK Attendance Machines

## المتطلبات

- Odoo 19 متوافق مع هذا المجلد.
- الإضافات: `base`, `hr`, `hr_attendance`
- الترخيص المعلن: `غير محدد في manifest`. راجع ملف `LICENSE` وأي إشعار حقوق مرفق قبل إعادة التوزيع.

## التثبيت

1. أضف `odoo19` إلى `addons_path` في بيئة Odoo.
2. تحقق أن كل dependency متاح في إصدار Odoo والطبعة المستهدفين.
3. حدّث قائمة التطبيقات ثم ثبّت `zk_attendance_integration_v19` من Apps، أو شغّل: `./odoo-bin -d <database> -i zk_attendance_integration_v19 --stop-after-init`.
4. افتح الإعدادات/القوائم المذكورة في [CONFIGURATION.md](CONFIGURATION.md) واختبرها بمستخدم وصلاحيات مماثلة للإنتاج.

لا تنفذ التثبيت أو الترقية على قاعدة إنتاج قبل نسخة احتياطية ومراجعة أثر hooks وعمليات البيانات.
