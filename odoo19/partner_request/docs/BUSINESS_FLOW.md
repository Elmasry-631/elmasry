# Partner Request

- **المسار والإصدار:** `odoo19/partner_request` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Approval workflow for creating new customers via sales requests.

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Partner Requests
- النموذج/الامتداد المعني: PartnerRequest: model _name
- النموذج/الامتداد المعني: ResPartner: model _inherit
- العملية البرمجية المتاحة: `create` في `models/partner_request.py`
- العملية البرمجية المتاحة: `_validate_state` في `models/partner_request.py`
- العملية البرمجية المتاحة: `action_submit` في `models/partner_request.py`
- العملية البرمجية المتاحة: `action_create_partner` في `models/partner_request.py`
- العملية البرمجية المتاحة: `action_send_back` في `models/partner_request.py`
- العملية البرمجية المتاحة: `action_reject` في `models/partner_request.py`
- العملية البرمجية المتاحة: `action_open_partner` في `models/partner_request.py`
- العملية البرمجية المتاحة: `create` في `models/partner_request.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
