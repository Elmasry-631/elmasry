# Product Movement Lifecycle Report

- **المسار والإصدار:** `odoo18/product_movement_report` — Odoo 18
- **إصدار الحزمة:** `18.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Full movement history of a product/lot from first receipt until fully sold

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Product Movement Lifecycle
- النموذج/الامتداد المعني: ProductMovementLine: model _name
- النموذج/الامتداد المعني: ProductMovementSummary: model _name
- النموذج/الامتداد المعني: ProductMovementWizard: model _name
- العملية البرمجية المتاحة: `_generate_lines` في `wizard/product_movement_wizard.py`
- العملية البرمجية المتاحة: `action_show` في `wizard/product_movement_wizard.py`
- العملية البرمجية المتاحة: `action_print` في `wizard/product_movement_wizard.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
