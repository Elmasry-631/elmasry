# POS Daily Sequence

- **المسار والإصدار:** `odoo19/pos_daily_sequence` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Automatically reset POS order numbering every day

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: PosConfig: model _inherit
- النموذج/الامتداد المعني: PosSession: model _inherit
- النموذج/الامتداد المعني: PosOrder: model _inherit
- العملية البرمجية المتاحة: `_create_daily_sequence` في `models/pos_config.py`
- العملية البرمجية المتاحة: `_create_session_sequence` في `models/pos_config.py`
- العملية البرمجية المتاحة: `_generate_session_order_number` في `models/pos_config.py`
- العملية البرمجية المتاحة: `_generate_day_order_number` في `models/pos_config.py`
- العملية البرمجية المتاحة: `_generate_daily_order_number` في `models/pos_config.py`
- العملية البرمجية المتاحة: `_get_or_create_today_date_range` في `models/pos_config.py`
- العملية البرمجية المتاحة: `create` في `models/pos_config.py`
- العملية البرمجية المتاحة: `_process_order` في `models/pos_order.py`
- العملية البرمجية المتاحة: `action_pos_order_paid` في `models/pos_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
