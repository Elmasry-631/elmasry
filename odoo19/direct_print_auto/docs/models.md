# Models Reference — `direct_print_auto`

## `direct.print.mixin` (AbstractModel)

**File:** `models/direct_print_mixin.py`

Shared logic for direct-printable models. Never instantiated directly.

### Methods

#### `_get_direct_print_report_ref(self)` → `str`

**Abstract.** Each concrete model must override this to return the
XML ID of the report to print.

**Returns:** the report's XML ID (e.g. `"sale.action_report_saleorder"`).

**Raises:** `NotImplementedError` if not overridden.

---

#### `_should_direct_print_auto(self)` → `bool`

Returns `True` when auto-print should fire for `self`.

**Default:** returns `False`. Concrete models override to:
1. Read the relevant toggle from `ir.config_parameter`
2. Apply any domain filter (e.g. customer invoices only)
3. Return `True` only when both conditions are met

**Returns:** boolean.

---

#### `action_direct_print(self)` → `dict`

Entry point for the manual "Direct Print" button on the form view.

**Behaviour:**
1. `self.ensure_one()` — only one record can be manually printed at a time
2. Calls `_get_direct_print_report_ref()` to get the report XML ID
3. Returns a client action dict:
   ```python
   {
       "type": "ir.actions.client",
       "tag": "direct_print_auto",
       "name": "Direct Print",
       "params": {
           "report_ref": "<report xml id>",
           "res_model": self._name,
           "res_ids": self.ids,
           "next_action": False,
       },
   }
   ```

---

#### `_trigger_direct_print_after(self, original_action)` → `dict`

Helper for the auto-print flow. Called by the
confirm/post/validate/approve overrides.

**Behaviour:**
1. If `self` is empty → return `original_action` untouched
2. If `len(self) > 1` → return `original_action` untouched (no multi-record auto-print)
3. If `self[0]._should_direct_print_auto()` returns `False` → return `original_action` untouched
4. Otherwise → return a `direct_print_auto` client action dict with `next_action` set to `original_action`

**Returns:** an action dict (either the original or a wrapped client action).

---

## `res.config.settings` (inherited)

**File:** `models/res_config_settings.py`

Adds 5 boolean toggles to the Sales settings tab.

### Fields

| Field | Type | config_parameter | Default | Purpose |
|-------|------|------------------|---------|---------|
| `direct_print_invoice_auto` | Boolean | `direct_print_auto.invoice_auto` | False | Auto-print customer invoices on `action_post` |
| `direct_print_so_auto` | Boolean | `direct_print_auto.so_auto` | False | Auto-print sales orders on `action_confirm` |
| `direct_print_picking_auto` | Boolean | `direct_print_auto.picking_auto` | False | Auto-print outgoing delivery slips on `button_validate` |
| `direct_print_po_auto` | Boolean | `direct_print_auto.po_auto` | False | Auto-print purchase orders on `button_approve` |
| `direct_print_open_dialog` | Boolean | `direct_print_auto.open_dialog` | True | Manual button: open print dialog (True) vs. download PDF (False) |

---

## `sale.order` (inherited + mixin)

**File:** `models/sale_order.py`

### Methods added

| Method | Returns | Purpose |
|--------|---------|---------|
| `_get_direct_print_report_ref()` | `"sale.action_report_saleorder"` | Report XML ID |
| `_should_direct_print_auto()` | bool | Reads `direct_print_auto.so_auto` from `ir.config_parameter` |
| `action_confirm()` (override) | dict | Calls `super()`, wraps return with `_trigger_direct_print_after` |

---

## `account.move` (inherited + mixin)

**File:** `models/account_move.py`

### Methods added

| Method | Returns | Purpose |
|--------|---------|---------|
| `_get_direct_print_report_ref()` | `"account.account_invoices"` | Report XML ID |
| `_should_direct_print_auto()` | bool | Returns `False` if `move_type not in ('out_invoice', 'out_refund')`. Otherwise reads `direct_print_auto.invoice_auto`. |
| `action_post()` (override) | dict | Calls `super()`, wraps return with `_trigger_direct_print_after` |

---

## `stock.picking` (inherited + mixin)

**File:** `models/stock_picking.py`

### Methods added

| Method | Returns | Purpose |
|--------|---------|---------|
| `_get_direct_print_report_ref()` | `"stock.action_report_delivery"` | Report XML ID |
| `_should_direct_print_auto()` | bool | Returns `False` if `picking_type_id.code != 'outgoing'`. Otherwise reads `direct_print_auto.picking_auto`. |
| `button_validate()` (override) | dict | Calls `super()`, wraps return with `_trigger_direct_print_after` |

---

## `purchase.order` (inherited + mixin)

**File:** `models/purchase_order.py`

### Methods added

| Method | Returns | Purpose |
|--------|---------|---------|
| `_get_direct_print_report_ref()` | `"purchase.action_report_purchase_order"` | Report XML ID |
| `_should_direct_print_auto()` | bool | Reads `direct_print_auto.po_auto` from `ir.config_parameter` |
| `button_approve()` (override) | dict | Calls `super()`, wraps return with `_trigger_direct_print_after` |
