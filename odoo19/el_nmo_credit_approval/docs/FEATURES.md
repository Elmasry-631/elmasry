# El-Nmo - Credit Limit Approval Workflow

- **المسار والإصدار:** `odoo19/el_nmo_credit_approval` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for sale orders exceeding customer credit limits.

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Approval workflow for sale orders exceeding customer credit limits.
- نموذج Odoo: CreditApprovalRequest: model _name
- نموذج Odoo: CreditRejectionReason: model _name
- نموذج Odoo: SaleOrder: model _inherit
- نموذج Odoo: CreditApprovalWizard: model _name
- قائمة واجهة: Credit Approval
- قائمة واجهة: Approval Requests
- قائمة واجهة: Rejection Reasons

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `mail`, `sale`, `el_nmo_classification`
