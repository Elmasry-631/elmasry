# Stock Movement Report

- **المسار والإصدار:** `odoo19/ie_stock_movement_report` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** PDF report of inventory movements with opening/closing balance and running value.

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Stock Movement Report
- النموذج/الامتداد المعني: StockMovementReportHandler: model _name
- النموذج/الامتداد المعني: StockMovementReport: model _name
- النموذج/الامتداد المعني: StockMovementReportWizard: model _name
- العملية البرمجية المتاحة: `test_01_wizard_creates_with_required_dates` في `tests/test_stock_movement_report.py`
- العملية البرمجية المتاحة: `test_04_action_print_pdf_returns_dict` في `tests/test_stock_movement_report.py`
- العملية البرمجية المتاحة: `test_01_manager_can_create` في `tests/test_permissions.py`
- العملية البرمجية المتاحة: `_compute_opening_balances` في `models/stock_movement_report.py`
- العملية البرمجية المتاحة: `action_print_pdf` في `models/stock_movement_report.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
