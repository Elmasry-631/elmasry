# Product Traceability Dashboard

- **المسار والإصدار:** `odoo18/el_product_traceability_dashboard` — Odoo 18
- **إصدار الحزمة:** `18.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Product traceability dashboard with returns, scrap and manufacturing genealogy

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Product Traceability
- المستخدم يبدأ من قائمة: Dashboard
- المستخدم يبدأ من قائمة: Movement Details
- المستخدم يبدأ من قائمة: Manufacturing Genealogy
- النموذج/الامتداد المعني: TraceabilityMovementReport: model _name
- النموذج/الامتداد المعني: TraceabilityManufacturingReport: model _name
- النموذج/الامتداد المعني: ProductTraceabilityReport: model _name
- النموذج/الامتداد المعني: ProductTraceabilityManufacturing: model _name
- النموذج/الامتداد المعني: ProductTraceabilityDashboard: model _name
- العملية البرمجية المتاحة: `action_open_report` في `models/traceability_report.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
