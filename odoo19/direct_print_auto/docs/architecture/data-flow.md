# Data Flow — `direct_print_auto`

This document traces the end-to-end data flow for both the **manual
button** and the **auto-print** paths.

---

## Flow 1 — Manual "Direct Print" button

User clicks the Direct Print button on a sales order form.

```
[User clicks "Direct Print" button on sale.order form]
                │
                ▼
[Odoo dispatches button call: sale.order.action_direct_print()]
                │
                ▼
[direct.print.mixin.action_direct_print(self)]
   ─ self.ensure_one()
   ─ report_ref = self._get_direct_print_report_ref()
        └→ returns "sale.action_report_saleorder"
   ─ returns client action dict:
       {
         "type": "ir.actions.client",
         "tag": "direct_print_auto",
         "params": {
           "report_ref": "sale.action_report_saleorder",
           "res_model": "sale.order",
           "res_ids": [42],
           "next_action": false
         }
       }
                │
                ▼
[Odoo's web client receives the action dict]
   ─ looks up the OWL component registered under tag="direct_print_auto"
   ─ instantiates DirectPrintAction with this.props.action = the dict
                │
                ▼
[DirectPrintAction.setup()]
   ─ reads this.props.action.params
   ─ builds URL: /report/html/sale.action_report_saleorder/42
   ─ assigns URL to iframe.src via this.state.frameSrc
                │
                ▼
[Browser fetches /report/html/sale.action_report_saleorder/42]
   ─ Odoo backend renders the QWeb report as HTML
   ─ ACL check: does the user have read access on sale.order(42)?
       └→ yes: HTML returned
       └→ no: 403 returned (caught by iframe.onerror)
                │
                ▼
[iframe load event fires → DirectPrintAction.onFrameLoad()]
   ─ checks this._printed flag (guard against double-trigger)
   ─ setTimeout(350ms) — let report CSS/fonts settle
   ─ frame.focus()
   ─ frame.contentWindow.print()   ← browser native print dialog opens
                │
                ▼
[User picks printer, clicks Print or Cancel]
                │
                ▼
[setTimeout(400ms) after print() returns → DirectPrintAction._dispatchNext()]
   ─ params.next_action is false
   ─ dispatches {type: "ir.actions.act_window_close"}
   ─ client action closes, user returns to the SO form
```

---

## Flow 2 — Auto-print on confirm

User opens a sales order, clicks "Confirm" (with the SO auto-print
toggle enabled in settings).

```
[User clicks "Confirm" on sale.order form]
                │
                ▼
[Odoo dispatches button call: sale.order.action_confirm()]
                │
                ▼
[sale_order.action_confirm(self)]  ← our override
   ─ action = super().action_confirm()
       └→ standard Odoo confirm: state=draft → state=sale, returns action dict
   ─ return self._trigger_direct_print_after(action)
                │
                ▼
[direct.print.mixin._trigger_direct_print_after(self, action)]
   ─ check: self exists? yes
   ─ check: len(self) == 1? yes (single-record operation)
   ─ check: self[0]._should_direct_print_auto()?
       └→ reads ir.config_parameter "direct_print_auto.so_auto"
       └→ "true" → returns True
   ─ returns wrapped client action:
       {
         "type": "ir.actions.client",
         "tag": "direct_print_auto",
         "params": {
           "report_ref": "sale.action_report_saleorder",
           "res_model": "sale.order",
           "res_ids": [42],
           "next_action": <original confirm action dict>  ← captured super() return
         }
       }
                │
                ▼
[Odoo dispatches the direct_print_auto client action]
   ─ same OWL flow as Flow 1 steps 4-9
   ─ print dialog opens, user prints
                │
                ▼
[After print dialog closes → DirectPrintAction._dispatchNext()]
   ─ params.next_action is the original confirm action dict (e.g. {type: "ir.actions.act_window", ...})
   ─ this.actionService.doAction(next_action)
   ─ user is returned to the confirmed SO form view
```

---

## Flow 3 — Auto-print disabled (toggle off)

Same as Flow 2, but the settings toggle is off.

```
[User clicks "Confirm" on sale.order form, toggle off]
                │
                ▼
[sale_order.action_confirm(self)]
   ─ action = super().action_confirm()
   ─ return self._trigger_direct_print_after(action)
                │
                ▼
[direct.print.mixin._trigger_direct_print_after(self, action)]
   ─ check: self exists? yes
   ─ check: len(self) == 1? yes
   ─ check: self[0]._should_direct_print_auto()?
       └→ reads ir.config_parameter "direct_print_auto.so_auto"
       └→ "False" → returns False
   ─ returns action (untouched)   ← original confirm action goes through
                │
                ▼
[User sees the standard confirm flow: SO state changes to "Sale", form reloads]
```

---

## Flow 4 — Multi-record confirm (auto-print skipped)

User multi-selects 5 sales orders in list view, clicks "Confirm" in the
action menu.

```
[User selects 5 SOs, clicks "Confirm" in action menu]
                │
                ▼
[sale_order.action_confirm(self)]   ← self = sale.order(1, 2, 3, 4, 5)
   ─ action = super().action_confirm()   ← standard multi-confirm runs
   ─ return self._trigger_direct_print_after(action)
                │
                ▼
[direct.print.mixin._trigger_direct_print_after(self, action)]
   ─ check: self exists? yes
   ─ check: len(self) == 1?   NO (len is 5)
   ─ returns action (untouched)   ← auto-print skipped, multi-confirm flow continues
                │
                ▼
[User sees the standard multi-confirm flow: 5 SOs confirmed, list reloads]
```

---

## Flow 5 — Customer invoice with vendor bill check

User posts a vendor bill (move_type=in_invoice) with the invoice
auto-print toggle enabled.

```
[User opens vendor bill, clicks "Post"]
                │
                ▼
[account_move.action_post(self)]
   ─ action = super().action_post()
   ─ return self._trigger_direct_print_after(action)
                │
                ▼
[direct.print.mixin._trigger_direct_print_after(self, action)]
   ─ check: self exists? yes
   ─ check: len(self) == 1? yes
   ─ check: self[0]._should_direct_print_auto()?
       └→ self.move_type == "in_invoice" (vendor bill)
       └→ returns False (customer-only filter)
   ─ returns action (untouched)   ← no auto-print for vendor bills
                │
                ▼
[User sees the standard post flow: vendor bill posted, form reloads]
```

This is the domain filter in action: even when the toggle is on, only
the right kind of document auto-prints.
