# Kitchen Receipt from Quotation

- **المسار والإصدار:** `odoo18/el_kitchen_receipt` — Odoo 18
- **إصدار الحزمة:** `18.0.4.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Print kitchen receipt from sales quotation with customer delivery info auto-fill + pilot name sync with delivery

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: الطيارين
- المستخدم يبدأ من قائمة: تقرير الطيار
- النموذج/الامتداد المعني: ResPartner: model _inherit
- النموذج/الامتداد المعني: AccountMove: model _inherit
- النموذج/الامتداد المعني: StockPicking: model _inherit
- النموذج/الامتداد المعني: XPilot: model _name
- النموذج/الامتداد المعني: PilotReportWizard: model _name
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `test_04_sync_delivery_to_partner` في `tests/test_kitchen_receipt.py`
- العملية البرمجية المتاحة: `_sync_driver_name_to_orders` في `models/account_move.py`
- العملية البرمجية المتاحة: `create` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `action_print_report` في `models/pilot_report_wizard.py`
- العملية البرمجية المتاحة: `create` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_sync_delivery_fields_to_partner` في `models/sale_order.py`
- العملية البرمجية المتاحة: `_sync_driver_name_everywhere` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
