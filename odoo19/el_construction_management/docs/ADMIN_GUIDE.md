# Administration Guide

## Installation

1. Copy the module into an Odoo addons path.
2. Ensure the required dependencies are installed: Base, Mail, Contacts, HR, Stock, Stock Accounting, Purchase, Accounting, Project, and Gantt support.
3. Update the Apps list.
4. Install **Construction Management**.

## Upgrade

1. Back up the database and filestore.
2. Replace the module directory with the new release.
3. Restart Odoo.
4. Upgrade the module from Apps or with the Odoo upgrade command.
5. Clear/rebuild web assets when frontend assets were changed.
6. Open the Construction application and verify the navigation tree.

## Security

Use the module security groups and Odoo standard groups to control access. Manager-only configuration includes approval governance and controlled actions. Do not solve access errors by granting broad Administrator access; review the exact model, group, ACL, and record rule.

## Inventory prerequisites

For integrated material operations, configure a warehouse for the project and ensure the responsible users have the required Odoo Inventory permissions. The module uses Odoo stock moves, pickings, locations, scraps, and valuation layers rather than duplicating inventory quantities.

## Troubleshooting

### Registry fails with `bases assignment ... object layout differs`
Check for multiple scalar Python classes using the same `_inherit` target. Odoo 19 registry setup is sensitive to conflicting extension layouts. The module keeps consolidated extensions for affected models.

### `_sql_constraints` warning
Odoo 19 expects `models.Constraint`. Do not add legacy `_sql_constraints` to new code.

### Progress Billing RPC error: `_compute_invoice_count` missing
The invoice count is computed by `_compute_invoice_links`; the field must reference the method that actually exists. This release removes the stale `_compute_invoice_count` reference.

### Old menus remain after upgrade
The module includes upgrade-safe deactivation records for the previous report and navigation menus. Upgrade the module rather than only replacing the filesystem directory.

## Production checklist

- Database backup verified.
- Filestore backup verified.
- Odoo service restart plan confirmed.
- Module upgrade tested on staging.
- Security groups reviewed.
- Warehouse/project stock locations reviewed.
- Report generation tested.
- Critical workflows tested end-to-end.
