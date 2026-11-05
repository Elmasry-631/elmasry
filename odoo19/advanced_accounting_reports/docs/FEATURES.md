# Advanced Accounting Reports

- **المسار والإصدار:** `odoo19/advanced_accounting_reports` — Odoo 19
- **إصدار الحزمة:** `1.20.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Advanced General Ledger, Trial Balance with Analytic Dimensions & Multi-Currency
- نموذج Odoo: TrialBalanceReport: model _name
- نموذج Odoo: GeneralLedgerReport: model _name
- نموذج Odoo: ResCompany: model _inherit
- نموذج Odoo: AccountFeature: model _name
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: AccountPatchNumber: model _name
- نموذج Odoo: AccountMoveLine: model _inherit
- نموذج Odoo: AccountCostCenter: model _name
- نموذج Odoo: TrialBalanceWizard: model _name
- نموذج Odoo: GeneralLedgerWizard: model _name
- قائمة واجهة: Advanced Dimensions
- قائمة واجهة: Features
- قائمة واجهة: Cost Centers
- قائمة واجهة: Patch Numbers
- قائمة واجهة: General Ledger (Advanced)
- قائمة واجهة: Trial Balance (Advanced)
- نقطة HTTP: '/advanced_accounting/reports/general_ledger' (auth=user)
- نقطة HTTP: '/advanced_accounting/export/general_ledger_xlsx' (auth=user)
- نقطة HTTP: '/advanced_accounting/export/trial_balance_xlsx' (auth=user)

## التكوين والإضافات

الاعتماديات المعلنة: `account`, `account_reports`, `base`, `web`
