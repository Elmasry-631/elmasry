# PDF Print Preview

- **المسار والإصدار:** `odoo19/el_pdf_print_preview` — Odoo 19
- **إصدار الحزمة:** `19.0.1.1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Preview PDF reports in-browser before printing — no download needed

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: IrHttp: model _inherit
- النموذج/الامتداد المعني: ResUsers: model _inherit
- النموذج/الامتداد المعني: IrActionsReport: model _inherit
- العملية البرمجية المتاحة: `test_07_preview_reload_action` في `tests/test_pdf_preview.py`
- العملية البرمجية المتاحة: `test_12_error_catcher_action` في `tests/test_pdf_preview.py`
- العملية البرمجية المتاحة: `action_preview_reload` في `models/res_users.py`
- العملية البرمجية المتاحة: `_render_qweb_pdf` في `models/ir_actions_report.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
