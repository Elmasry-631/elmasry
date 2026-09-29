# Requirements Specification — el_restrict_journal

## 1. Overview
- **Module Name:** el_restrict_journal
- **Target Odoo Version:** 19
- **Category:** Accounting/Management
- **Summary:** Restrict specific account journals from being used by selected users (defense-in-depth: record rules + Python enforcement).
- **Author:** Ibrahim Elmasry

## 2. Business Problem
In multi-user Odoo deployments, accounting teams frequently need to **isolate journals** so that specific users cannot accidentally (or deliberately) post entries to sensitive journals such as:
- Payroll journal (only HR-accountant should post)
- Tax adjustment journal (only senior accountant)
- Year-end closing journal (only chief accountant)
- Director's expense journal (only director's assistant)

Without this module, the only option is to grant users broad access to all journals via the `account.group_account_invoice` / `account.group_account_manager` groups, which exposes every journal to every accountant. This module adds a **per-user "restricted journals" list** to `res.users`; once a journal is added to a user's restricted list, that user:

1. Cannot select the journal in new `account.move` or `account.payment` records (Python-side `ValidationError`).
2. Sees the journal as **read-only** in lists (record rules with `perm_write=False, perm_create=False, perm_unlink=False`).
3. Cannot change an existing record's journal to a restricted one.

The cost of NOT having this module: accidental postings to wrong journals → reconciliation mismatches → auditor findings → month-end delays. Typical finance teams lose 4–8 hours per month correcting these errors manually.

## 3. Functional Requirements

### 3.1 Models
| # | Model Name | Purpose | Inherits | Key Fields |
|---|-----------|---------|----------|------------|
| 1 | res.users (extend) | Add restricted journals per user | _inherit='res.users' | journal_ids |
| 2 | account.move (extend) | Block create/write with restricted journal | _inherit='account.move' | (no new field) |
| 3 | account.payment (extend) | Block create/write with restricted journal | _inherit='account.payment' | (no new field) |

### 3.2 Fields per Model

#### res.users (extension)
| Field | Type | Required | Index | Tracking | Notes |
|-------|------|----------|-------|----------|-------|
| journal_ids | Many2many → account.journal | No | No | No | "Restricted Journals" — journals this user CANNOT use. Empty = no restriction. |

#### account.move (extension)
No new fields. Only method overrides.

#### account.payment (extension)
No new fields. Only method overrides.

### 3.3 State Machines
No state machines — this is a security/enforcement module, not a workflow module.

### 3.4 Views Required
| View ID | Type | Model | Purpose |
|---------|------|-------|---------|
| view_users_form_restrict_journal | form (inherit) | res.users | Add "Restricted Journals" tab on user form |
| view_account_move_form_restrict_journal | form (inherit) | account.move | (No UI change; readonly guard via Python) |
| view_account_journal_form_restrict_journal | form (inherit) | account.journal | Show "Restricted for users" smart button (count) |

### 3.5 Actions & Menus
No new menus — configuration is done through the standard Settings → Users form (admin only).

### 3.6 Security
| Group | Name | Permissions | Stakeholder |
|-------|------|-------------|-------------|
| group_restrict_journal_user | Restricted Journal: User | Implicit, automatically enforced when admin assigns journals | Accountant |
| group_restrict_journal_manager | Restricted Journal: Manager | Can configure restrictions on users | Chief Accountant / Admin |

**Record Rules:**
| Rule | Model | Domain | Perms | Applies To |
|------|-------|--------|-------|------------|
| rule_journal_unrestricted | account.journal | `[('id', 'not in', user.journal_ids.ids)]` | RWCUD | group_user |
| rule_journal_restricted_readonly | account.journal | `[('id', 'in', user.journal_ids.ids)]` | R only | group_user |
| rule_move_unrestricted | account.move | `[('journal_id', 'not in', user.journal_ids.ids)]` | RWCUD | group_user |
| rule_move_restricted_readonly | account.move | `[('journal_id', 'in', user.journal_ids.ids)]` | R only | group_user |
| rule_payment_unrestricted | account.payment | `[('journal_id', 'not in', user.journal_ids.ids)]` | RWCUD | group_user |
| rule_payment_restricted_readonly | account.payment | `[('journal_id', 'in', user.journal_ids.ids)]` | R only | group_user |

