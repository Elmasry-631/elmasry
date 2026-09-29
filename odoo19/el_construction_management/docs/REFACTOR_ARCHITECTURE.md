# Construction Management — Refactor Architecture

## Release

- Technical module: `el_construction_management`
- Odoo target: 19
- Refactor release: `19.0.1.23.0`
- Author: Ibrahim Elmasry

## 1. Architecture goals

The refactor is intentionally domain-oriented. The objective is to make business rules discoverable, isolate integrations with Odoo core models, and keep workflow/security controls enforceable from RPC as well as from the UI.

### Layering

```text
UI / XML / Dashboard
        |
        v
Business Domain Models
  Project / BOQ / Budget / WBS / Task / Work Order
  MREQ / Inventory / Subcontract / Billing / Quality
        |
        +--------------------+
        |                    |
        v                    v
Workflow & Control Layer    Revision / Cost / Approval Controls
        |                    |
        +----------+---------+
                   |
                   v
        Odoo Core Integrations
 Account / Purchase / Stock
```

## 2. Python package structure

### Core domain

- `construction_project.py` — construction project lifecycle and project-owned records.
- `construction_permit.py` — execution permits and permit lifecycle.
- `construction_sub_project.py` — sub-project lifecycle.
- `construction_sub_project_documents.py` — handover/supporting documents.
- `construction_boq.py` — BOQ header and commercial setup.
- `construction_boq_lines.py` — BOQ line calculations and validation.
- `construction_rate_analysis.py` — rate analysis.
- `construction_budget.py` — budget header and budget workflow.
- `construction_budget_lines.py` — budget line calculations and costing.
- `construction_phase.py` — WBS / phase lifecycle.
- `construction_work_order.py` — execution work orders.
- `construction_task.py` — planning, dependencies, schedule and timesheets.
- `construction_material_requisition.py` — MREQ lifecycle and procurement creation.
- `construction_material_inventory_controls.py` — MREQ inventory quantities and site stock KPIs.
- `construction_material_issue.py` — stock issue/consume/return/wastage document and lines.
- `construction_consume_order.py` — subcontract consume orders.
- `construction_subcontract.py` — subcontract contract.
- `construction_ra_billing.py` — subcontract RA billing.
- `construction_progress_billing.py` — customer progress billing.
- `construction_progress_billing_lines.py` — progress billing lines.
- `construction_quality_check.py` — quality inspection header.
- `construction_quality_check_lines.py` — inspection lines and images.
- `construction_quality_point.py` — reusable quality points.
- `construction_extra_expense.py` — extra project expenses.
- `construction_configuration.py` — work-type configuration.
- `construction_report_wizard.py` — reporting wizard layer.

### Cross-cutting controls

The former `construction_controls.py` contained 21 classes and more than 1,000 lines of unrelated responsibilities. It is now split into:

- `construction_project_controls.py` — closure gates, cost snapshot, dashboard scope, baseline action.
- `construction_variation.py` — variation orders and their approval ledger.
- `construction_revisions.py` — BOQ, budget and schedule-baseline revisions.
- `construction_cost.py` — idempotent project cost source service.
- `construction_quality_controls.py` — NCR/CAPA controls.
- `construction_approval.py` — approval matrix configuration.
- `construction_billing_controls.py` — billing/commercial controls.
- `construction_task_controls.py` — task progress controls.
- `construction_material_controls.py` — MREQ procurement/inventory lifecycle controls.

### Odoo core integrations

All direct extensions of core Odoo models are isolated under `models/integrations/`:

- `integrations/account.py` — `account.move` construction links and vendor-bill cost hook.
- `integrations/purchase.py` — Purchase Order and Purchase Order Line links.
- `integrations/stock.py` — Stock Move/Picking/Scrap integration and material actual-cost hook.

This avoids mixing Odoo core overrides into construction business models.

## 3. Workflow security model

`workflow_mixin.py` is the central state transition guard.

1. UI action calls a business method.
2. Business method validates prerequisites.
3. `_transition()` validates the old/new state pair.
4. `_transition()` writes through a private runtime context token.
5. Direct RPC `write({'state': ...})` is rejected by the mixin.
6. Manager-only transitions call `_require_manager()`.
7. Operations that need serialization use `_lock_records()`.

The runtime token is generated per Python process and is not a user-controlled string.

## 4. Inventory accounting path

```text
MREQ
  |
  v
Material Stock Operation
  |
  +--> Issue to Site --> Stock Picking --> Site Location
  |
  +--> Consume -------> Production/Consumption Location
  |
  +--> Return ---------> Warehouse
  |
  +--> Wastage --------> Stock Scrap
                              |
                              v
                       Stock Valuation Layer
                              |
                              v
                    Construction Cost Entry
```

Actual material cost is sourced from `stock.valuation.layer` through the related `stock.move`. Cost creation is idempotent and protected by a database uniqueness constraint.

## 5. Financial source-of-truth model

`el_construction.cost.entry` is a project-control snapshot, not a replacement for Odoo Accounting.

- Committed: Purchase Order source.
- Actual material/subcontract: posted vendor-bill or stock-valuation source where applicable.
- Actual labour: construction timesheet source and employee hourly cost when available.
- Forecast: project-control value, not a GL posting.

System-generated entries carry `source_model` and `source_res_id`. User-entered entries may remain source-less and are therefore outside the system-generated uniqueness rule.

## 6. Closure gates

Project completion/archiving evaluates:

- Sub-project handover.
- Task and Work Order completion.
- MREQ closure.
- Budget closure.
- Quality checks.
- NCR/CAPA.
- Variation order resolution.
- Subcontract closure.
- Progress billing completion.
- Posted customer invoice payment/reversal.
- Posted subcontract vendor bill payment/reversal.
- Material requisition Purchase Orders.
- Material requisition Stock Pickings.
- Extra Expenses.
- Project permits.

The `enforce_closure_gates` flag allows an organization to explicitly choose a less strict project-close policy; it does not silently bypass individual workflow rules.

## 7. Dashboard scope rule

A Sub Project always belongs to one Project. If a dashboard request supplies a Sub Project without a Project, the Project is derived automatically. If both are supplied and do not match, the request is rejected. This prevents mixed-scope KPIs.

## 8. Refactor constraints

- No Odoo core files were modified.
- No Studio dependency.
- Community-compatible business code unless an explicit Enterprise feature is declared (`web_gantt`).
- Odoo 19 XML syntax retained.
- Existing external IDs were not intentionally renamed.
- Runtime certification is not claimed by static analysis.
