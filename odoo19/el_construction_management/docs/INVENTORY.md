# Inventory & Material Control

## Design principle
Odoo Inventory is the source of truth. Construction Management stores the project/requisition context and creates traceable Odoo stock operations.

## Locations
Each warehouse-backed project can have a Site internal location and a Consumption production location.

## Operation types
- Issue to Site
- Consume on Site
- Return to Warehouse
- Wastage / Scrap

## Controls
The module validates project/company consistency, source/destination consistency, UoM compatibility, stock availability, issued-vs-consumed quantities, and wastage allowance. Completed operations are protected from ordinary cancellation; reversal is handled through controlled operations.

## Costing
Completed stock operations can feed construction actual material cost through Odoo stock valuation layers when Stock Accounting is installed.
