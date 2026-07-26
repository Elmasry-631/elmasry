# API Reference — el_cheque_tracking

## `cheque.cheque` model

### Lifecycle methods

#### `action_receive()`
- **Trigger:** User clicks "Receive" button on a draft received cheque.
- **Preconditions:** `cheque_type == 'received'` AND `state == 'draft'`.
- **Effect:** Posts a receipt entry (Dr Cheques Received / Cr Receivable),
  sets `state = 'holding'`, posts a chatter message.
- **Raises:** `UserError` if preconditions not met.

#### `action_approve()`
- **Trigger:** User clicks "Approve" button on a draft issued cheque.
- **Preconditions:** `cheque_type == 'issued'` AND `state == 'draft'`.
- **Effect:** Posts an issue entry (Dr Payable / Cr Cheques Issued),
  sets `state = 'approved'`, posts chatter.
- **Raises:** `UserError` if preconditions not met.

#### `action_hand_over()`
- **Trigger:** User clicks "Hand Over" button on an approved issued cheque.
- **Preconditions:** `cheque_type == 'issued'` AND `state == 'approved'`.
- **Effect:** Sets `state = 'handed_over'`, sets `handover_date = today`,
  posts chatter. No accounting entry.
- **Raises:** `UserError` if preconditions not met.

#### `action_deposit()`
- **Trigger:** User clicks "Deposit" button, OR called by deposit wizard.
- **Preconditions:** `cheque_type == 'received'` AND
  `state in ('holding', 'returned')`.
- **Validations:**
  - If `is_post_dated` AND `due_date > today`: raise `UserError`.
  - If `state == 'returned'` AND `return_count >= cheque_max_redeposits`:
    raise `UserError`.
- **Effect:** Posts a deposit entry (Dr Under Collection / Cr Cheques Received),
  sets `state = 'deposited'`, posts chatter.

#### `action_clear()`
- **Trigger:** User clicks "Clear" button on a deposited cheque.
- **Preconditions:** `cheque_type == 'received'` AND `state == 'deposited'`.
- **Effect:** Posts a clearance entry (Dr Bank / Cr Under Collection),
  sets `state = 'cleared'`, posts chatter.

#### `action_cash()`
- **Trigger:** User clicks "Cash" button on a handed-over issued cheque.
- **Preconditions:** `cheque_type == 'issued'` AND `state == 'handed_over'`.
- **Effect:** Posts a cashing entry (Dr Cheques Issued / Cr Bank),
  sets `state = 'cashed'`, posts chatter.

#### `action_return()`
- **Trigger:** User clicks "Return" button.
- **Preconditions:** `state in ('deposited', 'cleared', 'handed_over')`.
- **Returns:** An action dict opening the `cheque.return.wizard` form with
  `default_cheque_id` set.

#### `_apply_return(return_date, reason_id, bank_charges=0.0, penalty_amount=0.0)`
- **Trigger:** Called by `cheque.return.wizard.action_submit_return()`.
- **Effect:**
  1. Creates a `cheque.return` record.
  2. Reverses the latest posted move on the cheque.
  3. If `bank_charges > 0`: posts a bank-charges move (Dr Bank Charges / Cr Bank).
  4. If `penalty_amount > 0`: posts a penalty move (Dr Receivable / Cr Penalty Income).
  5. Sets `state = 'returned'`, posts chatter, schedules a follow-up activity.
- **Returns:** The created `cheque.return` record.

#### `action_void()`
- **Trigger:** User clicks "Void" button.
- **Preconditions:** `cheque_type == 'issued'` AND
  `state in ('draft', 'approved', 'handed_over')`.
- **Effect:** Reverses any posted moves, sets `state = 'void'`, posts chatter.

#### `action_cancel()` / `action_reset_to_draft()`
- Cancel: `state == 'draft'` → `state == 'cancelled'`.
- Reset: `state == 'cancelled'` → `state == 'draft'`.

### Helper methods (private)

- `_is_high_value()` → bool
- `_create_high_value_activity()`
- `_to_company_currency(amount, date=None)` → float
- `_require_account(account_field, label)` → `account.account`
- `_require_bank_journal_default_account()` → `account.account`
- `_require_partner_account()` → `account.account` (receivable or payable)
- `_post_cheque_move(stage, date, lines, ref=None)` → `account.move`
- `_reverse_move(move, reason=None)` → `account.move`

### Cron jobs (model methods)

#### `_cron_pdc_maturity_reminder()`
- **Scheduled:** Daily.
- **Effect:** For each company, finds received cheques in `holding` state
  with `due_date` in `[today, today + reminder_days]`, schedules an activity
  on each.

#### `_cron_stale_cheque_detection()`
- **Scheduled:** Daily.
- **Effect:** Finds cheques in `holding` or `deposited` state where
  `is_stale == True`, posts a chatter note + schedules a follow-up activity.

## `cheque.deposit` model

#### `action_confirm()`
- **Preconditions:** `state == 'draft'` AND `cheque_ids` is not empty.
- **Effect:** For each linked cheque, sets `deposit_account_id` +
  `deposit_id`, then calls `cheque.action_deposit()`. Sets
  `state = 'confirmed'`.

#### `action_cancel()`
- **Preconditions:** `state == 'draft'` (confirmed deposits cannot be
  cancelled — return the cheques first).
- **Effect:** Sets `state = 'cancelled'`.

#### `action_print_slip()`
- **Returns:** Report action for `action_report_deposit_slip`.

## Wizards

### `cheque.deposit.wizard`
- `default_get()` pre-fills `cheque_ids` from active_ids context.
- `action_create_deposit()` → creates `cheque.deposit`, calls
  `action_confirm()`, returns action to open the new deposit form.

### `cheque.return.wizard`
- `_onchange_return_reason_id()` pre-fills `penalty_amount` from the
  reason's `default_penalty`.
- `action_submit_return()` → calls `cheque._apply_return()`, returns
  action to open the new return form.

### `cheque.print.wizard`
- `default_get()` pre-fills `cheque_ids` from active_ids context.
- `action_print()` → returns the selected report action.
