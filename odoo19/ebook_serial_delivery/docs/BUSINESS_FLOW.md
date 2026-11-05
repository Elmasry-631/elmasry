# eBook Serial Delivery

- **المسار والإصدار:** `odoo19/ebook_serial_delivery` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Deliver eBook licenses using standard Inventory Serial Numbers (stock.lot) — no custom "activation code" model.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: ResCompany: model _inherit
- النموذج/الامتداد المعني: ResConfigSettings: model _inherit
- النموذج/الامتداد المعني: StockPicking: model _inherit
- النموذج/الامتداد المعني: StockMove: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- النموذج/الامتداد المعني: ProductTemplate: model _inherit
- النموذج/الامتداد المعني: StockPickingJawalySms: model _name
- العملية البرمجية المتاحة: `_confirm_ebook_order` في `tests/test_serial_mail_template.py`
- العملية البرمجية المتاحة: `action_open_ebook_serial_mail_template` في `models/res_config_settings.py`
- العملية البرمجية المتاحة: `action_resend_ebook_email` في `models/stock_picking.py`
- العملية البرمجية المتاحة: `_action_done` في `models/stock_move.py`
- العملية البرمجية المتاحة: `_compute_ebook_serial_numbers_html` في `models/sale_order.py`
- العملية البرمجية المتاحة: `action_confirm` في `models/sale_order.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
