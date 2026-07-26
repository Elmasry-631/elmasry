# Testing — el_cheque_tracking

## Test suite overview

The module ships 25 tests in `tests/test_cheque_lifecycle.py`, organized in
5 categories:

| Category | Tests | What's covered |
|---|---|---|
| Creation + constraints | 1-4 | draft state, sequence, unique constraint, amount > 0 |
| Received lifecycle | 5 | draft → holding → deposited → cleared (3 posted moves) |
| Issued lifecycle | 6 | draft → approved → handed over → cashed (2 posted moves) |
| Return + void + cancel | 7-9 | return with charges+penalty, issued return, void |
| PDC + max re-deposit | 10-11 | PDC validation, max re-deposit enforcement |
| Partner stats + activity | 12-14 | counters, totals, high-value activity |
| Cron jobs | 15-16 | PDC maturity, stale detection |
| Multi-company + security | 17-19 | company isolation, group membership |
| Wizards | 20-22 | deposit, return, print wizards |
| Reports | 23-25 | cheque register, deposit slip, cheque print |

## Running the tests

### Via Odoo CLI

```bash
# Install + run tests in one command
./odoo-bin -c odoo.conf -d <db> -i el_cheque_tracking     --test-enable --test-tags=/el_cheque_tracking     --stop-after-init --log-level=info
```

### Via Docker (recommended for CI)

```bash
# See docs/build-report.md for the full Docker setup
cd /path/to/el_cheque_tracking_runtime/
docker compose up -d
docker compose exec odoo odoo --stop-after-init -d cheque_test     --test-enable --test-tags=/el_cheque_tracking     -u el_cheque_tracking --log-level=info
```

### Filtering tests

The tests are tagged `@tagged("post_install", "-at_install")`. To run a
specific test:

```bash
./odoo-bin -c odoo.conf -d <db> --test-enable     --test-tags=/el_cheque_tracking:TestChequeLifecycle.test_05_received_lifecycle_full_cycle     --stop-after-init
```

## Test setup

Each test class extends `TransactionCase` and uses `setUpClass` to:
1. Create 5 dedicated cheque accounts (asset_current, asset_current,
   liability_current, income, expense).
2. Configure the demo company with these accounts + thresholds.
3. Create a test partner + test bank.
4. Reuse the demo chart's first bank journal.

The `_base_vals()` helper returns a baseline cheque.cheque vals dict; tests
override specific fields via `**overrides`.

## What the tests do NOT cover

- **UI tests (JS tours)**: not included; would require a running browser
  and `HttpCase`. Add as a follow-up if needed.
- **Performance tests**: no load testing; the `read_group` partner stats
  are tested for correctness, not speed.
- **Currency rate import**: tests use the company currency; multi-currency
  conversion is exercised indirectly via `amount_company_currency` compute.
- **Email sending**: chatter + activities are tested, but actual email
  delivery is not (would require an SMTP server).
