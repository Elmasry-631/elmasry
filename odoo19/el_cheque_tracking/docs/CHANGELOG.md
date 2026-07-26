# Changelog — el_cheque_tracking

All notable changes to this module are documented in this file.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and the project adheres to [Semantic Versioning](https://semver.org/).

## [19.0.1.0.0] — 2026-07-09 — Initial rebuild from scratch

### Added — Models
- `cheque.cheque`: core model with full lifecycle for received + issued cheques,
  3 SQL constraints (`unique cheque_number/bank/date/company`, `amount > 0`,
  `due_date >= cheque_date`), `mail.thread` + `mail.activity.mixin` inherited,
  computed fields (`amount_company_currency`, `is_post_dated`, `is_stale`,
  `days_until_due`, `days_in_state`, `move_count`, `payment_count`,
  `return_count`, `last_return_date`), and 11 lifecycle methods
  (`action_receive`, `action_approve`, `action_deposit`, `action_clear`,
  `action_hand_over`, `action_cash`, `action_return`, `action_void`,
  `action_cancel`, `action_reset_to_draft`, `_apply_return`).
- `cheque.deposit`: batch deposit model with `cheque_ids` (M2M), `total_amount`
  (computed), state machine (draft/confirmed/cancelled), `action_confirm`
  (triggers `action_deposit` on each linked cheque), `action_cancel`,
  `action_print_slip`.
- `cheque.return`: return record with `cheque_id`, `return_date`,
  `return_reason_id`, `bank_charges`, `penalty_amount`, `currency_id` (related),
  `move_ids` (O2M to `account.move.cheque_return_id`).
- `cheque.return.reason`: config model with `name`, `code`, `sequence`,
  `active`, `default_penalty`, `currency_id`, `company_id`, and a unique
  `(code, company_id)` constraint.
- `res.partner` extension: 5 computed fields (`received_cheque_count`,
  `issued_cheque_count`, `bounced_cheque_count`, `total_cheque_received`,
  `total_cheque_issued`) + computed `company_currency_id`, using `read_group`
  to avoid N+1. Two smart-button actions.
- `res.company` extension: 5 cheque accounts (`cheque_received_account_id`,
  `cheque_under_collection_account_id`, `cheque_issued_account_id`,
  `cheque_penalty_income_account_id`, `cheque_bank_charges_account_id`) +
  4 thresholds (`cheque_stale_months`, `cheque_pdc_reminder_days`,
  `cheque_max_redeposits`, `cheque_approval_threshold`).
- `res.config.settings` extension: exposes all company cheque fields with
  `readonly=False` so they can be edited from the Settings UI.
- `account.move` extension: `cheque_id` (M2O), `cheque_return_id` (M2O),
  `cheque_stage` (Selection: receipt/deposit/clearance/return/issue/cash/void).
- `account.payment` extension: `cheque_id` (M2O), consistency constraint
  (`cheque_type` must match `payment_type`), partner match check, onchange
  to prefill partner/amount/currency from the selected cheque.
- `account.payment.register` extension: `cheque_id` field, passed to the
  payment creation vals.
- `account.payment.method` extension: `cheque_tracking_enabled` boolean
  (extension point for future per-method configuration).

### Added — Wizards
- `cheque.deposit.wizard`: select multiple holding/returned cheques + bank
  journal → create `cheque.deposit` + trigger `action_deposit` on each.
  Validates PDC due date + max re-deposit attempts.
- `cheque.return.wizard`: select cheque + return_reason + bank_charges +
  penalty_amount → delegate to `cheque.cheque._apply_return` which reverses
  the latest move + posts optional charges + penalty entries.
- `cheque.print.wizard`: select report type (cheque_print / deposit_slip /
  cheque_register) → return the corresponding `ir.actions.report`.

### Added — Views
- `cheque.cheque`: 6 views (list, form with chatter + statusbar + smart
  buttons, kanban grouped by state, calendar on `due_date`, pivot, graph)
  + comprehensive search view with filters (My Cheques, Pending Deposit,
  Under Collection, Cleared/Cashed, Post-Dated, Stale, This Month) and
  group-by options.
- `cheque.deposit`: list + form (with cheques inline list + statusbar) +
  search view.
- `cheque.return`: list + form (read-only, with journal entries inline).
- `cheque.return.reason`: list (with sequence handle + active toggle) +
  form.
- `res.partner` form: 2 stat buttons (received cheques, issued cheques).
- `res.config.settings`: cheque accounts section + lifecycle rules section.
- `account.payment` form: optional cheque_id field when cheque tracking
  method is selected.
- `account.payment.register` form: optional cheque_id field.
- Top-level menu "Cheque Tracking" with 4 submenus (Received, Issued,
  Operations, Configuration).

### Added — Reports
- `report_cheque_print`: single-cheque PDF layout with `web.external_layout`,
  partner/bank/date/amount details, amount in words, signature lines.
- `report_deposit_slip`: deposit batch PDF with table of cheques + totals.
- `report_cheque_register`: register list PDF with all cheques + their
  states.

### Added — Security
- `security/groups.xml`: ONE `res.groups.privilege` + 3 `res.groups`
  (User, Manager, Administrator) with `privilege_id` + `implied_ids`
  ladder (Odoo 19 pattern — no `ir.module.category`).
- `security/ir.model.access.csv`: 11 ACL rows covering all 7 models +
  3 wizards, per-group (User: read/write/create; Manager: full CRUD).
- `security/ir.rule.xml`: 5 multi-company record rules ensuring each
  cheque-domain record is company-scoped.

### Added — Data
- `data/sequence_data.xml`: 3 sequences (`cheque.cheque` with `CHQ/%(year)s/`
  prefix, `cheque.deposit` with `DEP/%(year)s/`, `cheque.return` with
  `RET/%(year)s/`).
- `data/return_reason_data.xml`: 4 default reasons (NSF, Stale, Damaged,
  Other).
- `data/account_payment_method_data.xml`: 2 cheque payment methods
  (inbound + outbound).
- `data/ir_cron_data.xml`: 2 daily cron jobs (`_cron_pdc_maturity_reminder`
  + `_cron_stale_cheque_detection`).

### Added — i18n
- `i18n/el_cheque_tracking.pot`: 99-msgid translation template.
- `i18n/ar.po`: Arabic translation, 96/99 entries translated.

### Added — Tests
- `tests/test_cheque_lifecycle.py`: 25 comprehensive tests covering
  creation + constraints (1-4), received lifecycle (5), issued lifecycle (6),
  return + void + cancel (7-9), PDC + max re-deposit (10-11), partner stats
  + high-value activity (12-14), cron jobs (15-16), multi-company + security
  (17-19), wizards (20-22), reports (23-25).

### Added — Documentation
- `README.md`: module overview, features, install, configuration, usage,
  security groups, file inventory.
- `docs/CHANGELOG.md`: this file.
- `docs/IMPLEMENTATION_REPORT.md`: build report.
- `docs/architecture/model-design.md`: model inventory.
- `docs/architecture/state-machine-design.md`: state diagrams.
- `docs/architecture/data-flow.md`: accounting entry flow.
- `docs/architecture/dependencies-map.md`: module dependencies.
- `docs/architecture/gap-analysis.md`: standard Odoo coverage.
- `docs/architecture/alignment-decision.md`: design decisions.
- `docs/architecture/impact-analysis.md`: impact on existing modules.
- `docs/configuration.md`: setup guide.
- `docs/security.md`: security documentation.
- `docs/testing.md`: how to run tests.
- `docs/workflows.md`: user workflows.
- `docs/api.md`: model API reference.
- `docs/views.md`: view inventory.
- `docs/models.md`: detailed model documentation.
- `docs/icon-design.md`: icon design notes.
- `docs/build-report.md`: build process report.

### Added — Static
- `static/description/icon.png`: 200×200 module icon (navy background with
  amber "CHQ" text and accent stripe, generated with Pillow).

### Pattern compliance (Odoo 19)
- Uses `models.Constraint` (not `_sql_constraints`).
- Uses `<list>` (not `<tree>`) in all list views.
- Uses `invisible=` / `readonly=` / `required=` (not `attrs=`).
- Uses `res.groups.privilege` + `privilege_id` (not `ir.module.category` +
  `category_id`).
- Uses `@api.model_create_multi` for `create` overrides.
- Uses `read_group` for partner cheque stats (no N+1).
- Uses `<chatter/>` shortcut for chatter in form views.
- Manifest version prefix `19.0.`.
- All `_()` calls have corresponding entries in `ar.po`.
