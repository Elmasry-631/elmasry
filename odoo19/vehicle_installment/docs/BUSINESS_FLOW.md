# Vehicle Installment Management

- **المسار والإصدار:** `odoo19/vehicle_installment` — Odoo 19
- **إصدار الحزمة:** `19.0.2.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Manage vehicle installments with automatic calculation

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Vehicle Installments
- المستخدم يبدأ من قائمة: Installments
- المستخدم يبدأ من قائمة: Payment Schedule
- النموذج/الامتداد المعني: HrPayslip: model _inherit
- النموذج/الامتداد المعني: VehicleInstallmentLine: model _name
- النموذج/الامتداد المعني: VehicleInstallment: model _name
- العملية البرمجية المتاحة: `action_payslip_paid` في `models/hr_payslip.py`
- العملية البرمجية المتاحة: `action_payslip_unpaid` في `models/hr_payslip.py`
- العملية البرمجية المتاحة: `action_payslip_cancel` في `models/hr_payslip.py`
- العملية البرمجية المتاحة: `_compute_total_amount` في `models/vehicle_installment.py`
- العملية البرمجية المتاحة: `_compute_calculated_months` في `models/vehicle_installment.py`
- العملية البرمجية المتاحة: `compute_installments` في `models/vehicle_installment.py`
- العملية البرمجية المتاحة: `button_approve` في `models/vehicle_installment.py`
- العملية البرمجية المتاحة: `button_reject` في `models/vehicle_installment.py`
- العملية البرمجية المتاحة: `button_draft` في `models/vehicle_installment.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
