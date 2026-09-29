# EL Readonly User Access — Fix Report

## Module
- **Technical Name:** `el_readonly_user`
- **Version:** `18.0.1.2.0`
- **Author:** Ibrahim Elmasry

## Issue
Readonly users were receiving an access error when opening/processing `stock.picking` because Odoo's stock forms/workflows can perform ACL-level `write` checks. The readonly group only had read ACLs, so the ACL check failed before the module's readonly write-blocking layer could apply.

## Required Behavior
The readonly user must be able to:
- View warehouses and inventory.
- View receipts, deliveries, internal transfers, and stock operations.
- Open stock pickings, stock moves, move lines, quants, scrap, and valuation records where normal record rules permit.

The readonly user must **not** be able to:
- Create records.
- Modify records.
- Delete records.
- Validate, cancel, scrap, or otherwise execute stock operations.

## Fix Implemented
1. Added stock form models to the ACL compatibility list:
   - `stock.picking`
   - `stock.move`
   - `stock.move.line`
   - `stock.quant`
   - `stock.scrap`
   - `stock.valuation.layer`
2. These models receive ACL-level `perm_write=True` for the readonly group so Odoo form permission checks do not fail.
3. `perm_create` and `perm_unlink` remain disabled.
4. The existing `ir.rule` readonly enforcement continues to return a false domain for `write`, `create`, and `unlink`, so actual business-record modifications remain blocked.
5. The Configuration/Settings menu hiding remains unchanged.

## Security Result
| Operation | Stock records |
|---|---|
| Read | Allowed |
| Open form | Allowed |
| Create | Denied |
| Write / Edit | Denied by readonly rule |
| Delete | Denied |
| Stock validation/workflow writes | Denied by readonly rule |

## Files Modified
- `hooks.py`
- `models/ir_model_access.py`
- `__manifest__.py`

## Validation
- Python AST parsing: **PASS**
- ZIP integrity: **PASS**
- Static security-flow review: **PASS**
- Live Odoo runtime/database validation: **NOT PERFORMED** in this environment.

## Staging Test
Create a user with `Readonly Access`, then verify:
1. Inventory opens normally.
2. Warehouse/location screens are visible according to normal record rules.
3. Receipts, Delivery Orders, Internal Transfers, and Transfers open normally.
4. Stock picking forms open without the previous `stock.picking` write-access error.
5. Edit/save is blocked.
6. Validate/cancel/scrap actions cannot change stock records.
7. Configuration/Settings remains hidden.
8. Normal users are unaffected.

## Important Security Note
The ACL-level write permission on the listed stock models is a compatibility mechanism for Odoo's permission checks; it is **not** intended to grant business write capability. The module's readonly record-rule layer remains responsible for denying actual writes. This should be verified on staging against the exact Odoo version and installed stock modules.
