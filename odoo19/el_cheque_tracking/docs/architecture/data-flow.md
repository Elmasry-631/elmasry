# Data Flow — el_cheque_tracking

## Accounting entry flow at each lifecycle transition

### Received cheque — Receipt (Draft → Holding)
1. User clicks **Receive** on a draft received cheque.
2. `cheque.cheque.action_receive()` validates state + cheque_type.
3. Calls `_require_account('cheque_received_account_id', ...)` → company account.
4. Calls `_require_partner_account()` → partner's receivable account.
5. Calls `_post_cheque_move(stage='receipt', date=cheque_date, lines=[...])`.
6. `_post_cheque_move` creates an `account.move` with `cheque_id` + `cheque_stage='receipt'`.
7. `move.action_post()` posts the move.
8. `cheque.journal_entry_id` is set to the new move.
9. `cheque.state = 'holding'`.
10. `cheque.message_post()` records the transition in chatter.

### Received cheque — Deposit (Holding → Deposited)
1. User opens **Batch Deposit Wizard** (selects multiple holding cheques + bank journal).
2. Wizard creates a `cheque.deposit` record + calls `deposit.action_confirm()`.
3. `deposit.action_confirm()` iterates `cheque_ids` and calls `cheque.action_deposit()` for each.
4. Each `cheque.action_deposit()` validates PDC + max re-deposits (if returning).
5. Posts deposit entry: Dr Under Collection / Cr Cheques Received.
6. Sets `cheque.deposit_id = deposit.id`.
7. Sets `cheque.state = 'deposited'`.

### Received cheque — Clearance (Deposited → Cleared)
1. User clicks **Clear** on a deposited cheque.
2. `action_clear()` validates state.
3. Posts clearance entry: Dr Bank / Cr Under Collection.
4. Sets `cheque.state = 'cleared'`.

### Received cheque — Return (Deposited/Cleared → Returned)
1. User clicks **Return** on a deposited/cleared cheque.
2. `action_return()` returns a wizard action.
3. Wizard creates a `cheque.return.wizard` record (cheque_id + return_reason + bank_charges + penalty_amount).
4. `wizard.action_submit_return()` calls `cheque._apply_return(date, reason_id, bank_charges, penalty_amount)`.
5. `_apply_return` creates a `cheque.return` record.
6. Reverses the latest move on the cheque (`_reverse_move`).
7. If `bank_charges > 0`: posts a new move tagged `cheque_stage='return'` with
   Dr Bank Charges / Cr Bank.
8. If `penalty_amount > 0`: posts another move with
   Dr Receivable (partner) / Cr Penalty Income.
9. Sets `cheque.state = 'returned'`.
10. Schedules a follow-up activity.

### Issued cheque — Approve (Draft → Approved)
1. User clicks **Approve** on a draft issued cheque.
2. `action_approve()` validates cheque_type + state.
3. Posts issue entry: Dr Payable (partner) / Cr Cheques Issued.
4. Sets `cheque.state = 'approved'`.

### Issued cheque — Cash (Handed Over → Cashed)
1. User clicks **Cash** on a handed-over issued cheque.
2. `action_cash()` validates state.
3. Posts cashing entry: Dr Cheques Issued / Cr Bank.
4. Sets `cheque.state = 'cashed'`.

## Cron job flow

### `_cron_pdc_maturity_reminder` (daily)
1. For each company in `res.company`:
   2. Compute `date_to = today + reminder_days`.
   3. Search received cheques in `holding` state with `due_date` in `[today, date_to]`.
   4. For each maturing cheque, schedule a `mail.activity` on the cheque.

### `_cron_stale_cheque_detection` (daily)
1. Search all cheques in `holding` or `deposited` state.
2. Filter by `is_stale` (computed based on `company_id.cheque_stale_months`).
3. For each stale cheque:
   - Post a chatter note ("Cheque is stale based on company configuration.").
   - Schedule a follow-up activity.

## Partner stat compute flow

When a partner form is loaded:
1. `_compute_cheque_stats` is triggered.
2. Uses `cheque.cheque.read_group(domain, ['amount_company_currency:sum'], ['partner_id', 'cheque_type'])`.
3. Iterates the grouped result, populating `received_count`, `issued_count`,
   `received_total`, `issued_total` per partner ID.
4. A second `read_group` on `[('state', '=', 'returned')]` populates `bounced_count`.

This avoids N+1: a single SQL query per metric, regardless of how many partners
are being computed.
