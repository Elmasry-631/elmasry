# Stock Split Transfer

- **المسار والإصدار:** `odoo18/stock_split_transfer` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Two-step internal transfers with per-user location visibility

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: StockPicking: model _inherit
- النموذج/الامتداد المعني: ResUsers: model _inherit
- العملية البرمجية المتاحة: `_compute_is_split_transfer` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `_create_split_transfer` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `button_validate` في `models/stock_picking.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
