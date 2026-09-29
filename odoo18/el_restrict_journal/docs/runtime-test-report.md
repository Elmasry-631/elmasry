# Runtime Test Report — el_restrict_journal v2.0.0 (Whitelist)

## L1: Install Smoke Test

**Status:** ✅ PASS

**Environment:**
- Odoo: 19.0 (via `/tmp/odoo_venv_19/bin/odoo`)
- Database: PostgreSQL 16.14 (via miniconda env `pg`, port 5433)
- Database name: `restrict_journal_db`
- Test date: 2026-07-14

**Result:**
- 51 modules loaded successfully
- Module `el_restrict_journal` v2.0.0 loaded all data files:
  - `security/account_restrict_journal_groups.xml` ✓
  - `security/ir.model.access.csv` ✓
  - `security/account_restrict_journal_rules.xml` ✓
  - `views/res_users_views.xml` ✓
  - `views/account_move_views.xml` ✓

## L2: Test Run

**Status:** ✅ PASS — 14/14 tests passed

```
Starting TestRestrictJournal.test_01_user_allowed_journal_ids_field ...
Starting TestRestrictJournal.test_02_move_create_blocked ...
Starting TestRestrictJournal.test_03_move_write_blocked ...
Starting TestRestrictJournal.test_04_payment_create_blocked ...
Starting TestRestrictJournal.test_05_payment_write_blocked ...
Starting TestRestrictJournal.test_06_admin_not_restricted ...
Starting TestRestrictJournal.test_07_move_create_allowed ...
Starting TestRestrictJournal.test_08_payment_create_allowed ...
Starting TestRestrictJournal.test_09_multi_journal_allowed ...
Starting TestRestrictJournal.test_10_privilege_escalation_prevented ...
Starting TestRestrictJournal.test_11_constrains_layer ...
Starting TestRestrictJournal.test_12_record_rule_read_allowed ...
Starting TestRestrictJournal.test_13_record_rule_non_allowed_hidden ...
Starting TestRestrictJournal.test_14_clear_allowed_removes_group ...

0 failed, 0 error(s) of 14 tests
```

## Key Test Verifications

| Test | What it Verifies | Result |
|------|------------------|--------|
| test_01 | Field `allowed_journal_ids` works + auto group membership | ✅ PASS |
| test_02 | account.move create BLOCKED with non-allowed journal | ✅ PASS |
| test_03 | account.move write BLOCKED when switching to non-allowed | ✅ PASS |
| test_04 | account.payment create BLOCKED with non-allowed journal | ✅ PASS |
| test_05 | account.payment write BLOCKED when switching to non-allowed | ✅ PASS |
| test_06 | Admin user (empty list) NOT blocked — sees all | ✅ PASS |
| test_07 | account.move create SUCCEEDS with allowed journal | ✅ PASS |
| test_08 | account.payment create SUCCEEDS with allowed journal | ✅ PASS |
| test_09 | Multiple journals in allowed list work | ✅ PASS |
| test_10 | Non-manager cannot edit allowed_journal_ids | ✅ PASS |
| test_11 | @api.constrains catches violations | ✅ PASS |
| test_12 | Restricted user CAN READ allowed journal | ✅ PASS |
| test_13 | Restricted user CANNOT SEE non-allowed journal (HIDDEN) | ✅ PASS |
| test_14 | Clearing allowed_journal_ids removes user from group | ✅ PASS |

## Issues Found and Fixed During v2 Build

| # | Issue | Fix |
|---|-------|-----|
| 1 | `groups_id` field removed from res.users in Odoo 19 | Changed to `group_ids` (Odoo 19 canonical name) |
| 2 | Whitelist requires auto group membership (else empty list hides everything) | Added auto-add/auto-remove logic in res.users.write() override |

## Verdict

✅ **L1 + L2 PASS** — module installs cleanly and all 14 tests pass on Odoo 19 + PostgreSQL 16.
