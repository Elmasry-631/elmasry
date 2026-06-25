# Architecture Inventories — `direct_print_auto`

**Target Odoo version:** 19
**Build type:** Full Build
**Author:** Ibrahim Elmasry

---

## 1. Requirements Summary (from STEP 0)

| Dimension | Decision |
|-----------|----------|
| Scope | Auto-print on action (when document is confirmed) |
| Documents | Sales invoices, Sales orders, Delivery / pickings, Purchase orders, Any report |
| Printer | Browser only (`window.print()` via iframe) |
| Routing | One default printer (browser default) |
| Trigger | Both — manual button + auto-print toggle per document type |
| Build depth | Full Build (1296 checks, all docs, A-F grade) |

**Translated to features:**
1. Settings page with one boolean toggle per document type for auto-print on confirm.
2. Manual "Direct Print" button on each target form view.
3. On `action_confirm` / `action_post` / `button_validate` / `button_approve`, if auto-print enabled for that doc type → return a custom client action that loads the report HTML in a hidden iframe and calls `iframe.contentWindow.print()`.
4. OWL client action (`tag='direct_print_auto'`) registered in the action registry.
5. Global toggle "Open print dialog instead of just showing PDF" in settings.

---

## 2. Model Inventory

| Model | Type | Purpose | Fields Added |
|-------|------|---------|--------------|
| `direct.print.mixin` | AbstractModel | Shared direct-print logic for any model | (no fields, only methods) |
| `res.config.settings` | inherit `res.config.settings` | Settings: per-doctype toggles | `direct_print_invoice_auto`, `direct_print_so_auto`, `direct_print_picking_auto`, `direct_print_po_auto`, `direct_print_open_dialog` |
| `sale.order` | inherit `sale.order` (mixin) | Auto-print SO on confirm + manual button | (no new fields) |
| `account.move` | inherit `account.move` (mixin) | Auto-print invoice on post + manual button | (no new fields) |
| `stock.picking` | inherit `stock.picking` (mixin) | Auto-print delivery slip on validate + manual button | (no new fields) |
| `purchase.order` | inherit `purchase.order` (mixin) | Auto-print PO on approve + manual button | (no new fields) |

### Method Inventory (per model)

**`direct.print.mixin` (AbstractModel):**
- `_get_direct_print_report_ref()` → str (XML ID of the report to print; overridden per concrete model)
- `_should_direct_print_auto()` → bool (checks settings for current model)
- `action_direct_print()` → dict (manual button: returns client action `direct_print_auto`)
- `_trigger_direct_print_after(action)` → dict (used by confirm/post/validate overrides to wrap the original action with a print step)

**`sale.order`:**
- `action_confirm()` → override: super().action_confirm() then wrap with direct print if `_should_direct_print_auto()`
- `action_direct_print()` → from mixin
- `_get_direct_print_report_ref()` → returns `'sale.action_report_saleorder'`

**`account.move`:**
- `action_post()` → override: super().action_post() then wrap with direct print if enabled AND move_type in ('out_invoice', 'out_refund')
- `action_direct_print()` → from mixin
- `_get_direct_print_report_ref()` → returns `'account.account_invoices'`

**`stock.picking`:**
- `button_validate()` → override: super().button_validate() then wrap with direct print if enabled AND picking_type_code == 'outgoing'
- `action_direct_print()` → from mixin
- `_get_direct_print_report_ref()` → returns `'stock.action_report_delivery'`

**`purchase.order`:**
- `button_approve()` → override: super().button_approve() then wrap with direct print if enabled
- `action_direct_print()` → from mixin
- `_get_direct_print_report_ref()` → returns `'purchase.action_report_purchase_order'`

---

## 3. View Inventory

| View | File | Inherits / New | Purpose |
|------|------|----------------|---------|
| Settings form | `views/res_config_settings_views.xml` | inherit `base.res_config_settings_view_form` | Add Direct Print section to Settings → Configuration → Sales (or a new section) |
| `sale.order` form | `views/sale_order_views.xml` | inherit `sale.view_order_form` | Add "Direct Print" button in statusbar |
| `account.move` form | `views/account_move_views.xml` | inherit `account.view_move_form` | Add "Direct Print" button in statusbar |
| `stock.picking` form | `views/stock_picking_views.xml` | inherit `stock.view_picking_form` | Add "Direct Print" button in statusbar |
| `purchase.order` form | `views/purchase_order_views.xml` | inherit `purchase.purchase_order_form` | Add "Direct Print" button in statusbar |

