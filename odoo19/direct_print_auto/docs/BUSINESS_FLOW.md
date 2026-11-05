# Direct Print Auto

- **المسار والإصدار:** `odoo19/direct_print_auto` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Auto-print invoices, SOs, delivery slips and POs to the browser's print dialog when confirmed, plus a manual Direct Print button on each form.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: PurchaseOrder: model _name
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _name
- النموذج/الامتداد المعني: StockPicking: model _name
- النموذج/الامتداد المعني: SaleOrder: model _name
- النموذج/الامتداد المعني: DirectPrintMixin: model _name
- العملية البرمجية المتاحة: `test_30_so_confirm_wraps_action_when_auto_print_on` في `tests/test_auto_print_flow.py`
- العملية البرمجية المتاحة: `test_31_so_confirm_no_wrap_when_auto_print_off` في `tests/test_auto_print_flow.py`
- العملية البرمجية المتاحة: `test_20_action_direct_print_returns_client_action` في `tests/test_direct_print_mixin.py`
- العملية البرمجية المتاحة: `button_approve` في `models/purchase_order.py`
- العملية البرمجية المتاحة: `action_post` في `models/account_move.py`
- العملية البرمجية المتاحة: `button_validate` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_direct_print` في `models/direct_print_mixin.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
