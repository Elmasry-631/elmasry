# Stock Picking From Invoice

- **المسار والإصدار:** `odoo19/invoice_stock_move` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Stock Picking From Customer/Supplier Invoice

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: AccountMoveLine: model _inherit
- العملية البرمجية المتاحة: `_compute_picking_type_id` في `models/account_move.py`
- العملية البرمجية المتاحة: `action_stock_move` في `models/account_move.py`
- العملية البرمجية المتاحة: `action_view_picking` في `models/account_move.py`
- العملية البرمجية المتاحة: `_create_stock_moves` في `models/account_move_line.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
