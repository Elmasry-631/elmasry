# GAP Analysis — el_cheque_tracking

## Standard Odoo coverage check

| # | Requirement | Standard module | Coverage | Action |
|---|---|---|---|---|
| 1 | Track received + issued cheques | None | ❌ None | ✅ Build `cheque.cheque` |
| 2 | Accounting entries at lifecycle transitions | `account` (provides `account.move`) | ⚠ Partial | ✅ Extend `account.move` with `cheque_id` + `cheque_stage` |
| 3 | Cheque lifecycle state machine | None | ❌ None | ✅ Build state machine in `cheque.cheque` |
| 4 | Batch deposit processing | None | ❌ None | ✅ Build `cheque.deposit` + wizard |
| 5 | Cheque return with bank charges + penalty | None | ❌ None | ✅ Build `cheque.return` + wizard |
| 6 | Return reason configuration | None | ❌ None | ✅ Build `cheque.return.reason` |
| 7 | Multi-company isolation | `base` | ✅ Full | ❌ Use record rules (no code) |
| 8 | Multi-currency | `base` + `currency_rate_live` | ✅ Full | ❌ Use existing `currency_id._convert` |
| 9 | Chatter + activities | `mail` | ✅ Full | ❌ Inherit `mail.thread` + `mail.activity.mixin` |
| 10 | PDF reports | `web` (QWeb) | ✅ Full | ❌ Use QWeb templates |
| 11 | Sequences | `base` (ir.sequence) | ✅ Full | ❌ Use data XML |
| 12 | Scheduled actions | `base` (ir.cron) | ✅ Full | ❌ Use data XML |
| 13 | Security groups | `base` | ✅ Full | ❌ Use `res.groups.privilege` (O19 pattern) |
| 14 | Settings page | `base` (res.config.settings) | ✅ Full | ❌ Extend via `related=` fields |
| 15 | Cheque payment method | `account` (account.payment.method) | ✅ Full | ❌ Use data XML |
| 16 | Partner cheque stats | None | ❌ None | ✅ Build computed fields with `read_group` |
| 17 | PDC maturity reminders | None | ❌ None | ✅ Build `_cron_pdc_maturity_reminder` |
| 18 | Stale cheque detection | None | ❌ None | ✅ Build `_cron_stale_cheque_detection` |

## Build scope (custom work)

Based on the GAP analysis, the actual custom build scope is:
1. **New models (4):** `cheque.cheque`, `cheque.deposit`, `cheque.return`, `cheque.return.reason`
2. **Extended models (5):** `res.partner`, `res.company`, `res.config.settings`, `account.move`, `account.payment`
3. **Standard modules to depend on:** `base`, `mail`, `account`
4. **Configuration-only (no code):** multi-company, multi-currency, chatter, PDF reports, sequences, cron, security groups, settings page

## Effort reduction

- Requirements that standard Odoo covers: 11 out of 18
- Effort saved: ~60% (no need to rebuild chatter, cron, sequences, security, settings, QWeb, multi-company, multi-currency)
- Actual custom scope: 4 new models + 5 extensions + 3 wizards + 3 reports + 25 tests
