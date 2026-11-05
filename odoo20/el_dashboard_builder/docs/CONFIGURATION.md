# Dashboard Builder

- **المسار والإصدار:** `odoo20/el_dashboard_builder` — Odoo 20
- **إصدار الحزمة:** `20.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Drag-and-drop dashboard builder with customizable widgets

## الحقول ونقاط الإعداد الموجودة في المصدر

- `company_id (Many2one)`
- `group_ids (Many2many)`
- `access_token (Char)`
- `group_ids (Many2many)`

### إجراءات الإعداد

- `tests/test_dashboard_builder.py::test_layout_config_validation`
- `tests/test_dashboard_builder.py::test_dashboard_item_config`
- `controllers/controllers.py::configure_item`
- `models/dashboard.py::_check_layout_config`
- `models/dashboard.py::action_export_config`
- `models/dashboard.py::import_dashboard_config`
- `models/dashboard.py::action_configure`
- `models/dashboard.py::action_regenerate_token`
- `wizard/item_config_wizard.py::_compute_config_fields`
- `wizard/item_config_wizard.py::default_get`
- `wizard/item_config_wizard.py::action_save`
- `wizard/item_config_wizard.py::action_reset`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
