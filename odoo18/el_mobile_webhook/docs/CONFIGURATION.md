# Mobile Webhook

- **المسار والإصدار:** `odoo18/el_mobile_webhook` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Reliable outbound status webhooks for mobile backends

## الحقول ونقاط الإعداد الموجودة في المصدر

- `company_id (Many2one)`
- `mobile_webhook_endpoint (Char)`
- `mobile_webhook_secret (Char)`
- `mobile_webhook_retry_limit (Integer)`

### إجراءات الإعداد

- `tests/test_webhook.py::test_queue_payload_has_unique_event_id`
- `tests/test_webhook.py::test_failed_delivery_is_retried`
- `models/webhook_event.py::_check_event_uuid`
- `models/webhook_event.py::_queue_status_change`
- `models/webhook_event.py::_settings`
- `models/webhook_event.py::_validate_endpoint`
- `models/webhook_event.py::_deliver`
- `models/webhook_event.py::_schedule_retry`
- `models/webhook_event.py::_cron_process_queue`
- `models/webhook_event.py::action_retry`
- `models/webhook_event.py::action_cancel`
- `models/webhook_event.py::action_send_now`
- `models/res_config_settings.py::_check_mobile_webhook_settings`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
