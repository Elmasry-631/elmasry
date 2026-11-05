# MRP Lock Lines

- **المسار والإصدار:** `odoo19/mrp_lock_lines` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Lock all component lines in Manufacturing Order except the last one

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: StockMoveLine: model _inherit
- النموذج/الامتداد المعني: StockMove: model _inherit
- العملية البرمجية المتاحة: `_compute_is_last_line` في `models/stock_move_line.py`
- العملية البرمجية المتاحة: `_compute_is_last_line` في `models/stock_move_line.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
