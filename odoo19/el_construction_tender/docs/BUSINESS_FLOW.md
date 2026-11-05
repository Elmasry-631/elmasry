# Construction Tendering

- **المسار والإصدار:** `odoo19/el_construction_tender` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Client Tenders (Bid Costing & Submission) + Subcontractor/Vendor RFQ & Bid Comparison

## التدفق كما تكشفه نقاط الدخول

- المستخدم يبدأ من قائمة: Tendering
- المستخدم يبدأ من قائمة: Tenders
- المستخدم يبدأ من قائمة: Subcontractor / Vendor RFQs
- النموذج/الامتداد المعني: ConstructionTenderRfq: model _name
- النموذج/الامتداد المعني: ConstructionTenderRfqLine: model _name
- النموذج/الامتداد المعني: ConstructionTenderRfqVendor: model _name
- النموذج/الامتداد المعني: ConstructionTenderRfqBidLine: model _name
- النموذج/الامتداد المعني: ConstructionTenderOpportunity: model _name
- النموذج/الامتداد المعني: ConstructionTenderLine: model _name
- النموذج/الامتداد المعني: ConstructionTenderRfqCompareWizard: model _name
- العملية البرمجية المتاحة: `create` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `_compute_stats` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_send` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_start_bidding` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_go_comparison` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_reset_draft` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_open_compare_wizard` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_award_vendor` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_create_subcontract` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `_open_subcontract_action` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `_compute_total_amount` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `create` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_mark_submitted` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_mark_declined` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `action_award` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `_compute_amount` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `_compute_is_lowest` في `models/tender_rfq.py`
- العملية البرمجية المتاحة: `create` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `_compute_totals` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `_compute_counts` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_set_qualification` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_start_estimating` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_send_review` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_submit` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_reset_draft` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_mark_lost` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_cancel` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_mark_won` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_create_project` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `_open_project_action` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `action_view_rfqs` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `_compute_cost_unit` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `_compute_price` في `models/tender_opportunity.py`
- العملية البرمجية المتاحة: `_compute_amounts` في `models/tender_opportunity.py`

التسلسل أعلاه مستخرج من القوائم والنماذج ونقاط الدخول المعرّفة؛ راجع حالات الأعمال الفعلية قبل تفعيل سير عمل مالي أو مخزني حساس.
