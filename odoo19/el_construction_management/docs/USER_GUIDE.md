# Construction Management — User Guide

## 1. Purpose

Construction Management provides a controlled lifecycle for construction projects covering project setup, WBS/planning, BOQ and budgeting, procurement/material requisitions, site stock movements, work execution, subcontracting, progress billing, quality, NCR/CAPA, cost control, and reporting.

## 2. Navigation

The main application is intentionally organized into eight business areas:

1. Dashboard
2. Projects
3. Planning & Execution
4. Commercial & Cost
5. Procurement & Inventory
6. Quality & Compliance
7. Reports
8. Configuration

## 3. First-time setup

### Step 1 — Configure work classification
Go to **Construction → Configuration → Work Types**.
1. Create the major work categories.
2. Add Work Sub Types when a category needs a second classification level.
3. Set codes and active status.
4. Save before creating BOQ or work-order lines.

### Step 2 — Configure project quality points
Go to **Construction → Configuration → Project Quality Points**.
1. Create the inspection/check-point definitions.
2. Set the relevant classification and active status.
3. Use these points when configuring project quality checks.

### Step 3 — Configure approval governance
Managers can configure **Construction → Configuration → Approval Matrix**.
1. Create a matrix row.
2. Select the business model and company.
3. Define amount range and required approvals.
4. Assign approvers.
5. Keep the matrix active only after reviewing separation-of-duties requirements.

## 4. Create a Project

Go to **Construction → Projects → Projects → New**.

### Project information
1. Enter the project name/reference.
2. Select the company.
3. Select the project manager/responsible user where available.
4. Enter planned dates and other scheduling information.
5. Select the warehouse when material/site stock integration is required.
6. Save the project.

### Site stock initialization
When a warehouse is configured, initialize the project stock locations from the project. The module creates a project Site location and a Consumption location beneath it. These are Odoo Inventory locations; the construction module does not maintain a parallel stock ledger.

## 5. Create a Sub Project

Go to **Construction → Projects → Sub Projects → New**.
1. Select the parent Project.
2. Enter dates and responsibility.
3. Complete the operational details.
4. Use the notebook tabs to manage BOQ, Tasks, WBS/Phases, Work Orders, Material Requisitions, Budget Lines, Engineers, Documents, Insurance, Extra Expenses, and Progress Billing.

## 6. Build the BOQ

Go to **Construction → Commercial & Cost → Bill of Quantities**.
1. Select Project/Sub Project.
2. Select Work Type and Work Sub Type where applicable.
3. Select the unit of measure.
4. Enter measurement dimensions when the line is dimension-driven.
5. Review calculated quantity.
6. Add BOQ product/material lines.
7. Enter unit prices.
8. Review the calculated total.

Do not manually duplicate the same commercial scope in unrelated records; use the BOQ as the controlled scope baseline.

## 7. Create the Budget

Go to **Construction → Commercial & Cost → Budgets**.
1. Select Project/Sub Project.
2. Choose the budget method.
3. Enter the project amount or create budget lines according to the selected method.
4. Review planned, actual, and variance amounts.
5. Confirm/approve using the available workflow buttons.
6. Use Budget Revisions under Project Controls when a controlled revision is required instead of editing a finalized budget directly.

## 8. Plan the Work

Go to **Construction → Planning & Execution → Phases / WBS**.
1. Create the project phases/WBS structure.
2. Assign dates and responsibility.
3. Add child phases when needed.
4. Link work orders and costing information.

Go to **Planning & Execution → Tasks**.
1. Create the task.
2. Link Project, Sub Project, Phase, and Work Order as applicable.
3. Assign the responsible user.
4. Set planned dates and hours.
5. Select progress mode when physical quantity progress is required.
6. Define dependencies where required.

Use **Planning & Execution → Schedule** for Gantt-oriented planning.

## 9. Execute Work Orders

Go to **Planning & Execution → Work Orders**.
1. Create/select the Project context.
2. Set responsible person and dates.
3. Add Materials, Equipment, Labour, and Overhead lines.
4. Link budget lines where applicable.
5. Review totals.
6. Confirm and move through the available execution workflow.

## 10. Material Requisition

Go to **Procurement & Inventory → Material Requisitions**.
1. Create a requisition.
2. Select Project/Sub Project and required context.
3. Add required material lines.
4. Enter quantities and UoM.
5. Submit through the configured workflow.
6. Use the procurement action(s) to create/track the downstream procurement process.
7. Once stock is available, create a Material Stock Operation.

