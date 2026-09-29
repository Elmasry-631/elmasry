# EL Readonly User Access — Post-Change Report

## Executive Summary

The readonly security model was corrected so readonly users can **view inventory, warehouses, and stock movements** while remaining unable to modify business records or execute stock operations. Configuration/Settings menus remain hidden.

## Requested Behavior

| Area | Readonly User |
|---|---|
| Inventory / Warehouse | View ✅ |
| Stock Transfers / Receipts / Deliveries | View ✅ |
| Stock Moves / Move Lines | View ✅ |
| Stock Quantities / Scrap / Valuation | View ✅ |
| Create business records | Denied ❌ |
| Edit business records | Denied ❌ |
| Delete business records | Denied ❌ |
| Execute stock operations | Denied ❌ |
| Configuration / Settings menus | Hidden ❌ |
| Readonly group on Users → Access Rights | Visible ✅ |

## Changes Applied

### 1. Stock access restored

Removed the previous explicit blocking of these models:

- `stock.picking`
- `stock.move`
- `stock.move.line`
- `stock.scrap`
- `stock.quant`
- `stock.valuation.layer`

The readonly access synchronizer now grants `perm_read=True` for all registered models, including inventory models.

### 2. Stock menus restored

Removed stock-specific menu filtering. Inventory menus such as Transfers, Receipts, Delivery Orders, Internal Transfers, Scrap, and related movement menus are no longer hidden by this module.

### 3. Write protection retained

The readonly security layer still denies `create`, `write`, and `unlink` for business models. The record-rule layer also applies a false domain for modification modes. Therefore visibility does not imply edit capability.

### 4. Configuration remains hidden

The menu filtering now targets Configuration/Settings menus and their descendants only. Stock/inventory menus are explicitly not filtered.

### 5. Access Rights group

The `Readonly Access` group remains defined as a normal `res.groups` entry with an application category, so it is available in the standard Users form under Access Rights.

Technical XML ID:

`el_readonly_user.group_users_readonly`

### 6. Module identity

- Technical name: `el_readonly_user`
- Display name: `EL Readonly User Access`
- Author: `Ibrahim Elmasry`
- Company: `Ibrahim Elmasry`
- Maintainer: `Ibrahim Elmasry`
- License: `LGPL-3`

## Files Modified

- `__manifest__.py`
- `hooks.py`
- `models/ir_model_access.py`
- `models/ir_ui_menu.py`
- `security/el_readonly_user_groups.xml`
- `README.rst`
- `doc/RELEASE_NOTES.md`
- `static/description/index.html`

## Security Notes

The module does not modify Odoo core. The readonly group is enforced through Odoo model/security extension points and dynamic ACL synchronization.

The JavaScript layer disables normal form create/edit controls for the readonly user, but this is **not treated as the security boundary**. Server-side ACL/ORM checks remain responsible for preventing modifications.

Stock operation buttons may still appear in some views depending on the installed Odoo modules and view definitions. If a button invokes a write/create/unlink operation, the server-side readonly protection must reject it. This is preferable to relying only on hiding buttons.

## Validation

### Static validation

- Python source compilation: PASS
- XML parsing: PASS
- Manifest inspection: PASS
- Module reference/structure inspection: PASS
- ZIP integrity: PASS

### Runtime validation

A live Odoo database/runtime was not available in the packaging environment, so the following were not claimed as runtime-tested:

- Actual Users → Access Rights rendering
- Menu rendering in a live web client
- Inventory views/actions under a real readonly user
- Stock operation button behavior in the installed Odoo version
- Interaction with third-party record rules/modules

## Staging Test Plan

Create a dedicated test user and assign only the intended normal Odoo groups plus `Readonly Access`.

1. Open Inventory.
2. Open Warehouses and Locations permitted by the user's normal record rules.
3. Open Receipts, Delivery Orders, Transfers, and Internal Transfers.
4. Open stock move and stock move line details.
5. Verify quantities and related inventory information are readable.
6. Attempt to edit a stock picking — must fail.
7. Attempt to create a stock picking — must fail.
8. Attempt to delete a stock picking — must fail.
9. Attempt to validate/cancel/scrap a stock operation — must fail.
10. Verify Configuration/Settings menus are hidden.
11. Verify a normal non-readonly user is unaffected.
12. Check server logs for unexpected AccessError/Owl errors after upgrade.

## Important Deployment Note

The technical module name is `el_readonly_user`. If an older installation uses a different technical module name, treat the change as a module migration/rename and verify XML IDs and installed-module state before replacing it in production.

## Release

**Version:** `18.0.1.2.0`

**Release summary:** Read-only inventory visibility restored; stock modification remains blocked; Configuration/Settings remains hidden.
