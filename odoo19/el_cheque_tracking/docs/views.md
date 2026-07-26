# Views Inventory — el_cheque_tracking

## `cheque.cheque` views

| View ID | Type | Purpose |
|---|---|---|
| `cheque_cheque_list` | list | List of all cheques with key fields + state badge |
| `cheque_cheque_form` | form | Full form with header buttons, statusbar, smart buttons, notebook (Invoices / Journal Entries / Returns / Notes), chatter |
| `cheque_cheque_kanban` | kanban | Grouped by state, card shows name + cheque_number + partner + amount |
| `cheque_cheque_calendar` | calendar | On `due_date`, colored by `cheque_type` |
| `cheque_cheque_pivot` | pivot | Rows: cheque_type, Cols: state, Measure: amount_company_currency |
| `cheque_cheque_graph` | graph | Bar chart: state (rows) vs amount_company_currency (measure) |
| `cheque_cheque_search` | search | Filters (My, Pending, Under Collection, Cleared, PDC, Stale, This Month) + Group By |

### Actions
| Action ID | Name | Domain |
|---|---|---|
| `action_cheque_received` | Received Cheques | `[('cheque_type', '=', 'received')]` |
| `action_cheque_issued` | Issued Cheques | `[('cheque_type', '=', 'issued')]` |
| `action_cheque_all` | All Cheques | (none) |

## `cheque.deposit` views

| View ID | Type | Purpose |
|---|---|---|
| `cheque_deposit_list` | list | List of deposits |
| `cheque_deposit_form` | form | Header (Confirm / Cancel / Print Slip buttons + statusbar), fields, cheques inline list |
| `cheque_deposit_search` | search | Filters (Draft, Confirmed) + Group By (Bank Journal, Status) |

### Action
- `action_cheque_deposit` — opens the deposits list.

## `cheque.return` views

| View ID | Type | Purpose |
|---|---|---|
| `cheque_return_list` | list | List of returns |
| `cheque_return_form` | form | Read-only form with cheque link, reason, charges, penalty, journal entries |
| `cheque_return_search` | search | Group By (Reason, Date) |

### Action
- `action_cheque_return` — opens the returns list.

## `cheque.return.reason` views

| View ID | Type | Purpose |
|---|---|---|
| `cheque_return_reason_list` | list | List with sequence handle + active toggle |
| `cheque_return_reason_form` | form | Simple form |

### Action
- `action_cheque_return_reason` — opens the return reasons list.

## Extended views (inherited)

| View ID | Inherits | What's added |
|---|---|---|
| `res_partner_cheque_stat_buttons` | `base.view_partner_form` | 2 stat buttons (received/issued cheques) |
| `res_config_settings_view_form` | `account.res_config_settings_view_form` | Cheque accounts + lifecycle rules sections |
| `account_payment_form_cheque` | `account.view_account_payment_form` | Cheque ID field (visible when cheque tracking method) |
| `account_payment_register_form_cheque` | `account.view_account_payment_register_form` | Cheque ID field (visible for cheque methods) |

## Menus

| Menu ID | Name | Parent | Action |
|---|---|---|---|
| `menu_cheque_tracking_root` | Cheque Tracking | (root) | — |
| `menu_cheque_received` | Received | root | — |
| `menu_cheque_received_list` | Received Cheques | Received | `action_cheque_received` |
| `menu_cheque_deposit_list` | Deposits | Received | `action_cheque_deposit` |
| `menu_cheque_issued` | Issued | root | — |
| `menu_cheque_issued_list` | Issued Cheques | Issued | `action_cheque_issued` |
| `menu_cheque_operations` | Operations | root | — |
| `menu_cheque_all_list` | All Cheques | Operations | `action_cheque_all` |
| `menu_cheque_return_list` | Returns | Operations | `action_cheque_return` |
| `menu_cheque_config` | Configuration | root | — |
| `menu_cheque_return_reason` | Return Reasons | Configuration | `action_cheque_return_reason` |
