# EL Cheque Tracking

> Comprehensive cheque management module for **Odoo 19** — full lifecycle for both received and issued cheques, with accounting entries at every state transition, multi-company support, batch deposit/return wizards, PDC & stale-cheque monitoring, and three QWeb PDF reports.

**Version** 19.0.1.0.0 · **License** LGPL-3 · **Author** Ibrahim Elmasry

---

## Features

### Received cheques lifecycle
| From → To | Accounting entry |
|---|---|
| Draft → Holding | Dr Cheques Received / Cr Receivable (partner) |
| Holding → Deposited | Dr Under Collection / Cr Cheques Received |
| Deposited → Cleared | Dr Bank / Cr Under Collection |
| Deposited/Cleared → Returned | Reverse to receivable + optional bank charges + penalty |
| Returned → Deposited (re-deposit) | Via batch deposit wizard, with max-attempt validation |

### Issued cheques lifecycle
| From → To | Accounting entry |
|---|---|
| Draft → Approved | Dr Payable (partner) / Cr Cheques Issued |
| Approved → Handed Over | No entry (records physical delivery) |
| Handed Over → Cashed | Dr Cheques Issued / Cr Bank |
| Handed Over → Returned | Reverse issued-cheque liability |
| Draft/Approved/Handed-Over → Void | Voiding path |

### Functional coverage
- Cheque lifecycle states with full chatter tracking + activities.
- Duplicate SQL constraint `(cheque_number, bank, cheque_date, company_id)` unique.
- Multi-company rules via `company_id` + record rules.
- Received & issued cheque list / form / kanban / calendar / pivot / graph views.
- **Batch deposit wizard**, **return wizard** (with bank charges + penalty), **print wizard**.
- Return reason configuration with default data (NSF, Stale, Damaged, Other).
- Partner cheque stat buttons (received count, issued count, bounced count, totals).
- PDC maturity + stale-cheque scheduled actions (`ir.cron`).
- QWeb reports: **cheque print**, **deposit slip**, **cheque register**.
- Settings page for required accounting accounts, stale months, PDC reminder days, max re-deposits, approval threshold.

## Installation

1. Copy the `el_cheque_tracking` folder to your Odoo `addons_path`.
2. Restart Odoo and go to **Apps → Update Apps List**.
3. Search for **EL Cheque Tracking** and click **Install**.

> **Dependencies**: `base`, `mail`, `account`. Configure a chart of accounts and at least one bank journal before using the module.

## Configuration

After installation:

1. Go to **Settings → Accounting → EL Cheque Tracking**.
2. Set the following required accounting accounts:
   - Cheques Received account (current asset)
   - Cheques Under Collection account (current asset)
   - Cheques Issued account (current liability)
   - Cheque Penalty Income account (income)
   - Cheque Bank Charges account (expense)
3. Set operational thresholds:
   - Stale cheque threshold (months)
   - PDC reminder days
   - Max re-deposit attempts
   - High-value approval threshold

## Usage

### Creating a received cheque
1. Go to **Cheque Tracking → Received → Received Cheques → New**.
2. Fill in cheque number, date, due date, amount, partner, bank, deposit journal.
3. Save → click **Receive** to move from Draft → Holding (posts receipt entry).
4. Use the **Batch Deposit** wizard to move Holding → Deposited.
5. After clearance from the bank, click **Clear** to post clearance entry.

### Creating an issued cheque
1. Go to **Cheque Tracking → Issued → Issued Cheques → New**.
2. Set `cheque_type = issued`, fill in fields.
3. Save → click **Approve** (posts issue entry).
4. On physical delivery, click **Hand Over**.
5. Once the bank cashes it, click **Cash** (posts cashing entry).

### Reports
- **Cheque Register** — printable list of all cheques in any state.
- **Deposit Slip** — printable deposit batch document.
- **Print Cheque** — single-cheque print layout.

## Security groups

| Group | Description |
|---|---|
| `Cheque User` | Create and track cheques, deposits, returns |
| `Cheque Manager` | Approve postings, re-deposit returned cheques, void issued cheques |
| `Cheque Administrator` | Full access including configuration and overrides |

## Testing

```bash
# Run the test suite (25 tests) against an Odoo 19 instance with demo data
./odoo-bin -c odoo.conf -d <db> -i el_cheque_tracking \
    --test-enable --test-tags=/el_cheque_tracking --stop-after-init
```

## Files

| Path | Purpose |
|---|---|
| `models/cheque.py` | Core `cheque.cheque` model with lifecycle + accounting methods |
| `models/deposit.py` | Batch deposit model |
| `models/cheque_return.py` | Return record model |
| `models/return_reason.py` | Return reason configuration |
| `models/res_partner.py` | Partner extension with cheque stats (uses `read_group`) |
| `models/res_company.py` | Company-level cheque settings (5 accounts + 4 thresholds) |
| `models/res_config_settings.py` | System-wide config settings |
| `models/account_move.py` | `account.move` extension: `cheque_id` + `cheque_stage` |
| `models/account_payment.py` | `account.payment` extension: `cheque_id` + consistency check |
| `models/account_payment_register.py` | `account.payment.register` extension |
| `models/account_payment_method.py` | `account.payment.method` extension |
| `wizard/deposit_wizard.py` | Batch deposit wizard |
| `wizard/return_wizard.py` | Return processing wizard (with bank charges + penalty) |
| `wizard/print_wizard.py` | Print selection wizard |
| `report/*.xml` | 3 QWeb report templates |
| `security/groups.xml` | `res.groups.privilege` + 3 group records (O19 pattern) |
| `security/ir.rule.xml` | Multi-company record rules |
| `security/ir.model.access.csv` | ACL per group |
| `data/*.xml` | Sequences, return reasons, cron jobs, payment methods |
| `tests/test_cheque_lifecycle.py` | 25 comprehensive tests |
| `i18n/el_cheque_tracking.pot` | Translation template (99 msgids) |
| `i18n/ar.po` | Arabic translation (96/99 translated) |
| `docs/` | Full documentation (architecture, user guide, API, etc.) |

## Author

**Ibrahim Elmasry** — Senior Odoo Developer + DevOps + Implementation Consultant
