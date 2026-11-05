# EL Cheque Tracking

- **المسار والإصدار:** `odoo19/el_cheque_tracking` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Track received and issued cheques with accounting lifecycle entries

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Track received and issued cheques with accounting lifecycle entries
- نموذج Odoo: AccountPaymentMethod: model _inherit
- نموذج Odoo: ResCompany: model _inherit
- نموذج Odoo: ResPartner: model _inherit
- نموذج Odoo: ChequeDeposit: model _name
- نموذج Odoo: ChequeReturn: model _name
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: AccountPaymentRegister: model _inherit
- نموذج Odoo: ChequeReturnReason: model _name
- نموذج Odoo: ChequeCheque: model _name
- نموذج Odoo: AccountPayment: model _inherit
- نموذج Odoo: ChequeDepositWizard: model _name
- نموذج Odoo: ChequeReturnWizard: model _name
- نموذج Odoo: ChequePrintWizard: model _name
- قائمة واجهة: Cheque Tracking
- قائمة واجهة: Received
- قائمة واجهة: Received Cheques
- قائمة واجهة: Deposits
- قائمة واجهة: Issued
- قائمة واجهة: Issued Cheques
- قائمة واجهة: Operations
- قائمة واجهة: All Cheques
- قائمة واجهة: Returns
- قائمة واجهة: Configuration
- قائمة واجهة: Return Reasons

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `mail`, `account`
