# Mobile Webhook

- **المسار والإصدار:** `odoo18/el_mobile_webhook` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Reliable outbound status webhooks for mobile backends

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Mobile Webhook
- المستخدم يبدأ من قائمة: Events
- النموذج/الامتداد المعني: MobileWebhookEvent: model _name
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: StockPicking: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: AccountPayment: model _inherit
- العملية البرمجية المتاحة: `_validate_endpoint` في `models/webhook_event.py`
- العملية البرمجية المتاحة: `_cron_process_queue` في `models/webhook_event.py`
- العملية البرمجية المتاحة: `action_retry` في `models/webhook_event.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/webhook_event.py`
- العملية البرمجية المتاحة: `action_send_now` في `models/webhook_event.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
