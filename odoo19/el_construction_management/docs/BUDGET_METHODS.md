# Budget Methods

The construction budget supports three planning models.

## 1. Project Total

Use when the project is controlled by one overall amount and you do not want to allocate the amount into budget lines.

- Enter **Project Budget**.
- Do not create Budget Lines.
- `Total Planned = Project Budget`.
- `Allocated to Lines = 0`.
- `Unallocated = Project Budget`.

This mode does **not** infer actual costs from unrelated project documents. Actual cost remains based on explicit Budget Line allocations, so a project-only budget should be treated as a top-level financial envelope unless line allocations are later introduced by changing the method.

## 2. Budget Lines

Use when the budget is built entirely from detailed items such as BOQ, materials, work types, or cost items.

- Project Budget is not entered.
- Add Budget Lines.
- `Total Planned = sum(Budget Lines)`.
- `Allocated to Lines = Total Planned`.
- `Unallocated = 0`.

This is the existing detailed costing model and is the default for budgets generated from BOQ.

## 3. Project Total + Budget Lines

Use when management approves one project ceiling and the team progressively distributes it across cost lines.

Example:

- Project Budget = 1,000,000
- Concrete = 300,000
- Steel = 250,000
- Labor = 200,000
- Allocated = 750,000
- Unallocated = 250,000
- Allocation = 75%

The allocated amount can never exceed the project budget.

## Workflow

The existing approval workflow remains:

`Draft -> Confirmed -> Approved -> Done`

with cancellation/reset according to the existing construction workflow rules.

Before Confirm/Approve/Done, the budget structure is validated server-side.

## BOQ integration

BOQ-generated budgets continue to use **Budget Lines** and preserve the exact BOQ-line-to-budget-line relationship. This avoids changing the established costing behavior.

## Actual cost limitation

Actual cost is intentionally still calculated from explicit Budget Line allocations (Work Orders, Extra Expenses, and approved RA Billing lines). A Project Total budget with no Budget Lines therefore does not invent or estimate actual cost from all project documents. This prevents double counting and protects historical costing semantics.
