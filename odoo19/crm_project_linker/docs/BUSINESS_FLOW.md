# CRM Project Linker

- **المسار والإصدار:** `odoo19/crm_project_linker` — Odoo 19
- **إصدار الحزمة:** `1.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Create and link projects from CRM opportunities.

## التدفق كما تكشفه نقاط الدخول

- النموذج/الامتداد المعني: CrmLead: model _inherit
- النموذج/الامتداد المعني: Project: model _inherit
- النموذج/الامتداد المعني: SaleOrder: model _inherit
- العملية البرمجية المتاحة: `action_open_project` في `models/crm_lead.py`
- العملية البرمجية المتاحة: `action_create_project` في `models/crm_lead.py`
- العملية البرمجية المتاحة: `action_open_crm_lead` في `models/crm_lead.py`
- العملية البرمجية المتاحة: `action_create_quotation_from_project` في `models/crm_lead.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
