# Upgrade / Migration Notes — 19.0.1.1.0

## Legacy budget-cost allocation

The hardened costing engine uses an explicit `budget_line_id` on cost-bearing records. During upgrade, the post-migration script attempts to backfill legacy Work Order Lines, Extra Expenses, and RA Billing Lines **only when exactly one Budget Line matches the legacy project/sub-project/company/product context**.

Ambiguous or unmappable records are intentionally left with an empty `budget_line_id`; the migration never guesses between duplicate budget lines. Review those records manually before relying on historical Actual Cost reporting.

## RA billing semantics

`current_amount` represents the amount certified by the current RA document. Approved RA documents are accumulated for cumulative cost. If the legacy process stored cumulative certification totals instead of current-period certification, historical RA data must be reconciled before upgrade.

## Runtime certification

Static package validation does not replace an Odoo 19 runtime installation, module upgrade, database migration rehearsal, automated test execution, and UAT in a staging database.


## 19.0.1.5.0 Budget Method
Existing budgets are retained as `Budget Lines`. No historical amounts are changed. New budgets support Project Total, Budget Lines, or Project Total + Budget Lines.

## 19.0.1.5.0

New `budget_method` supports `project`, `lines`, and `hybrid`. Existing budgets are migrated/defaulted to `lines` so their historical `total_planned` semantics remain unchanged. No historical financial amounts are rewritten.
