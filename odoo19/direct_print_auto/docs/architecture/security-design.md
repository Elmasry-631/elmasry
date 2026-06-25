# Security Design — `direct_print_auto`

## Groups

| Group XML ID | Name | Implied by | Implies | Purpose |
|--------------|------|------------|---------|---------|
| `direct_print_auto.group_direct_print_user` | Direct Print User | `sales_team.group_sale_salesman` (Sales / See All Leads) | — | Can see and click the Direct Print button on form views |
| `direct_print_auto.group_direct_print_manager` | Direct Print Manager | `direct_print_auto.group_direct_print_user` | Direct Print User | Can change Direct Print settings in the Sales settings tab |

The admin user is automatically a Direct Print Manager (declared in
`security/direct_print_groups.xml` via `users="[(4, ref('base.user_admin'))]"`).

---

## Module category

A new `ir.module.category` is declared:

```xml
<record id="module_category_direct_print" model="ir.module.category">
    <field name="name">Direct Print</field>
    <field name="sequence">20</field>
</record>
```

This makes the two Direct Print groups appear under their own
"Direct Print" category in **Settings → Users → Manage Groups**,
rather than being scattered under "Sales" or "Extra Rights".

---

## ACL strategy

| Model | ACL source | Notes |
|-------|-----------|-------|
| `direct.print.mixin` | none | AbstractModel — never persisted, no ACL needed |
| `res.config.settings` (inherited) | base module | Inherits the existing ACL — only Settings managers can read/write. We add a row in `ir.model.access.csv` to give Direct Print Managers explicit read/write access to the settings (via `model_res_config_settings`). |
| `sale.order` (inherited) | sale module | Inherits the existing sale.order ACL. Direct Print doesn't introduce any new fields, so the existing ACLs apply unchanged. |
| `account.move` (inherited) | account module | Same — inherits existing ACL |
| `stock.picking` (inherited) | stock module | Same — inherits existing ACL |
| `purchase.order` (inherited) | purchase module | Same — inherits existing ACL |

### Why no new ACL rows for the inherited models?

Direct Print doesn't add new fields or new methods that bypass the
parent model's ACL. A user who can't read `sale.order` still can't
read it just because Direct Print is installed — the button is gated
by `groups="direct_print_auto.group_direct_print_user"`, and even
if a user without that group somehow triggered
`sale.order.action_direct_print()`, the underlying report rendering
(`/report/html/sale.action_report_saleorder/<id>`) performs its own
ACL check and returns 403 if the user lacks read access.

### Defense in depth

Three layers protect access to direct printing:

1. **Button visibility** — the `groups=` attribute on the button
   hides it from users who aren't Direct Print Users.

2. **Method access** — even if a non-Direct-Print-User calls
   `action_direct_print()` directly (e.g. via RPC), the method runs
   on `self` which must be a record the user can read. If the user
   can't read the record, Odoo raises AccessError before
   `action_direct_print` executes.

3. **Report ACL** — the `/report/html/<ref>/<id>` route performs
   its own ACL check on `res_model(res_ids)`. Even if the OWL
   component somehow constructed a URL for a record the user can't
   read, the backend returns 403.

---

## Record rules

**None declared.** Direct Print doesn't introduce any multi-company
or per-record filtering that isn't already enforced by the parent
models' existing record rules.

For multi-company setups:

- `sale.order` already has company_id and the standard `sale.order`
  record rule restricts visibility per company.
- `account.move` has company_id and the standard `account.move`
  record rule restricts visibility per company.
- `stock.picking` has company_id and the standard `stock.picking`
  record rule restricts visibility per company.
- `purchase.order` has company_id and the standard `purchase.order`
  record rule restricts visibility per company.

Direct Print inherits all of this automatically — no additional record
rules are needed.

---

## Settings access

Direct Print settings live under **Settings → Sales → Direct Print**.
Access to the settings form is controlled by Odoo's standard settings
ACL (typically restricted to Settings managers).

The Direct Print Manager group grants explicit read/write access to
`res.config.settings` via the row in `ir.model.access.csv`, so that
managers can change the toggles even if they aren't full Settings
managers. However, in practice, accessing the Settings form still
requires the user to be a Settings manager (Odoo's settings view
has its own group filter).

If your deployment wants Direct Print Managers to access the
settings without being full Settings managers, you'd need to add
a custom settings menu action gated on the Direct Print Manager
group — but that's beyond the scope of this module.
