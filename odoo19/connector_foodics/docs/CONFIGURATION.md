# Foodics Connector

- **المسار والإصدار:** `odoo19/connector_foodics` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Bidirectional synchronization bridge between Odoo and Foodics POS

## الحقول ونقاط الإعداد الموجودة في المصدر

- `warehouse_id (Many2one)`
- `pos_config_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `api_key (Char)`
- `api_secret (Char)`
- `token (Char)`
- `token_expires_at (Datetime)`
- `base_url (Char)`
- `webhook_secret (Char)`
- `webhook_url (Char)`
- `company_id (Many2one)`
- `rate_limit (Integer)`
- `order_journal_id (Many2one)`

### إجراءات الإعداد

- `tests/test_foodics_models.py::test_connection_generates_webhook_url`
- `controllers/webhook_controller.py::foodics_webhook_health`
- `controllers/webhook_controller.py::foodics_webhook_http`
- `controllers/webhook_controller.py::_handle`
- `models/foodics_webhook.py::create_from_request`
- `models/foodics_webhook.py::process`
- `models/foodics_connection.py::_compute_counts`
- `models/foodics_connection.py::_compute_webhook_url`
- `models/foodics_connection.py::_check_base_url`
- `models/foodics_connection.py::action_generate_webhook_secret`
- `models/foodics_connection.py::action_open_sync_logs`
- `models/foodics_connection.py::action_open_failed_sync_logs`
- `models/foodics_connection.py::action_test_connection`
- `models/foodics_connection.py::_test_connection`
- `models/foodics_connection.py::_log_operation`
- `models/foodics_connection.py::_run_adapter`
- `models/foodics_connection.py::cron_sync_products`
- `models/foodics_connection.py::cron_sync_categories`
- `models/foodics_connection.py::cron_sync_customers`
- `models/foodics_connection.py::cron_sync_orders`
- `models/foodics_connection.py::cron_sync_inventory`
- `models/foodics_connection.py::cron_sync_taxes`
- `wizards/wizard_test_connection.py::action_test`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