## 11. Site Material Flow

The integrated material flow is:

**Warehouse → Project Site → Site Consumption**

with controlled returns and wastage/scrap where allowed.

### Issue to Site
1. Open the relevant Material Requisition.
2. Select the issue action.
3. Review source and project Site locations.
4. Review product, quantity, and UoM.
5. Confirm the stock operation.
6. Validate the generated Odoo stock document.

### Consume on Site
1. Create a Consumption operation from the requisition.
2. Verify the Site and Consumption locations.
3. Verify the quantity against the issued quantity.
4. Validate the generated stock movement.

### Return to Warehouse
1. Create a Return operation.
2. Confirm that the material is physically available at the Site.
3. Validate the stock movement back to the warehouse.

### Wastage / Scrap
1. Create a Wastage operation only for genuine scrap/wastage.
2. Check the allowed wastage quantity.
3. Excess wastage requires the configured manager authorization.
4. Validate the Odoo scrap operation.

## 12. Subcontracting

Go to **Commercial & Cost → Contracts → Subcontracting**.
1. Create the subcontract.
2. Select project/sub-project and contractor.
3. Define scope of work.
4. Add work lines and commercial values.
5. Record completion/certification.
6. Use Consume Orders and RA Billings where applicable.

## 13. Progress Billing

Go to **Commercial & Cost → Progress Billing**.
1. Create a billing record.
2. Select Project and optional Sub Project/Phase/Work Order.
3. Select the Customer and invoice type.
4. Choose which work-order line categories to include.
5. Use **Load Work Order Lines**.
6. Review each category tab: Materials, Equipment, Labour, Overhead, and Others.
7. Review taxes and calculated totals.
8. Start the billing workflow.
9. Create the invoice when the record reaches the invoice-creation state.
10. Review linked invoices using the Invoices smart button.
11. Complete the billing after the commercial conditions are satisfied.

## 14. Variation Orders

Go to **Commercial & Cost → Project Controls → Variation Orders**.
1. Create the variation.
2. Select project and relevant scope.
3. Enter the reason and description.
4. Add BOQ-based lines.
5. Review the calculated amount.
6. Submit for approval.
7. Approvers review and approve/reject according to the configured governance.

Approved variations become part of project commercial control; finalized records should not be edited directly.

## 15. Revisions

Use **Project Controls** for controlled revisions:
- BOQ Revisions
- Budget Revisions
- Schedule Baselines

Create a revision, document the reason, copy or define the revised scope, submit/approve as applicable, and preserve the historical revision rather than overwriting the previous baseline.

## 16. Quality and NCR/CAPA

### Quality Check
1. Go to **Quality & Compliance → Quality Checks**.
2. Select project and inspection context.
3. Complete check points.
4. Record results and evidence.
5. Move through the inspection workflow.

### NCR / CAPA
1. Create an NCR from the Quality area.
2. Record severity, description, and root cause.
3. Start CAPA actions.
4. Assign owners and deadlines.
5. Verify corrective action.
6. Close only after verification requirements are satisfied.

## 17. Cost Control

Use **Commercial & Cost → Project Controls → Cost Control** for controlled cost entries and review project committed, actual, and forecast values from the project controls area.

## 18. Reports

Go to **Construction → Reports**.
1. Select the report type.
2. Select optional Project/date filters.
3. Select the output format.
4. Generate the report.

The Report Center replaces the previous long list of report menus and is the single entry point for construction reporting.

## 19. Project Closeout

Before closing a project, resolve the closure gates shown by the Project Controls information. Typical blockers include open tasks, work orders, material requisitions, budgets, quality checks, NCRs, CAPA items, variations, subcontracts, progress billings, extra expenses, or pending permits.

## 20. Daily operating checklist

**Planner:** verify WBS, task dates, dependencies, and baseline.

**Commercial:** verify BOQ, budget, variations, commitments, and billing.

**Procurement/Store:** verify requisitions, receipts, issues, consumption, returns, and wastage.

**Site:** update work orders, quantities, progress, and evidence.

**Quality:** close inspections and NCR/CAPA actions.

**Project Manager:** review dashboard, cost status, schedule, commercial exposure, and closure gates.
