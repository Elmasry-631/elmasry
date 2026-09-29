# Build Report — el_restrict_journal v2.0.0 (Whitelist)

## Quality Grade

| Dimension | Grade | Notes |
|-----------|-------|-------|
| Manifest | A | All required fields; v2.0.0; whitelist description; correct data[] order |
| Models | A | Clean _inherit; auto group management in res.users.write(); inverted check logic |
| Views | A | "Allowed Journals" tab; help text explains whitelist semantics |
| Security | A | 2 groups + 3 record rules (HIDE non-allowed); auto-membership |
| i18n | A | ar.po with 15+ translations; all user-facing strings translated |
| Tests | A | 14 test methods (added test for auto-group-removal); L2 PASS 14/14 |
| Docs | A | All docs updated to reflect whitelist semantics |
| Pre-flight | PASS | All 5 PRE-* checks PASS |

## Overall: A (PASS)

## v2.0.0 Changes (Whitelist Inversion)

The module was **inverted** from v1.0.0 (blacklist) to v2.0.0 (whitelist) based on user feedback:

| Aspect | v1.0.0 (Blacklist) | v2.0.0 (Whitelist) |
|--------|---------------------|---------------------|
| Field name | `journal_ids` | `allowed_journal_ids` |
| Semantics | "Restricted" (blocked) | "Allowed" (permitted) |
| Empty list | Unrestricted (sees all) | Unrestricted (sees all) — SAME |
| Non-empty list | Listed journals = READ-ONLY; others = full access | Listed journals = full access; others = HIDDEN |
| Non-listed journals | Visible as read-only | **COMPLETELY HIDDEN** (perm_read=False) |
| Record rules | 6 (2 per model: full + readonly) | 3 (1 per model: only allowed) |
| Group membership | Static (admin assigns manually) | **AUTO** (assigned/cleared by write override) |

## Runtime Validation

| Level | Result | Verification |
|-------|--------|--------------|
| L1 (Install Smoke) | ✅ PASS | 51 modules loaded successfully on PostgreSQL 16 |
| L2 (Test Run) | ✅ PASS | 14/14 tests passed (0 failed, 0 errors) |
| L3 (Full Smoke) | ⚠ DEFERRED | L1+L2 sufficient evidence; L3 deferred to user UAT |

## Test Results (L2)

```
TestRestrictJournal.test_01_user_allowed_journal_ids_field ... ok
TestRestrictJournal.test_02_move_create_blocked ... ok
TestRestrictJournal.test_03_move_write_blocked ... ok
TestRestrictJournal.test_04_payment_create_blocked ... ok
TestRestrictJournal.test_05_payment_write_blocked ... ok
TestRestrictJournal.test_06_admin_not_restricted ... ok
TestRestrictJournal.test_07_move_create_allowed ... ok
TestRestrictJournal.test_08_payment_create_allowed ... ok
TestRestrictJournal.test_09_multi_journal_allowed ... ok
TestRestrictJournal.test_10_privilege_escalation_prevented ... ok
TestRestrictJournal.test_11_constrains_layer ... ok
TestRestrictJournal.test_12_record_rule_read_allowed ... ok
TestRestrictJournal.test_13_record_rule_non_allowed_hidden ... ok
TestRestrictJournal.test_14_clear_allowed_removes_group ... ok

0 failed, 0 error(s) of 14 tests
```

## Bug Fixes Applied

| # | Bug | Fix |
|---|-----|-----|
| 1 | `groups_id` field removed in Odoo 19 (was on res.users) | Changed to `group_ids` (Odoo 19 canonical) |
| 2 | Blacklist semantics didn't match user requirement | Inverted to whitelist: only allowed journals visible |
| 3 | Non-listed journals were still visible (read-only) | Changed to completely hidden (perm_read=False on rule) |
| 4 | Group membership was static (admin had to assign manually) | Auto-managed via res.users.write() override |

## Known Limitations

- **Smart button on journal form** — still deferred (xpath issue with `hasclass`)
- **Bulk configuration** — currently requires editing each user individually
- **L3 HTTP smoke test** — deferred to user UAT

## Build Date

2026-07-14 (skill v1.1.0, module v2.0.0)
