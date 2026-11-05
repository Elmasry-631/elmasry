# Investment Clubs Management

- **المسار والإصدار:** `odoo18/investment_club` — Odoo 18
- **إصدار الحزمة:** `18.0.12.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Complete investment management system with Unified Return System

## الحقول ونقاط الإعداد الموجودة في المصدر

- `company_id (Many2one)`
- `payment_journal_id (Many2one)`
- `company_id (Many2one)`
- `payment_journal_id (Many2one)`
- `return_payment_journal_id (Many2one)`
- `termination_company_share_pct (Float)`
- `report_company_header (Boolean)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `refund_journal_id (Many2one)`
- `payment_journal_id (Many2one)`
- `company_id (Many2one)`
- `company_id (Many2one)`
- `refund_journal_id (Many2one)`
- `company_share_increase (Float)`
- `company_income (Float)`
- `refund_journal_id (Many2one)`

### إجراءات الإعداد

- `models/investment_actual_return_inherit.py::_get_config`
- `models/investment_subscription.py::_get_config`
- `models/membership.py::_get_config`
- `models/investment_project_inherit.py::_get_config`

### إعدادات النظام

راجع `res.config.settings` وملفات XML/CSV المدرجة في manifest. لا توجد قيمة افتراضية مفترضة هنا؛ راجع الحقول المعرفة فعليًا واضبطها في نسخة الاختبار أولًا.
