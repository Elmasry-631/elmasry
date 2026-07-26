# Impact Analysis — el_cheque_tracking

## Impact on existing modules

### `account`
- **`account.move`**: adds 3 fields (`cheque_id`, `cheque_return_id`,
  `cheque_stage`). Non-breaking — these are nullable Many2one + Selection.
- **`account.payment`**: adds 1 field (`cheque_id`) + 1 constraint
  (`_check_cheque_consistency`) + 1 onchange (`_onchange_cheque_id`).
  Non-breaking — the constraint only fires when `cheque_id` is set.
- **`account.payment.register`**: adds 1 field (`cheque_id`). Non-breaking.
- **`account.payment.method`**: adds 1 boolean field (`cheque_tracking_enabled`).
  Non-breaking.
- **`account.journal`**: no changes (used read-only via `deposit_account_id`).
- **`account.account`**: no changes (used read-only via company config).

### `base`
- **`res.partner`**: adds 6 computed fields (`received_cheque_count`,
  `issued_cheque_count`, `bounced_cheque_count`, `total_cheque_received`,
  `total_cheque_issued`, `company_currency_id`). Non-breaking — all computed.
- **`res.company`**: adds 9 fields (5 accounts + 4 thresholds). Non-breaking.
- **`res.config.settings`**: adds 9 fields (related to company). Non-breaking.
- **`ir.sequence`**: 3 new sequences created via data XML. Non-breaking.
- **`ir.cron`**: 2 new cron jobs created via data XML. Non-breaking.

### `mail`
- **`mail.activity`**: no schema changes; the module schedules activities
  via `activity_schedule()` on `cheque.cheque` (which inherits
  `mail.activity.mixin`).
- **`mail.thread`**: `cheque.cheque` inherits it; chatter is enabled.

## Upgrade safety

- All new fields are nullable or have defaults → no migration needed on
  existing `account.move`, `account.payment`, `res.partner`, `res.company`
  records.
- All new models are independent → no impact on existing tables.
- All constraints use `models.Constraint` (O19 syntax) → forward-compatible.
- All views use modern O19 syntax (`<list>`, `invisible=`, `readonly=`,
  `required=`) → no deprecated patterns.
- Security uses `res.groups.privilege` → forward-compatible.
- Manifest version prefix `19.0.` → correctly scoped.

## Uninstall safety

- Uninstalling the module drops the new tables (`cheque_cheque`,
  `cheque_deposit`, `cheque_return`, `cheque_return_reason`) and removes
  the added fields from `account_move`, `account_payment`,
  `account_payment_register`, `account_payment_method`, `res_partner`,
  `res_company`, `res_config_settings`.
- All `Many2one` fields from this module to standard models use
  `ondelete='restrict'` → no cascade deletion of standard records.
- The 2 cron jobs + 3 sequences + 4 return reasons + 2 payment methods are
  created with `noupdate="1"` → they persist after uninstall unless
  explicitly removed.

## Multi-company impact

- All cheque-domain records carry `company_id` (required, indexed).
- 5 record rules enforce `[('company_id', 'in', company_ids)]` for all 4
  cheque models + 1 user-group rule for return reasons.
- Users without multi-company access will only see cheques in their own
  company.
- The `account.move` records created by this module inherit the cheque's
  `company_id` via the journal's company → no cross-company leakage.
