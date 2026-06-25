# Model Design — `direct_print_auto`

## Model list

| # | Model | Type | Inherits | New fields | New methods |
|---|-------|------|----------|-----------|-------------|
| 1 | `direct.print.mixin` | AbstractModel | — | none | `_get_direct_print_report_ref`, `_should_direct_print_auto`, `action_direct_print`, `_trigger_direct_print_after` |
| 2 | `res.config.settings` | TransientModel (inherit) | `res.config.settings` | 5 Boolean | none |
| 3 | `sale.order` | Model (inherit + mixin) | `sale.order` + `direct.print.mixin` | none | `_get_direct_print_report_ref`, `_should_direct_print_auto`, `action_confirm` (override) |
| 4 | `account.move` | Model (inherit + mixin) | `account.move` + `direct.print.mixin` | none | `_get_direct_print_report_ref`, `_should_direct_print_auto`, `action_post` (override) |
| 5 | `stock.picking` | Model (inherit + mixin) | `stock.picking` + `direct.print.mixin` | none | `_get_direct_print_report_ref`, `_should_direct_print_auto`, `button_validate` (override) |
| 6 | `purchase.order` | Model (inherit + mixin) | `purchase.order` + `direct.print.mixin` | none | `_get_direct_print_report_ref`, `_should_direct_print_auto`, `button_approve` (override) |

---

## `direct.print.mixin` — the AbstractModel

The mixin is the heart of the module. It defines the **contract** for
direct-printable models and provides the **shared implementation** for
both the manual button and the auto-print-after-confirm flow.

### Why AbstractModel?

An `AbstractModel` is never persisted (no DB table) but can be inherited
by any `Model` via `_inherit = ["my.model", "direct.print.mixin"]`. This
is the standard Odoo pattern for sharing behaviour across models that
have nothing else in common (in our case: SOs, invoices, pickings, POs).

### API

| Method | Returns | Purpose |
|--------|---------|---------|
| `_get_direct_print_report_ref()` | `str` | Returns the XML ID of the report to print. **Abstract** — must be overridden by each concrete model. |
| `_should_direct_print_auto()` | `bool` | Returns `True` when auto-print should fire for `self`. Default: `False`. Concrete models override to check the settings toggle AND any domain filter (e.g. customer invoices only). |
| `action_direct_print()` | `dict` (client action) | Entry point for the manual button on the form view. Returns a `direct_print_auto` client action dict. |
| `_trigger_direct_print_after(original_action)` | `dict` | Helper called by the confirm/post/validate overrides. If `self` has exactly one record AND `_should_direct_print_auto()` returns `True`, wraps `original_action` in a `direct_print_auto` client action. Otherwise returns `original_action` untouched. |

### Code sketch

```python
class DirectPrintMixin(models.AbstractModel):
    _name = "direct.print.mixin"
    _description = "Direct Print Mixin"

    def _get_direct_print_report_ref(self):
        raise NotImplementedError(...)

    def _should_direct_print_auto(self):
        return False

    def action_direct_print(self):
        self.ensure_one()
        return {
            "type": "ir.actions.client",
            "tag": "direct_print_auto",
            "params": {
                "report_ref": self._get_direct_print_report_ref(),
                "res_model": self._name,
                "res_ids": self.ids,
                "next_action": False,
            },
        }

    def _trigger_direct_print_after(self, original_action):
        if not self or len(self) > 1:
            return original_action
        record = self[0]
        if not record._should_direct_print_auto():
            return original_action
        return {
            "type": "ir.actions.client",
            "tag": "direct_print_auto",
            "params": {
                "report_ref": record._get_direct_print_report_ref(),
                "res_model": record._name,
                "res_ids": [record.id],
                "next_action": original_action,
            },
        }
```

---

## `res.config.settings` — the 5 toggles

```python
class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    direct_print_invoice_auto = fields.Boolean(
        config_parameter="direct_print_auto.invoice_auto",
    )
    direct_print_so_auto = fields.Boolean(
        config_parameter="direct_print_auto.so_auto",
    )
    direct_print_picking_auto = fields.Boolean(
        config_parameter="direct_print_auto.picking_auto",
    )
    direct_print_po_auto = fields.Boolean(
        config_parameter="direct_print_auto.po_auto",
    )
    direct_print_open_dialog = fields.Boolean(
        config_parameter="direct_print_auto.open_dialog",
        default=True,
    )
```

### Why `config_parameter=` instead of a normal Boolean field?

A normal Boolean field on `res.config.settings` would store its value in
a separate column on the `res.config.settings` transient model — which
is wiped periodically. The `config_parameter=` attribute tells Odoo to
persist the value in `ir.config_parameter` instead, which is a permanent
key-value store. This survives database restarts, module upgrades, and
can be read from anywhere in the codebase via
`self.env['ir.config_parameter'].sudo().get_param('direct_print_auto.so_auto')`.

---

## Concrete model pattern

All four concrete models follow the same pattern. Here's `sale.order`
as an example:

```python
class SaleOrder(models.Model):
    _name = "sale.order"                                  # ← keep original name
    _inherit = ["sale.order", "direct.print.mixin"]       # ← extend + add mixin

    def _get_direct_print_report_ref(self):
        return "sale.action_report_saleorder"

    def _should_direct_print_auto(self):
        return bool(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("direct_print_auto.so_auto", "False")
            .lower() == "true"
        )

    def action_confirm(self):
        action = super().action_confirm()
        return self._trigger_direct_print_after(action)
```

### Why re-declare `_name`?

When using `_inherit = [...]` (list form), Odoo needs to know which
item in the list is the "primary" model (the one being extended) vs.
which are mixins being added. Re-declaring `_name = "sale.order"`
makes this unambiguous: "I am extending the existing sale.order
model, and also pulling in the direct.print.mixin methods."

Without `_name`, Odoo would interpret the list as "create a new model
that delegates to all parents" — which is wrong for our use case.

### Why `len(self) > 1` skip in `_trigger_direct_print_after`?

If the user multi-selects 30 SOs and clicks Confirm, `super().action_confirm()`
returns a single action dict (not 30). Auto-printing 30 documents in a
row would open 30 print dialogs — unusable. The single-record check
ensures auto-print only fires when the user confirms one document at a
time, which is the common case for the auto-print use case.

### Why lowercase compare on `ir.config_parameter`?

`ir.config_parameter` values are stored as strings. The Boolean field
writes `"True"` or `"False"` (Python repr). To be defensive against
future changes (e.g. someone setting the value via SQL or via the
`ir.config_parameter` menu with different casing), we lowercase the
string and compare to `"true"`. The default fallback `"False"` ensures
auto-print is off when the parameter hasn't been set yet (e.g. fresh
install before the user visits the settings page).
