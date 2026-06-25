# Security Reference — `direct_print_auto`

## Groups

### Direct Print User (`direct_print_auto.group_direct_print_user`)

- **Implied by:** Sales / See All Leads (`sales_team.group_sale_salesman`)
- **Implies:** (nothing)
- **Capabilities:** Sees the "Direct Print" button on the form view
  of supported documents (sales order, customer invoice, outgoing
  delivery, purchase order). Can click the button to open the
  browser print dialog with the relevant report pre-loaded.

### Direct Print Manager (`direct_print_auto.group_direct_print_manager`)

- **Implied by:** Direct Print User
- **Implies:** Direct Print User
- **Capabilities:** All Direct Print User capabilities, plus read/write
  access to `res.config.settings` (so they can change the Direct Print
  toggles). However, accessing the Settings menu still requires the
  standard Settings manager group.
- **Default members:** The admin user (`base.user_admin`) is
  automatically added as a Direct Print Manager on install.

---

## Module category

A new `ir.module.category` is declared:

- **XML ID:** `direct_print_auto.module_category_direct_print`
- **Name:** Direct Print
- **Sequence:** 20

This appears in **Settings → Users → Manage Groups** as a top-level
category, containing the two groups above.

---

## ACL (`ir.model.access.csv`)

| Line | Group | Model | Permissions |
|------|-------|-------|-------------|
| 1 | Direct Print Manager | `res.config.settings` | read, write, create (no unlink) |

No other ACL rows are declared because:

- `direct.print.mixin` is an AbstractModel — no DB table, no ACL.
- `sale.order`, `account.move`, `stock.picking`, `purchase.order`,
  `res.config.settings` are inherited models whose ACLs come from
  their parent modules. Direct Print doesn't add new fields or new
  methods that bypass those ACLs.

---

## Button-level access control

The Direct Print button on each form view has:

```xml
groups="direct_print_auto.group_direct_print_user"
```

This hides the button from users who aren't Direct Print Users. Even
if a non-authorized user calls `action_direct_print()` directly via
RPC, the standard model ACL on `sale.order` / `account.move` / etc.
will raise AccessError before the method body executes.

---

## Defense in depth

Three layers protect access to direct printing:

1. **Button visibility** — `groups=` attribute hides the button from
   unauthorized users in the UI.

2. **Method access** — `action_direct_print()` runs on `self`, which
   must be a record the user can read. Standard model ACLs enforce
   this regardless of how the method is invoked.

3. **Report ACL** — the `/report/html/<ref>/<id>` route performs its
   own ACL check. Even if a user somehow constructed a print URL for
   a record they can't read, the backend returns 403.

---

## Multi-company considerations

No new record rules are declared. All four target models already have
`company_id` and standard per-company record rules from their parent
modules. Direct Print inherits these automatically.

In a multi-company setup:
- A user can only direct-print documents in companies they have access to.
- The auto-print toggle is global (per database), not per-company. If
  you need per-company auto-print settings, you'd need to extend the
  module to add a `res.company` form field — out of scope for this
  version.

---

## Uninstall safety

When the module is uninstalled:

- The two groups are removed (and any user-to-group assignments
  are dropped).
- The `ir.module.category` is removed.
- The ACL row for `res.config.settings` is removed.
- The `ir.config_parameter` entries (`direct_print_auto.*`) are
  removed (because they were created via the `config_parameter=`
  field attribute, which Odoo tracks and cleans up).
- The inherited views are removed, so the Direct Print button
  disappears from all form views.
- The OWL client action is unregistered (because the JS bundle is
  removed from `web.assets_backend`).

No orphan records, no orphan tables, no orphan columns.
