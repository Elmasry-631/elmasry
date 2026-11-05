# Construction Management

- **المسار والإصدار:** `odoo19/el_construction_management` — Odoo 19
- **إصدار الحزمة:** `19.0.1.24.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Construction Management \| Job Costing \| BOQ \| Work Orders \| RA Billing \| Material Requisition \| Subcontracting \| Budget

## الصلاحيات والحماية المكتشفة

### ACL

- access_construction_project_user: model=model_el_construction_project, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_project_manager: model=model_el_construction_project, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_project_image_user: model=model_el_construction_project_image, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_project_image_manager: model=model_el_construction_project_image, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_permit_user: model=model_el_construction_permit, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_permit_manager: model=model_el_construction_permit, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_sub_project_user: model=model_el_construction_sub_project, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_sub_project_manager: model=model_el_construction_sub_project, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_sub_project_document_user: model=model_el_construction_sub_project_document, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_sub_project_document_manager: model=model_el_construction_sub_project_document, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_boq_user: model=model_el_construction_boq, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_boq_manager: model=model_el_construction_boq, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_boq_line_user: model=model_el_construction_boq_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_boq_line_manager: model=model_el_construction_boq_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_rate_analysis_user: model=model_el_construction_rate_analysis, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_rate_analysis_manager: model=model_el_construction_rate_analysis, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_rate_analysis_line_user: model=model_el_construction_rate_analysis_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_rate_analysis_line_manager: model=model_el_construction_rate_analysis_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_budget_user: model=model_el_construction_budget, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_budget_manager: model=model_el_construction_budget, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_budget_line_user: model=model_el_construction_budget_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_budget_line_manager: model=model_el_construction_budget_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_phase_user: model=model_el_construction_phase, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_phase_manager: model=model_el_construction_phase, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_phase_entry_user: model=model_el_construction_phase_entry, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_phase_entry_manager: model=model_el_construction_phase_entry, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_work_order_user: model=model_el_construction_work_order, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_work_order_manager: model=model_el_construction_work_order, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_work_order_line_user: model=model_el_construction_work_order_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_work_order_line_manager: model=model_el_construction_work_order_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_material_requisition_user: model=model_el_construction_material_requisition, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_material_requisition_manager: model=model_el_construction_material_requisition, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_material_requisition_line_user: model=model_el_construction_material_requisition_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_material_requisition_line_manager: model=model_el_construction_material_requisition_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_subcontract_user: model=model_el_construction_subcontract, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_subcontract_manager: model=model_el_construction_subcontract, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_subcontract_line_user: model=model_el_construction_subcontract_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_subcontract_line_manager: model=model_el_construction_subcontract_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_consume_order_user: model=model_el_construction_consume_order, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_consume_order_manager: model=model_el_construction_consume_order, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_consume_order_line_user: model=model_el_construction_consume_order_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_consume_order_line_manager: model=model_el_construction_consume_order_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_ra_billing_user: model=model_el_construction_ra_billing, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_ra_billing_manager: model=model_el_construction_ra_billing, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_ra_billing_line_user: model=model_el_construction_ra_billing_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_ra_billing_line_manager: model=model_el_construction_ra_billing_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_progress_billing_user: model=model_el_construction_progress_billing, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_progress_billing_manager: model=model_el_construction_progress_billing, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_progress_billing_line_user: model=model_el_construction_progress_billing_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_progress_billing_line_manager: model=model_el_construction_progress_billing_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_quality_check_user: model=model_el_construction_quality_check, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_quality_check_manager: model=model_el_construction_quality_check, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_quality_check_line_user: model=model_el_construction_quality_check_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_quality_check_line_manager: model=model_el_construction_quality_check_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_quality_check_image_user: model=model_el_construction_quality_check_image, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_quality_check_image_manager: model=model_el_construction_quality_check_image, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_task_user: model=model_el_construction_task, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_task_manager: model=model_el_construction_task, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_timesheet_user: model=model_el_construction_timesheet, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_timesheet_manager: model=model_el_construction_timesheet, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_extra_expense_user: model=model_el_construction_extra_expense, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_extra_expense_manager: model=model_el_construction_extra_expense, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_work_type_user: model=model_el_construction_work_type, group=group_construction_user, read/write/create/delete=1/0/0/0
- access_construction_work_type_manager: model=model_el_construction_work_type, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_work_sub_type_user: model=model_el_construction_work_sub_type, group=group_construction_user, read/write/create/delete=1/0/0/0
- access_construction_work_sub_type_manager: model=model_el_construction_work_sub_type, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_quality_point_user: model=model_el_construction_quality_point, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_quality_point_manager: model=model_el_construction_quality_point, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_report_wizard_user: model=model_el_construction_report_wizard, group=group_construction_user, read/write/create/delete=1/1/1/1
- access_construction_report_menu_wizard_user: model=model_el_construction_report_menu_wizard, group=group_construction_user, read/write/create/delete=1/1/1/1
- access_construction_variation_order_user: model=model_el_construction_variation_order, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_variation_order_manager: model=model_el_construction_variation_order, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_variation_order_line_user: model=model_el_construction_variation_order_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_variation_order_line_manager: model=model_el_construction_variation_order_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_boq_revision_user: model=model_el_construction_boq_revision, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_boq_revision_manager: model=model_el_construction_boq_revision, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_boq_revision_line_user: model=model_el_construction_boq_revision_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_boq_revision_line_manager: model=model_el_construction_boq_revision_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_budget_revision_user: model=model_el_construction_budget_revision, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_budget_revision_manager: model=model_el_construction_budget_revision, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_budget_revision_line_user: model=model_el_construction_budget_revision_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_budget_revision_line_manager: model=model_el_construction_budget_revision_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_baseline_revision_user: model=model_el_construction_task_baseline_revision, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_baseline_revision_manager: model=model_el_construction_task_baseline_revision, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_baseline_revision_line_user: model=model_el_construction_task_baseline_revision_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_baseline_revision_line_manager: model=model_el_construction_task_baseline_revision_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_cost_entry_user: model=model_el_construction_cost_entry, group=group_construction_user, read/write/create/delete=1/0/0/0
- access_construction_cost_entry_manager: model=model_el_construction_cost_entry, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_ncr_user: model=model_el_construction_ncr, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_ncr_manager: model=model_el_construction_ncr, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_capa_user: model=model_el_construction_capa, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_capa_manager: model=model_el_construction_capa, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_approval_matrix_user: model=model_el_construction_approval_matrix, group=group_construction_user, read/write/create/delete=1/0/0/0
- access_construction_approval_matrix_manager: model=model_el_construction_approval_matrix, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_material_issue_user: model=model_el_construction_material_issue, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_material_issue_manager: model=model_el_construction_material_issue, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_material_issue_line_user: model=model_el_construction_material_issue_line, group=group_construction_user, read/write/create/delete=1/1/1/0
- access_construction_material_issue_line_manager: model=model_el_construction_material_issue_line, group=group_construction_manager, read/write/create/delete=1/1/1/1
- access_construction_variation_approval_user: model=model_el_construction_variation_approval, group=group_construction_user, read/write/create/delete=1/0/0/0
- access_construction_variation_approval_manager: model=model_el_construction_variation_approval, group=group_construction_manager, read/write/create/delete=1/0/0/0

### المجموعات وقواعد السجلات

- المجموعات: `group_construction_user`, `group_construction_manager`
- قواعد السجلات: `rule_construction_project_company`, `rule_construction_sub_project_company`, `rule_construction_boq_company`, `rule_construction_budget_company`, `rule_construction_work_order_company`, `rule_construction_mreq_company`, `rule_construction_subcontract_company`, `rule_construction_progress_billing_company`, `rule_construction_phase_company`, `rule_construction_quality_company`, `rule_construction_task_company`, `rule_construction_extra_expense_company`, `rule_construction_quality_point_company`, `rule_construction_ra_billing_company`, `rule_construction_approval_matrix_company`, `rule_construction_variation_approval_company`, `rule_construction_boq_revision_company`, `rule_construction_boq_revision_line_company`, `rule_construction_budget_revision_company`, `rule_construction_budget_revision_line_company`, `rule_construction_baseline_revision_company`, `rule_construction_baseline_revision_line_company`, `rule_construction_boq_line_company`, `rule_construction_budget_line_company`, `rule_construction_work_order_line_company`, `rule_construction_mreq_line_company`, `rule_construction_subcontract_line_company`, `rule_construction_consume_company`, `rule_construction_consume_line_company`, `rule_construction_ra_billing_line_company`, `rule_construction_progress_billing_line_company`, `rule_construction_quality_line_company`, `rule_construction_quality_image_company`, `rule_construction_task_timesheet_company`, `rule_construction_phase_entry_company`, `rule_construction_permit_company`, `rule_construction_project_image_company`, `rule_construction_sub_project_document_company`, `rule_construction_rate_analysis_company`, `rule_construction_rate_analysis_line_company`, `rule_construction_variation_order_company`, `rule_construction_cost_entry_company`, `rule_construction_ncr_company`, `rule_construction_capa_company`, `rule_construction_variation_order_line_company`, `rule_construction_ncr_capa_company`, `rule_construction_material_issue_company`, `rule_construction_material_issue_line_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- `models/construction_variation.py`

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.