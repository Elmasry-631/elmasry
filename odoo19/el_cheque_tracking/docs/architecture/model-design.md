# Model Design — el_cheque_tracking

## Model inventory

| # | Model | Type | Description |
|---|---|---|---|
| 1 | `cheque.cheque` | new | Core cheque model with full lifecycle |
| 2 | `cheque.deposit` | new | Batch deposit model |
| 3 | `cheque.return` | new | Return record model |
| 4 | `cheque.return.reason` | new | Return reason config |
| 5 | `res.partner` | extend | Add cheque stat counters + smart buttons |
| 6 | `res.company` | extend | Add 5 cheque accounts + 4 thresholds |
| 7 | `res.config.settings` | extend | Expose company cheque fields |
| 8 | `account.move` | extend | Add `cheque_id` + `cheque_stage` |
| 9 | `account.payment` | extend | Add `cheque_id` + consistency check |
| 10 | `account.payment.register` | extend | Pass cheque context |
| 11 | `account.payment.method` | extend | Track cheque methods |

## `cheque.cheque` — fields

### Identity
- `name` (Char, sequence-prefilled, readonly, copy=False, required)
- `cheque_type` (Selection: received/issued, required, default=received)
- `cheque_number` (Char, required)
- `cheque_date` (Date, required, default=today)
- `due_date` (Date)
- `payee_name` (Char)

### Amount
- `amount` (Monetary, required, currency_field=currency_id)
- `currency_id` (Many2one → res.currency, required, default=company currency)
- `company_currency_id` (Many2one → res.currency, related=company_id.currency_id)
- `amount_company_currency` (Monetary, computed+stored, currency_field=company_currency_id)
- `exchange_rate` (Float, digits=(12,6))

### Relations
- `partner_id` (Many2one → res.partner, required)
- `bank_id` (Many2one → res.bank, required)
- `bank_branch_id` (Many2one → res.partner)
- `bank_account_id` (Many2one → res.partner.bank)
- `deposit_account_id` (Many2one → account.journal, domain=bank, required)
- `invoice_ids` (Many2many → account.move via cheque_invoice_rel)
- `deposit_id` (Many2one → cheque.deposit, readonly, copy=False)
- `journal_entry_id` (Many2one → account.move, readonly, copy=False)
- `move_ids` (One2many → account.move via cheque_id)
- `payment_ids` (One2many → account.payment via cheque_id)
- `return_ids` (One2many → cheque.return via cheque_id)

### Workflow
- `state` (Selection: draft/holding/deposited/cleared/approved/handed_over/cashed/returned/cancelled/void)
- `responsible_id` (Many2one → res.users, default=current user)
- `handover_date`, `handover_recipient`, `expected_clearing_date`
- `state_changed_date` (Datetime, default=now)
- `is_post_dated`, `is_stale` (Boolean, computed+stored)
- `days_until_due`, `days_in_state` (Integer, computed)
- `notes` (Text)
- `company_id` (Many2one → res.company, required, default=current company)

## `cheque.cheque` — constraints

1. `_cheque_number_bank_date_uniq`: `unique(cheque_number, bank_id, cheque_date, company_id)`
2. `_amount_positive`: `check(amount > 0)`
3. `_due_date_after_cheque_date`: `check(due_date IS NULL OR due_date >= cheque_date)`

## `cheque.cheque` — methods

### Lifecycle (state transitions)
- `action_receive()` — Draft → Holding (posts receipt entry)
- `action_approve()` — Draft → Approved (posts issue entry)
- `action_hand_over()` — Approved → Handed Over (no entry)
- `action_deposit()` — Holding/Returned → Deposited (posts deposit entry)
- `action_clear()` — Deposited → Cleared (posts clearance entry)
- `action_cash()` — Handed Over → Cashed (posts cashing entry)
- `action_return()` — opens return wizard
- `_apply_return(date, reason_id, bank_charges, penalty_amount)` — called by wizard
- `action_void()` — Draft/Approved/Handed Over → Void
- `action_cancel()` — Draft → Cancelled
- `action_reset_to_draft()` — Cancelled → Draft

### Helpers
- `_is_high_value()` — checks against company approval threshold
- `_create_high_value_activity()` — schedules approval activity
- `_to_company_currency(amount, date)` — currency conversion
- `_require_account(account_field, label)` — fetches configured company account
- `_require_bank_journal_default_account()` — fetches bank journal default account
- `_require_partner_account()` — receivable or payable based on cheque_type
- `_post_cheque_move(stage, date, lines, ref)` — creates + posts an account.move
- `_reverse_move(move, reason)` — reverses a posted move

### Smart-button actions
- `action_view_moves()`, `action_view_payments()`

### Cron jobs
- `_cron_pdc_maturity_reminder()` — schedules activities for maturing PDCs
- `_cron_stale_cheque_detection()` — flags stale cheques + posts chatter note