### 3.7 Reports
None.

### 3.8 Wizards
None.

### 3.9 Email Templates
None.

### 3.10 Cron Jobs
None.

## 4. Non-Functional Requirements
- **Performance:** Single index hit per move/payment write — negligible overhead.
- **Multi-company:** Yes — `journal_ids` filtered by `company_id` automatically because `account.journal` has `company_id`. Record rules apply per-user.
- **Multi-currency:** Not applicable.
- **Mobile:** No mobile-specific UI changes.
- **i18n:** Arabic + English.
- **Backwards Compatibility:** Admin user (with empty `journal_ids`) is never restricted — preserves default Odoo behavior when no restrictions configured.

## 5. Dependencies
| Module | Reason |
|--------|--------|
| base | Required (res.users extension) |
| account | Required (account.move, account.payment, account.journal) |

## 6. Constraints
- NO Enterprise module dependencies (CE compatible only)
- NO deprecated patterns (Odoo 19+)
- Author: Ibrahim Elmasry (LAW 18)
- Defense-in-depth: record rules + Python enforcement (belt and suspenders)
- NO computed field that raises ValidationError (anti-pattern from original module — explicitly forbidden)
- NO `from . import wizard` if no wizard folder exists (original bug)

## 7. Open Questions
None — requirements are clear from the original (broken) module + standard accounting practice.

## 8. Acceptance Criteria
- [ ] Module installs without errors on Odoo 19
- [ ] All 13+ tests pass
- [ ] Pre-flight validation: 0 errors
- [ ] Documentation: 7+ files in docs/
- [ ] Arabic translations: 10+ entries
- [ ] Module icon: 256×256 PNG < 100KB
- [ ] User with restricted journals CANNOT create account.move with restricted journal (Python ValidationError)
- [ ] User with restricted journals CANNOT create account.payment with restricted journal (Python ValidationError)
- [ ] User with restricted journals sees restricted journals as READ-ONLY in lists (record rule)
- [ ] Admin user (no restricted journals configured) behaves identically to vanilla Odoo

## 9. Requirements Traceability Matrix

| # | Requirement | Model.Field | View | Test Method | Doc Section |
|---|-------------|-------------|------|-------------|-------------|
| 1 | res.users.journal_ids | res.users.journal_ids | view_users_form_restrict_journal | test_01_user_journal_ids_field | models.md §1 |
| 2 | Block account.move create w/ restricted journal | account.move.create() override | — | test_02_move_create_blocked | security.md §1 |
| 3 | Block account.move write w/ restricted journal | account.move.write() override | — | test_03_move_write_blocked | security.md §1 |
| 4 | Block account.payment create w/ restricted journal | account.payment.create() override | — | test_04_payment_create_blocked | security.md §1 |
| 5 | Block account.payment write w/ restricted journal | account.payment.write() override | — | test_05_payment_write_blocked | security.md §1 |
| 6 | Account.journal record rule (unrestricted full access) | ir.rule rule_journal_unrestricted | — | test_06_journal_rule_unrestricted | security.md §2 |
| 7 | Account.journal record rule (restricted read-only) | ir.rule rule_journal_restricted_readonly | — | test_07_journal_rule_readonly | security.md §2 |
| 8 | Account.move record rule | ir.rule rule_move_* | — | test_08_move_rule | security.md §2 |
| 9 | Account.payment record rule | ir.rule rule_payment_* | — | test_09_payment_rule | security.md §2 |
| 10 | Admin user not restricted | res.users.journal_ids empty | — | test_10_admin_not_restricted | models.md §2 |
| 11 | onchange clears restricted journal | account.move._onchange_journal_id | — | test_11_onchange_journal | workflows.md §1 |
| 12 | Multi-journal restriction (>=2 journals) | res.users.journal_ids | — | test_12_multi_journal | models.md §3 |
| 13 | Group membership enforcement | res.groups group_restrict_journal_user | — | test_13_group_membership | security.md §3 |
