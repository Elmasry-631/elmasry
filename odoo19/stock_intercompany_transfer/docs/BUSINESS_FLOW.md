# Inter Company Stock Transfer

- **المسار والإصدار:** `odoo19/stock_intercompany_transfer` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `AGPL-3`
- **الملخص المعلن:** Create counterpart Receipt/Delivery Orders between     companies.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: StockPickingInherit: model _inherit
- النموذج/الامتداد المعني: StockBackorderConfirmation: model _inherit
- العملية البرمجية المتاحة: `compute_message` في `models/res_company.py`
- العملية البرمجية المتاحة: `button_validate` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `create_intercompany_transfer` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `process` في `wizard/stock_backorder_confirmation.py`
- العملية البرمجية المتاحة: `process_cancel_backorder` في `wizard/stock_backorder_confirmation.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
