# POS Daily Sequence

- **المسار والإصدار:** `odoo19/pos_daily_sequence` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically reset POS order numbering every day

## الحقول ونقاط الإعداد الموجودة في المصدر

- لا توجد عناصر معلنة في ملفات الموديول.

### إجراءات الإعداد

- `models/pos_config.py::_onchange_use_daily_sequence`
- `models/pos_config.py::_create_daily_sequence`
- `models/pos_config.py::write`
- `models/pos_config.py::_create_session_sequence`
- `models/pos_config.py::_generate_session_order_number`
- `models/pos_config.py::_generate_day_order_number`
- `models/pos_config.py::_generate_daily_order_number`
- `models/pos_config.py::_get_or_create_today_date_range`
- `models/pos_config.py::create`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
