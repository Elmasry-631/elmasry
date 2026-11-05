# Investment Clubs Management

- **المسار والإصدار:** `odoo18/investment_club` — Odoo 18
- **إصدار الحزمة:** `18.0.12.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Complete investment management system with Unified Return System

## الوظائف الظاهرة في المصدر

- ملخص الوظيفة في manifest: Complete investment management system with Unified Return System
- نموذج Odoo: ProjectSummaryReport: model _name
- نموذج Odoo: InvestorStatementReport: model _name
- نموذج Odoo: ProjectProfitReport: model _name
- نموذج Odoo: RenewalDueReport: model _name
- نموذج Odoo: ReturnPaymentLedgerReport: model _name
- نموذج Odoo: InvestorSummaryReport: model _name
- نموذج Odoo: InvestmentMaturityReport: model _name
- نموذج Odoo: MonthlyReturnsReport: model _name
- نموذج Odoo: InvestmentClub: model _name
- نموذج Odoo: TerminateReason: model _name
- نموذج Odoo: InvestmentActualReturn: model _name
- نموذج Odoo: InvestmentDashboard: model _name
- نموذج Odoo: CrmLead: model _inherit
- نموذج Odoo: ResConfigSettings: model _inherit
- نموذج Odoo: AccountMove: model _inherit
- نموذج Odoo: AccountFullReconcile: model _inherit
- نموذج Odoo: AccountPartialReconcile: model _inherit
- نموذج Odoo: MembershipRenewal: model _name
- نموذج Odoo: InvestmentProject: model _name
- نموذج Odoo: InvestmentSubscriptionRejectWizard: model _name
- نموذج Odoo: InvestmentActualReturn: model _name
- نموذج Odoo: SaleContract: model _inherit
- نموذج Odoo: SubscriptionTerminateWizard: model _name
- نموذج Odoo: InvestmentSubscription: model _name
- نموذج Odoo: InvestmentContact: model _inherit
- نموذج Odoo: InvestmentMembership: model _name
- نموذج Odoo: Contact: model _inherit
- نموذج Odoo: InvestmentProject: model _name
- نموذج Odoo: AccountPayment: model _inherit
- نموذج Odoo: InvestorDeathWizard: model _name
- قائمة واجهة: Reports
- قائمة واجهة: 1. Renewal Due
- قائمة واجهة: 2. Monthly Returns
- قائمة واجهة: 3. Investor Summary
- قائمة واجهة: 4. Active Investments
- قائمة واجهة: 5. All Investors
- قائمة واجهة: 6. Return Payments Summary
- قائمة واجهة: 7. Pending Return Payments
- قائمة واجهة: 8. Return Payment Ledger / Return payment ledger
- قائمة واجهة: 9. Investment Maturity / Investment Maturity
- قائمة واجهة: 10. Investor Statement / Investor investment statement
- قائمة واجهة: Investment
- قائمة واجهة: Dashboard
- قائمة واجهة: Clubs
- قائمة واجهة: Return Payments
- قائمة واجهة: Projects
- قائمة واجهة: Investments
- قائمة واجهة: Memberships
- قائمة واجهة: Terminations
- قائمة واجهة: Terminated Memberships
- نقطة HTTP: '/investment/dashboard/stats' (auth=user)

## التكوين والإضافات

الاعتماديات المعلنة: `base`, `mail`, `account`, `analytic`, `product`, `contacts`, `crm`, `sale_contract_auto`, `web`
