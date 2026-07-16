# Inventories — ie_stock_movement_report

## 1. Model Inventory

### stock.movement.report (AbstractModel)
- **Purpose:** Business logic — fetches move lines, computes balances.
- **Methods:**
  - `get_report_data(date_from, date_to, warehouse_id, location_id, product_id, categ_id) → dict`
  - `_build_base_domain(company, warehouse_id, location_id, product_id, categ_id) → list`
  - `_prefetch_product_data(products) → dict`
  - `_compute_opening_balances(domain, product_data) → dict`
  - `_scope_location_ids(warehouse_id, location_id) → set|None`
  - `_make_inbound_checker(warehouse_id, location_id) → callable`
  - `_prefetch_names(records) → dict`
  - `_empty_payload(...) → dict`
- **No fields** (abstract data provider)
- **No states** (no persisted records)

### stock.movement.report.wizard (TransientModel)
- **Purpose:** Collects user filters, triggers PDF.
- **Fields:**
  | Name        | Type        | Required | Help                          |
  |-------------|-------------|----------|-------------------------------|
  | date_from   | Date        | Yes      | Start of period               |
  | date_to     | Date        | Yes      | End of period                 |
  | warehouse_id| Many2one → stock.warehouse | No | Restrict to one warehouse |
  | location_id | Many2one → stock.location  | No | Restrict to one location subtree |
  | product_id  | Many2one → product.product | No | Restrict to one product    |
  | categ_id    | Many2one → product.category| No | Restrict to one product category |
- **Methods:**
  - `action_print_pdf() → dict` (ir.actions.report)
  - `_check_dates() → None` (@api.constrains on date_from, date_to)
- **Constraints:**
  - `date_from <= date_to` else UserError

### report.stock.movement.report (AbstractModel, _inherit='report.abstract_report')
- **Purpose:** Glue between wizard and QWeb template.
- **Methods:**
  - `_get_report_values(docids, data=None) → dict`
- **Template:** `ie_stock_movement_report.report_stock_movement_document`

## 2. View Inventory

| View ID                                    | Type | Model                            | Purpose              |
|--------------------------------------------|------|----------------------------------|----------------------|
| view_stock_movement_report_wizard_form     | form | stock.movement.report.wizard     | Wizard filter form   |

(No list/search views — wizard only opens in modal)

## 3. Action Inventory

| Action ID                                | Name                    | res_model                        | Type               |
|------------------------------------------|-------------------------|----------------------------------|--------------------|
| action_stock_movement_report_wizard      | Stock Movement Report   | stock.movement.report.wizard     | ir.actions.act_window |
| action_report_stock_movement             | Stock Movement Report (PDF) | stock.movement.report.wizard | ir.actions.report  |

## 4. Button → Method Map

| Button                | View         | Method called        | Type   |
|-----------------------|--------------|----------------------|--------|
| action_print_pdf      | wizard form  | action_print_pdf     | object |
| (cancel)              | wizard form  | (special=cancel)     | special|
