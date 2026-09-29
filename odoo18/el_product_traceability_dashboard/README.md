# el_product_traceability_dashboard

Odoo 18 Community module for tracing completed stock moves from purchase receipts through manufacturing consumption/production and subsequent stock movements.

## Features
- Purchase receipt visibility: vendor, purchase order, quantity, unit price and purchase value when linked.
- Manufacturing consumption and production visibility.
- Lot/serial visibility.
- Stock valuation layer integration when valuation records exist.
- List, Pivot and Graph analytical views.
- OWL dashboard with KPI cards and top-product analysis.
- Company-aware reporting and dedicated access group.

## Install
Copy `el_product_traceability_dashboard` to an Odoo addons path, update Apps, then install **Product Traceability Dashboard**.

## Important limitation
The report uses one representative move-line lot per stock move to avoid multiplying analytical move rows. Full one-row-per-lot genealogy should be implemented as a dedicated move-line genealogy model if strict lot genealogy is required.
