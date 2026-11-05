# Transaction Tracker

- **المسار والإصدار:** `odoo19/transaction_tracker` — Odoo 19
- **إصدار الحزمة:** `1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track all user transactions across every Odoo module

## الحقول ونقاط الإعداد الموجودة في المصدر

- `company_id (Many2one)`
- `company_id (Many2one)`

### إجراءات الإعداد

- `models/tracker_config.py::create`
- `models/tracker_config.py::write`
- `models/tracker_config.py::unlink`
- `models/tracker_config.py::_get_config`
- `models/tracker_config.py::_invalidate_tracker_cache`
- `models/tracker_config.py::action_track_all`
- `models/tracker_config.py::action_untrack_all`
- `models/tracker_config.py::action_auto_populate_models`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
