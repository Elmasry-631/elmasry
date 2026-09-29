# Gap Analysis — el_restrict_journal

## Requirement → Standard Module Mapping

| # | Requirement | Standard Module | Coverage | Custom Work Needed? |
|---|-------------|-----------------|----------|---------------------|
| 1 | Per-user journal restriction (create/write) | None (CE) | ❌ None | ✅ YES — extend `res.users` + `account.move` + `account.payment` |
| 2 | Per-user journal visibility (read-only on restricted) | None (CE) | ❌ None | ✅ YES — record rules on `account.journal`, `account.move`, `account.payment` |
| 3 | User configuration UI | `base` (res.users form) | ⚠ Partial | ✅ YES — inherit user form to add `journal_ids` field |
| 4 | Journal multi-company isolation | `base` (record rules) | ✅ Full | ❌ NO — Odoo's default `account.journal` multi-company rule already filters by `company_ids` |
| 5 | Group-based accounting permissions | `account` (groups) | ✅ Full | ❌ NO — uses `account.group_account_invoice`, `account.group_account_manager` as base |
| 6 | ValidationError on restricted action | `base` (exceptions) | ✅ Full | ❌ NO — uses standard `odoo.exceptions.ValidationError` |
| 7 | Onchange UX feedback | `base` (onchange API) | ✅ Full | ❌ NO — uses standard `@api.onchange` + warning dict |
| 8 | Audit trail of blocked attempts | `mail` (chatter) | ⚠ Partial | ⚠ PARTIAL — `ValidationError` is logged server-side; future iteration could log to `mail.activity` for explicit audit |

## Build Scope (Custom Work)

Based on the GAP analysis, the actual custom build scope is:

1. **Models to extend:**
   - `res.users` — add `journal_ids` Many2many field
   - `account.move` — override `create`, `write`; add `_onchange_journal_id`; add `_check_journal_not_restricted` constrains
   - `account.payment` — override `create`, `write`; add `_check_journal_not_restricted` constrains

2. **Models to build from scratch:** None.

3. **Standard modules to depend on:** `base`, `account`.

4. **Configuration-only (no code):** None — restriction is data-driven (per-user M2M) but the enforcement is code-driven.

## Dependency Decision

| Module | Action | Reason |
|--------|--------|--------|
| `base` | depend | Required for all modules |
| `account` | depend | Provides `account.move`, `account.payment`, `account.journal` |
| `mail` | ❌ NOT direct depend | Already a transitive dep of `account` |
| `web` | ❌ NOT direct depend | Already a transitive dep of `account` |
| `hr_payroll` | ❌ NOT depend | Enterprise-only — breaks CE compatibility |
| `account_edi` | ❌ NOT depend | Not needed — restriction is journal-level, not EDI-level |
| `account_payment` | ❌ NOT direct depend | Sub-module of `account` in Odoo 17+ — included transitively |

## Estimated Effort Reduction

- Requirements that standard Odoo covers: **5 out of 8** (multi-company, groups, ValidationError, onchange, audit infrastructure)
- Effort saved: ~50% (no need to reinvent multi-company rules, group hierarchy, exception handling, onchange UX, audit logging infrastructure)
- Actual custom scope: **3 model extensions + 6 record rules + 1 view inherit + 1 onchange + 2 constrains + 2 security groups**

## What We Are NOT Building (and why)

| Out of Scope | Reason |
|--------------|--------|
| Per-journal configuration UI (reverse direction) | Requirements specify per-user config; reverse direction is a separate feature |
| Time-based restrictions (e.g., restrict only on weekends) | Not in requirements — future iteration |
| Email notification when restriction triggers | Not in requirements — `ValidationError` is sufficient signal |
| Mass-assign journals to multiple users at once | Not in requirements — admin uses standard user list view + bulk edit |
| Audit log table for blocked attempts | Partially out of scope — server log captures tracebacks; full audit table is a future iteration |
