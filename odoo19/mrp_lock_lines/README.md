# MRP Lock Lines

## Overview

Odoo 19 module that locks all component lines (Components to Consume) in a Manufacturing Order, keeping only the **last line** editable. This prevents accidental modifications to raw material quantities, lots, and locations while still allowing adjustments on the final component line.

## Problem Solved

In a Manufacturing Order, the "Components to Consume" tab displays all raw materials from the BOM. Without this module, users can modify any line (quantity, lot, location, etc.), which may lead to unintended changes. This module restricts editing to only the last component line.

## How It Works

### Computed Field: `is_last_line`

A non-stored Boolean field is added to `stock.move.line`:

- **`True`** — This is the last component line in the Manufacturing Order (editable)
- **`False`** — All other lines (locked/readonly)

The computation groups records by `production_id` and performs a single `search()` per production order (avoiding N+1 queries) to identify the last line by `id ASC` ordering.

### View Modifications

Six XPath modifications are applied to `mrp.mrp_production_form_view`:

| Field | When Editable |
|---|---|
| `product_id` | Only on last line |
| `lot_id` | Only on last line |
| `qty_done` | Only on last line |
| `product_uom_id` | Only on last line |
| `location_id` | Only on last line |
| `location_dest_id` | Only on last line |

## What Is NOT Affected

- No business logic changes to Manufacturing Orders
- No access rights or security modifications
- No impact on creation, deletion, or workflow of orders
- BOM component generation works normally
- Lines come from BOM automatically as usual

## Technical Details

### File Structure

```
mrp_lock_lines/
├── __manifest__.py          # Module manifest (v19.0.1.0.0)
├── __init__.py              # Root import
├── models/
│   ├── __init__.py          # Model imports
│   └── stock_move_line.py   # stock.move.line extension
└── views/
    └── mrp_production_views.xml  # XPath view modifications
```

### Dependencies

- `mrp` — Manufacturing module
- `stock` — Inventory/Warehouse module

### Odoo 19 Compatibility

- Uses `readonly="not is_last_line"` instead of deprecated `attrs={}`
- Uses `qty_done` (correct Odoo 19 field name) instead of `quantity`
- Uses `move_id.raw_material_production_id` (stored field) for search domains instead of `move_id.is_consumed` (non-stored computed)

## Installation

1. Copy the `mrp_lock_lines` directory to your Odoo addons path
2. Update the apps list: Settings → Apps → Update Apps List
3. Search for "MRP Lock Lines" and click Install

## Expected Behavior

| Line | Status |
|---|---|
| Line 1 | Locked (readonly) |
| Line 2 | Locked (readonly) |
| Line 3 | Locked (readonly) |
| ... | Locked (readonly) |
| Last Line | **Editable** |