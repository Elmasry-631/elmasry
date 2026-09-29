# Full Code Review — `el_construction_management` 19.0.1.23.0

## Review status

**Static review:** PASS after refactor and hardening.

**Runtime Odoo 19 validation:** NOT EXECUTED in this build environment because the Python environment does not contain the Odoo package/registry. No live database, module upgrade, browser UI, QWeb render, multi-company transaction or concurrency certification is claimed.

## Review basis

- Previous module release: `19.0.1.22.0` / V40 Control Hardening.
- Risk report: `RISK_AND_WORKFLOW_GAPS_AR.md` supplied for this module.
- Current source tree after refactor.
- All Python/XML/security/report/asset/test files were enumerated.

## 1. Refactor delta

### Before

`models/construction_controls.py` contained 21 classes and approximately 1,051 lines, mixing:

- project stock setup
- project closure
- cost snapshots
- dashboard aggregation
- variations
- approvals
- revisions
- cost entries
- NCR/CAPA
- progress billing controls
- task controls
- MREQ controls
- RA billing controls

The same file therefore acted as a de-facto service layer, integration layer and workflow layer simultaneously.

### After

The responsibilities are separated into domain control files and a dedicated `models/integrations/` package. The legacy God File is no longer in the import graph.

The source tree now contains 42 Python files under `models/`, including the integration package, with 51 registered model classes discovered statically.

## 2. Central workflow review

### Finding

Many models already inherited `ConstructionWorkflowMixin`, but the write-protection pattern was repeated across individual models. Models such as NCR/CAPA/revision parents were not uniformly protected against direct state writes.

### Change

`ConstructionWorkflowMixin.write()` now rejects direct state changes unless the private runtime workflow token is present.

### Effect

The protection is centralized. A UI button, RPC call, server action or custom code cannot simply call `write({'state': ...})` on a workflow model without going through an approved transition path.

### Remaining test requirement

Run RPC tests for every workflow model with a non-manager user and a manager user.

## 3. Stock integration review

### Finding A — misplaced stock actual-cost calculation

The previous stock-picking implementation treated a picking record as though it were a stock move while looking up `stock.valuation.layer.stock_move_id`. That can associate valuation with the wrong record identity.

### Change

Actual-cost creation now lives on the `stock.move` integration. `stock.picking._action_done()` delegates to its `move_ids`.

### Finding B — Wastage ordering

The previous Wastage path validated the Scrap while the construction material operation was still Draft. That meant the downstream state/cost hook could run before the operation reached its controlled state.

### Change

Wastage now creates the Scrap first, marks the Construction Stock Operation Confirmed, and validates the Scrap from `action_done()`. The Scrap validation then moves the linked operation to Done and creates the valuation-backed actual cost.

### Finding C — Stock Operation state security

`el_construction.material.issue` did not previously have the same direct-RPC state protection as the other construction workflows.

### Change

It now inherits the workflow mixin, protects state writes, and uses `_transition()` for Confirmed/Done/Cancelled.

## 4. Cost-entry review

### Finding

A Python `search_count()` before `create()` is not a database concurrency guard.

### Change

`el_construction.cost.entry` has a database uniqueness constraint for generated source identity and a `create_from_source()` helper using a savepoint. The helper is used by project snapshot generation and stock valuation cost generation.

### Effect

Concurrent rebuilds or duplicate stock hooks cannot intentionally create two generated entries for the same `(source_model, source_res_id, cost_type, project_id)` identity.

## 5. Vendor-bill / Extra Expense integration

### Finding

Duplicate detection previously used mutable business values such as amount/product/project. That can produce false positives or false negatives when two invoice lines legitimately share the same amount.

The previous code also swallowed every exception while confirming/approving the generated expense.

### Change

`el_construction.extra.expense` now stores `source_move_line_id` with a database uniqueness constraint. A posted vendor-bill line therefore has one deterministic Extra Expense identity.

