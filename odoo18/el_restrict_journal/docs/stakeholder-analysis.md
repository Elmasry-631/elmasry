# Stakeholder Analysis — el_restrict_journal

## Stakeholder Matrix

| # | Name/Title | Role | Influence | Impact | Attitude | Engagement |
|---|-----------|------|-----------|--------|----------|------------|
| 1 | CFO / Finance Director | Sponsor | High | High | Supportive | Monthly summary, demo at sign-off |
| 2 | Chief Accountant | Champion | High | High | Supportive | Weekly demo, configure restrictions |
| 3 | Senior Accountant | Key User | Medium | High | Neutral | Training + feedback session |
| 4 | Junior Accountants (5–10) | End User | Low | High | Unknown | Training + announce before go-live |
| 5 | IT / Odoo Admin | IT Admin | Medium | Medium | Supportive | Technical docs, install + maintain |
| 6 | External Auditor | External | Low | Medium | Neutral | Read-only access, evidence trail |

## RACI Matrix

> R = Responsible (does the work) · A = Accountable (owns the outcome — only ONE per task) · C = Consulted (provides input) · I = Informed (kept up to date)

| Task / Deliverable | CFO | Chief Accountant | Senior Accountant | Junior Accountants | IT Admin |
|-------------------|-----|------------------|-------------------|---------------------|----------|
| Requirements approval | A | R | C | I | I |
| Architecture design | I | A | C | — | C |
| Security rules + record rules | I | A | C | — | R |
| Configure restricted journals per user | I | A | R | — | I |
| User acceptance testing | I | A | R | C | I |
| Training materials | I | C | R | I | C |
| Deployment decision | A | R | I | I | C |
| Go-live approval | A | R | C | I | C |
| Post-go-live audit support | I | A | C | — | I |

## Key Concerns to Address
- **Chief Accountant:** "I must be able to override restrictions for myself." → Solution: admin users (with empty `journal_ids`) are never restricted.
- **Junior Accountants:** "Will I see the restricted journals at all?" → Solution: yes, but as **read-only** in lists (so they can read existing entries they need for reference). Creating/editing is blocked.
- **External Auditor:** "Is there an evidence trail?" → Solution: every blocked attempt raises a `ValidationError` which Odoo logs in the chatter / server log. For stronger audit, add `mail.activity` tracking in a future iteration.
- **IT Admin:** "Will this break existing records?" → Solution: NO — record rules only filter what users SEE going forward; existing records remain visible (as read-only if their journal is now restricted).
- **CFO:** "What is the rollback plan?" → Solution: uninstall the module — all overrides and record rules are removed; users regain full access via their existing `account` groups.

## User Roles → Security Groups Mapping

| Stakeholder | Security Group | Permissions |
|-------------|---------------|-------------|
| Chief Accountant | `account.group_account_manager` + implicit `el_restrict_journal.group_restrict_journal_manager` | Configure restrictions + full CRUD on all journals |
| Senior Accountant | `account.group_account_invoice` + `el_restrict_journal.group_restrict_journal_user` (if their journal_ids is non-empty) | Read-write on unrestricted journals, read-only on restricted |
| Junior Accountants | `account.group_account_invoice` + `el_restrict_journal.group_restrict_journal_user` | Read-write on unrestricted journals, read-only on restricted |
| IT Admin | `base.group_system` | Install / configure / maintain |
| External Auditor | `account.group_account_invoice` (read-only via implied) | Read-only access to all accounting records |
