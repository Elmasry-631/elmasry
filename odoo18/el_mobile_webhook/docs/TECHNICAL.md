# Mobile Webhook

- **المسار والإصدار:** `odoo18/el_mobile_webhook` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Reliable outbound status webhooks for mobile backends

## المكونات المكتشفة

- Python: 11 file(s)
- XML: 4 file(s)

### نماذج وامتدادات Odoo

- MobileWebhookEvent: model _name
- ResConfigSettings: model _inherit
- AccountMove: model _inherit
- StockPicking: model _inherit
- SaleOrder: model _inherit
- AccountPayment: model _inherit

### الملفات المصدرية ذات الصلة

- `views/res_config_settings_views.xml`
- `views/mobile_webhook_event_views.xml`
- `models/webhook_event.py`
- `models/res_config_settings.py`
- `models/account_move.py`
- `models/stock_picking.py`
- `models/__init__.py`
- `models/sale_order.py`
- `models/account_payment.py`
- `security/security.xml`
- `security/ir.model.access.csv`

### حقول معلنة

- `event_uuid (Char)`
- `event_type (Char)`
- `res_model (Char)`
- `res_id (Integer)`
- `record_name (Char)`
- `company_id (Many2one)`
- `previous_status (Char)`
- `status (Char)`
- `payload_json (Text)`
- `state (Selection)`
- `attempts (Integer)`
- `next_attempt_at (Datetime)`
- `sent_at (Datetime)`
- `last_error (Char)`
- `mobile_webhook_endpoint (Char)`
- `mobile_webhook_secret (Char)`
- `mobile_webhook_timeout (Integer)`
- `mobile_webhook_retry_limit (Integer)`

### XML IDs

- `views/res_config_settings_views.xml::res_config_settings_view_form`
- `views/mobile_webhook_event_views.xml::view_mobile_webhook_event_list`
- `views/mobile_webhook_event_views.xml::view_mobile_webhook_event_form`
- `views/mobile_webhook_event_views.xml::view_mobile_webhook_event_search`
- `views/mobile_webhook_event_views.xml::action_mobile_webhook_event`
- `views/mobile_webhook_event_views.xml::menu_mobile_webhook_root`
- `views/mobile_webhook_event_views.xml::menu_mobile_webhook_events`
- `data/ir_cron.xml::ir_cron_mobile_webhook_process_queue`
- `security/security.xml::module_category_mobile_webhook`
- `security/security.xml::group_mobile_webhook_manager`
- `security/security.xml::rule_mobile_webhook_event_company`