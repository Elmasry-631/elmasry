# Models Documentation — el_cheque_tracking

## `cheque.cheque`

The core cheque model. Tracks both received and issued cheques through
their full lifecycle, posting accounting entries at every state transition.

**Inherits:** `mail.thread`, `mail.activity.mixin`
**Order:** `cheque_date desc, id desc`
**Rec name:** `name`

### Fields

See `architecture/model-design.md` for the full field inventory.

### Lifecycle methods

See `api.md` for the full method reference.

### Constraints

1. **Unique cheque per company:** `(cheque_number, bank_id, cheque_date, company_id)` must be unique.
2. **Positive amount:** `amount > 0`.
3. **Due date after cheque date:** `due_date >= cheque_date` (or NULL).

### Computed fields

- `amount_company_currency` — converts `amount` to company currency using
  `exchange_rate` if set, otherwise the automatic currency rate.
- `is_post_dated` — True if `due_date > today`.
- `is_stale` — True if `cheque_date` is older than `company_id.cheque_stale_months`
  months AND state is holding/deposited.
- `days_until_due`, `days_in_state` — computed day counts.
- `move_count`, `payment_count`, `return_count` — record-set size counters.
- `last_return_date` — max `return_date` from `return_ids`.

---

## `cheque.deposit`

Batch deposit model. Groups multiple holding received cheques into a single
deposit batch posted to one bank journal.

**Inherits:** `mail.thread`
**Order:** `deposit_date desc, id desc`

### Fields

- `name` (Char, sequence-prefilled)
- `deposit_date` (Date, required, default=today)
- `bank_journal_id` (Many2one → account.journal, domain=bank, required)
- `cheque_ids` (Many2many → cheque.cheque, domain=received+holding/returned)
- `total_amount` (Monetary, computed+stored)
- `currency_id` (Many2one → res.currency, required, default=company currency)
- `state` (Selection: draft/confirmed/cancelled)
- `notes` (Text)
- `company_id` (Many2one → res.company, required, default=current)

### Methods

- `action_confirm()` — confirms the deposit, triggers `action_deposit` on each cheque.
- `action_cancel()` — cancels (only draft deposits).
- `action_print_slip()` — returns the deposit slip report action.

---

## `cheque.return`

Return record. One per return event on a cheque.

**Order:** `return_date desc, id desc`

### Fields

- `name` (Char, sequence-prefilled)
- `cheque_id` (Many2one → cheque.cheque, required, ondelete=restrict)
- `return_date` (Date, required, default=today)
- `return_reason_id` (Many2one → cheque.return.reason, required)
- `bank_charges` (Monetary, default=0.0)
- `penalty_amount` (Monetary, default=0.0)
- `currency_id` (Many2one → res.currency, related=cheque_id.currency_id)
- `company_id` (Many2one → res.company, related=cheque_id.company_id, stored)
- `notes` (Text)
- `move_ids` (One2many → account.move via cheque_return_id)

---

## `cheque.return.reason`

Config model for return reasons.

**Order:** `sequence, id`

### Fields

- `name` (Char, required, translate=True)
- `code` (Char, required)
- `sequence` (Integer, default=10)
- `active` (Boolean, default=True)
- `default_penalty` (Monetary, default=0.0)
- `currency_id` (Many2one → res.currency, default=company currency)
- `company_id` (Many2one → res.company, required, default=current)

### Constraint

- `_code_uniq`: `(code, company_id)` must be unique.

---

## `res.partner` (extension)

Adds 5 computed cheque stat counters + 1 computed currency field + 2 smart
buttons.

### Computed fields

- `received_cheque_count` (Integer)
- `issued_cheque_count` (Integer)
- `bounced_cheque_count` (Integer)
- `total_cheque_received` (Monetary, currency_field=company_currency_id)
- `total_cheque_issued` (Monetary, currency_field=company_currency_id)
- `company_currency_id` (Many2one → res.currency, computed+searchable)

### Methods

- `_compute_cheque_stats()` — uses `read_group` to avoid N+1.
- `_compute_company_currency_id()` — resolves the partner's company currency.
- `_search_company_currency_id()` — search fallback.
- `action_view_received_cheques()` / `action_view_issued_cheques()` — smart button actions.

---

## `res.company` (extension)

Adds 5 cheque accounts + 4 operational thresholds.

### Fields

- `cheque_received_account_id` (Many2one → account.account)
- `cheque_under_collection_account_id` (Many2one → account.account)
- `cheque_issued_account_id` (Many2one → account.account)
- `cheque_penalty_income_account_id` (Many2one → account.account)
- `cheque_bank_charges_account_id` (Many2one → account.account)
- `cheque_stale_months` (Integer, default=6)
- `cheque_pdc_reminder_days` (Integer, default=7)
- `cheque_max_redeposits` (Integer, default=2)
- `cheque_approval_threshold` (Monetary, default=50000.0)

---

## `res.config.settings` (extension)

Exposes all company cheque fields via `related=` + `readonly=False` so they
can be edited from the Settings UI.

---

## `account.move` (extension)

Adds `cheque_id`, `cheque_return_id`, `cheque_stage`.

---

## `account.payment` (extension)

Adds `cheque_id` + a consistency constraint + an onchange.

### Constraint

- `_check_cheque_consistency`: if `cheque_id` is set, validates that
  `cheque_type` matches `payment_type` and `partner_id` matches.

### Onchange

- `_onchange_cheque_id`: pre-fills `partner_id`, `amount`, `currency_id`
  from the selected cheque.

---

## `account.payment.register` (extension)

Adds `cheque_id` and passes it to the payment creation vals.

---

## `account.payment.method` (extension)

Adds `cheque_tracking_enabled` boolean (extension point for future use).