System-generated expenses are marked Approved at creation because the source is already a posted accounting document. This avoids requiring the accountant who posts a vendor bill to also be a Construction Manager.

The broad `except Exception: pass` was removed.

## 6. Project stock-location identity

### Finding

If a project had an existing Site/Consumption location belonging to another company, the old helper could create a replacement location. This risks splitting stock history.

### Change

Existing mismatched locations now raise a validation error. The module no longer silently creates a replacement location for a company mismatch.

Warehouse/Company changes after stock activity remain blocked.

## 7. Revision numbering

### Finding

Revision number calculation used `search(last revision)` without serialization. Two concurrent users could select the same next revision number.

### Change

BOQ and Budget revision creation locks the parent record before calculating the next number. Database uniqueness remains the final guard.

## 8. Approval Matrix

### Finding

The matrix advertised multiple document types while only Variation Order was actually connected to the approval ledger and multi-approval logic.

### Change

The configuration is now restricted to the workflow that is actually wired end-to-end: Variation Order.

Variation approval behavior:

1. Creator cannot approve their own Variation Order.
2. Matrix determines authorized approvers.
3. Duplicate approval by the same user is rejected.
4. Approval history is stored.
5. `required_approvals` is enforced.
6. Only after the required count is reached does the Variation move to Approved.
7. Without a configured matrix, Construction Manager approval is required.

This is intentionally more honest than presenting unsupported multi-document approval as a completed feature.

## 9. Dashboard scope

### Finding

A Sub Project filter could coexist with a broader Project KPI scope when the Project filter was not supplied.

### Change

The dashboard now derives the Project from the selected Sub Project and rejects an inconsistent Project/Sub Project pair.

## 10. Project closure

Closure checks were expanded to include downstream commercial and inventory records, not only construction states.

### Current closure blockers

- unfinished Sub Projects
- unfinished Tasks
- unfinished Work Orders
- open MREQs
- unfinished Budgets
- open Quality Checks
- open NCRs
- open CAPA
- unresolved Variation Orders
- unfinished Subcontracts
- posted unpaid/reversed subcontract Vendor Bills according to the strict policy
- unfinished Progress Billings
- posted unpaid customer invoices linked to Progress Billing
- unapproved Extra Expenses
- MREQ-linked Purchase Orders not Done/Cancelled
- MREQ-linked Stock Pickings not Done/Cancelled
- pending Permits

## 11. Core integration isolation

External Odoo model extensions were moved out of construction domain files:

- `account.move` → `models/integrations/account.py`
- `purchase.order` / `purchase.order.line` → `models/integrations/purchase.py`
- `stock.move` / `stock.picking` / `stock.scrap` → `models/integrations/stock.py`

An unrelated global override of `project.project.unlink()` was removed. The construction module should not globally change deletion semantics of every standard Odoo Project unless a construction-specific relation requires it.

## 12. Model-by-model code review map

