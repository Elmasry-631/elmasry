# Mobile Webhook

- **المسار والإصدار:** `odoo18/el_mobile_webhook` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Reliable outbound status webhooks for mobile backends

## الصلاحيات والحماية المكتشفة

### ACL

- access_mobile_webhook_event_manager: model=model_mobile_webhook_event, group=base.group_system, read/write/create/delete=1/1/1/0

### المجموعات وقواعد السجلات

- المجموعات: `group_mobile_webhook_manager`
- قواعد السجلات: `rule_mobile_webhook_event_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `tests/test_webhook.py`
- `models/webhook_event.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.