# Global Delete Protection

This Odoo 19 Community addon blocks `unlink()` through the ORM for every
registered model, including `ir.attachment`. It applies to regular users and
Administrators and covers UI and ORM-backed RPC/API calls. It does not modify
Odoo Core.

## Installation

Add `/odoo/odoo_19/odoo/projects/elmasry` to the server's `addons_path` (alongside the
existing community and custom addon paths), restart Odoo, update the Apps list,
then install **Global Delete Protection** (`el_global_delete_protection`).

CLI examples, using the actual database name:

```bash
./odoo-bin --addons-path=addons,odoo/addons,odoo/projects/elmasry -d <database> -i el_global_delete_protection --stop-after-init
./odoo-bin --addons-path=addons,odoo/addons,odoo/projects/elmasry -d <database> -u el_global_delete_protection --stop-after-init
```

Retain any other addon paths required by your deployment when setting
`--addons-path`.

## Internal deletion exception

No environment context key, `sudo()`, administrator identity, or uninstall
flag bypasses the guard. Trusted server-side maintenance code may import
`allow_internal_deletion` from
`odoo.addons.el_global_delete_protection.models.delete_protection` and scope
the smallest required cleanup block with it. The bypass is held in a
process-local `ContextVar`, is not serialized into RPC context, and resets even
when the operation raises. Do not wrap user-triggered or broad business flows.

The guard intentionally blocks cascading ORM deletes too. Consequently some
business operations, module uninstallations, and housekeeping jobs that rely on
deletion can fail until their specific trusted cleanup is explicitly scoped.
Database-level SQL deletes do not call ORM `unlink()` and are outside this
addon’s protection; direct database access must be restricted operationally.

## Tests

Run the module tests against a disposable Odoo database:

```bash
./odoo-bin --addons-path=addons,odoo/addons,odoo/projects/elmasry -d <test_database> --test-enable --test-tags /el_global_delete_protection --stop-after-init
```