| Domain | Main file | Responsibility | Static review |
|---|---|---|---|
| Project | `construction_project.py` | lifecycle, links, archive | PASS |
| Project Controls | `construction_project_controls.py` | closure, cost, dashboard | PASS |
| Permit | `construction_permit.py` | permit lifecycle | PASS |
| Sub Project | `construction_sub_project.py` | sub-project lifecycle | PASS |
| Sub Project Documents | `construction_sub_project_documents.py` | handover evidence | PASS |
| BOQ | `construction_boq.py` | BOQ header | PASS |
| BOQ Lines | `construction_boq_lines.py` | quantities/amounts | PASS |
| Rate Analysis | `construction_rate_analysis.py` | rates | PASS |
| Budget | `construction_budget.py` | budget lifecycle | PASS |
| Budget Lines | `construction_budget_lines.py` | allocation/cost | PASS |
| Phase/WBS | `construction_phase.py` | phase lifecycle | PASS |
| Work Order | `construction_work_order.py` | execution gates | PASS |
| Task | `construction_task.py` | planning/dependencies/timer | PASS |
| MREQ | `construction_material_requisition.py` | procurement workflow | PASS |
| MREQ Inventory KPIs | `construction_material_inventory_controls.py` | issued/consumed/returned/wastage | PASS |
| Material Issue | `construction_material_issue.py` | stock operations | PASS |
| Subcontract | `construction_subcontract.py` | contract | PASS |
| Consume Order | `construction_consume_order.py` | subcontract consumption | PASS |
| RA Billing | `construction_ra_billing.py` | subcontract billing | PASS |
| Progress Billing | `construction_progress_billing.py` | customer billing | PASS |
| Progress Billing Lines | `construction_progress_billing_lines.py` | billing lines | PASS |
| Quality Check | `construction_quality_check.py` | inspections | PASS |
| Quality Lines/Images | `construction_quality_check_lines.py` | evidence | PASS |
| Quality Points | `construction_quality_point.py` | reusable checks | PASS |
| Extra Expense | `construction_extra_expense.py` | project expense | PASS |
| Variation | `construction_variation.py` | change control | PASS |
| Revisions | `construction_revisions.py` | BOQ/Budget/Baseline | PASS |
| Approval | `construction_approval.py` | matrix configuration | PASS |
| Cost | `construction_cost.py` | cost-source snapshot | PASS |
| NCR/CAPA | `construction_quality_controls.py` | quality escalation | PASS |
| Billing Controls | `construction_billing_controls.py` | commercial controls | PASS |
| Task Controls | `construction_task_controls.py` | progress controls | PASS |
| Material Controls | `construction_material_controls.py` | procurement/inventory state | PASS |
| Account Integration | `integrations/account.py` | posted vendor bill linkage | PASS |
| Purchase Integration | `integrations/purchase.py` | PO linkage | PASS |
| Stock Integration | `integrations/stock.py` | valuation/movement linkage | PASS |

## 13. Static validation performed

- Python AST parsing: PASS.
- Python `compileall`: PASS.
- XML parsing: PASS.
- Duplicate XML IDs: 0.
- Internal model inventory: 51 models discovered.
- ACL coverage: 51/51 internal models have ACL entries.
- Deprecated XML syntax scan (`tree`, `attrs`, `states`): PASS.
- External integration uniqueness: one integration class per core target.
- Removed legacy `construction_controls.py` from the import graph: PASS.
- Python cache artifacts in final package: removed.

## 14. Runtime/UAT requirements still open

Static review cannot prove:

1. Odoo 19 Registry loading.
2. View inheritance/XPath success against the exact installed Odoo 19 Enterprise build.
3. QWeb rendering.
4. Dashboard JS execution.
5. Multi-company record-rule behavior under real users.
6. Stock valuation behavior with actual costing configuration.
7. Concurrent revision/cost creation against PostgreSQL.
8. Payment-state behavior with real reconciliation.
9. Upgrade from the previous database schema.
10. Browser-level workflow/UAT.

These are deliberately marked **UNVERIFIED** rather than passed by assumption.

## 15. Recommended next runtime gate

Install/upgrade the module on an Odoo 19 staging database, then execute the workflow matrix in `tests/` plus the following live scenarios:

- two concurrent BOQ revisions
- two concurrent cost snapshot rebuilds
- Wastage over allowed quantity
- Wastage within allowed quantity
- Stock Issue → Consume → Return
- posted vendor bill → Extra Expense
- Progress Billing → Invoice → Payment
- Subcontract → RA Billing → Vendor Bill → Payment
- Project Company A / Company B access isolation
- Permit pending → Work Order Start blocked
- Quality Conditional/Fail → Work Order Done blocked
- Handover without documents/client acceptance → blocked
- Project archive with unpaid customer/vendor balances → blocked

## Conclusion

The module is materially cleaner and more defensible after the refactor. The main architectural debt from the previous release — the oversized controls file, mixed core integrations, inconsistent state protection, stock valuation identity error, and source-identity weaknesses — has been addressed in code.

**Status:** `STATIC REVIEW PASS / RUNTIME UNVERIFIED`