**All form-view inherits use XPath on `//header` with `position="inside"`**, button `type="object"` and `name="action_direct_print"`.

---

## 4. Action Inventory

| Action | Type | Declared In | Notes |
|--------|------|-------------|-------|
| `direct_print_auto.action_direct_print_client` | `ir.actions.client` (tag=`direct_print_auto`) | `views/client_actions.xml` (NEW) | Registered as OWL action; receives `res_model`, `res_ids`, `report_ref`, `next_action` params |
| `direct_print_auto.action_open_settings` | `ir.actions.act_url` | `views/res_config_settings_views.xml` | (Optional) menu shortcut to settings |

**No menus** — this is a settings-driven utility, no top-level menu needed.

---

## 5. Button → Method Binding Inventory

| Button | View | type | name | Method | Defined In |
|--------|------|------|------|--------|-----------|
| `<button name="action_direct_print" type="object" string="Direct Print" class="oe_highlight" icon="fa-print"/>` | `sale.order` form | object | `action_direct_print` | `direct.print.mixin.action_direct_print` (inherited by `sale.order`) | ✅ mixin |
| `<button name="action_direct_print" type="object" string="Direct Print" class="oe_highlight" icon="fa-print"/>` | `account.move` form | object | `action_direct_print` | (same) | ✅ mixin |
| `<button name="action_direct_print" type="object" string="Direct Print" class="oe_highlight" icon="fa-print"/>` | `stock.picking` form | object | `action_direct_print` | (same) | ✅ mixin |
| `<button name="action_direct_print" type="object" string="Direct Print" class="oe_highlight" icon="fa-print"/>` | `purchase.order` form | object | `action_direct_print` | (same) | ✅ mixin |

---

## 6. OWL Component Inventory

| Asset | File | Purpose |
|-------|------|---------|
| OWL client action `direct_print_auto` | `static/src/js/direct_print_action.js` | Reads `params`, fetches the report HTML via `/report/html/<ref>/<id>`, injects into hidden iframe, calls `iframe.contentWindow.print()`, then dispatches `next_action` |
| OWL template (loader) | `static/src/xml/direct_print_templates.xml` | Simple spinner template shown while report loads |
| Manifest assets entry | `__manifest__.py` → `assets` → `web.assets_backend` | Bundle JS + XML |

**OWL wiring check (Rule E):**
- [x] Component class + exported
- [x] Template with `t-name`
- [x] Both files in manifest `assets`
- [x] Registered in `registry.category("actions").add("direct_print_auto", DirectPrintAction)`

---

## 7. Security Inventory

| Group | XML ID | Implied | Purpose |
|-------|--------|---------|---------|
| Direct Print User | `direct_print_auto.group_direct_print_user` | Sales / See All Leads | Can use manual Direct Print button |
| Direct Print Manager | `direct_print_auto.group_direct_print_manager` | Direct Print User | Can change Direct Print settings |

**ACL:** No new model records → only `res.config.settings` inherit (existing ACL applies). No `ir.model.access.csv` rows needed for the mixin (AbstractModel) or for inherited models (existing ACL applies). **File still created with a single comment row** to satisfy manifest `data[]` integrity if listed.

**Record rules:** None.

---

## 8. Dependencies (`__manifest__.py`)

```python
'depends': ['base', 'web', 'sale_management', 'account', 'stock', 'purchase'],
'external_dependencies': {},
```

---

## 9. Cross-Validation Pre-Check (Rule A preview)

| Field/Method Used in Views | Exists in Model? |
|---------------------------|------------------|
| `action_direct_print` (button) | ✅ mixin |
| All other form fields | inherited from base views — no new fields introduced |

✅ **No new fields in views** — only buttons. Field-Model consistency trivially satisfied.

---

## 10. Open Questions for Confirmation

1. **OK to add the "Direct Print" button to the header (statusbar) of each form view?** (vs. in a sidebar / "Print" menu)
2. **OK to add the settings section under "Sales" tab** in `res.config.settings` (since invoices/SO/PO/picking share sales flow)? Or should it have its own "Direct Print" tab?
3. **For account.move:** apply auto-print only on `out_invoice` and `out_refund` (customer-facing), or also on `in_invoice` (vendor bills)?
4. **For stock.picking:** apply auto-print only on `outgoing` pickings (delivery), or also on `incoming` (receipts) and `internal`?
5. **OW or VSB?:** Manual "Direct Print" button — should it be visible on `sale.order` form only when state is `sale` (confirmed)? Or always visible (so user can print draft quotes too)?

---

**⛔ STOP GATE — awaiting user confirmation before STEP 2 (scaffold).**
