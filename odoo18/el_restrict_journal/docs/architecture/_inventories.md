# Inventories — el_restrict_journal

## 1. Model Inventory

| # | Model | Type | Inherits | Key Fields | Key Methods | Constraints |
|---|-------|------|----------|------------|-------------|-------------|
| 1 | res.users | _inherit | res.users | journal_ids (Many2many → account.journal) | (none new) | (none) |
| 2 | account.move | _inherit | account.move | (none new) | `create()`, `write()`, `_onchange_journal_id()` | `_check_journal_not_restricted` (api.constrains) |
| 3 | account.payment | _inherit | account.payment | (none new) | `create()`, `write()` | `_check_journal_not_restricted` (api.constrains) |

## 2. View Inventory

| View ID | Type | Model | Inherited View | Fields Used | Buttons |
|---------|------|-------|----------------|-------------|---------|
| view_users_form_restrict_journal | form inherit | res.users | base.view_users_form | journal_ids | — |
| view_account_move_form_restrict_journal | form inherit | account.move | account.view_move_form | (no new fields shown) | — |
| view_account_journal_form_restrict_journal | form inherit | account.journal | account.view_journal_form | (smart button: restricted_user_count) | — |

## 3. Action Inventory

| Action ID | Name | res_model | view_mode | Context |
|-----------|------|-----------|-----------|---------|
| (none — module extends existing actions) | — | — | — | — |

## 4. Button → Method Map

| Button | Model | Method | Visibility |
|--------|-------|--------|-----------|
| (none — no new buttons; only smart button which opens existing user view filtered by journal) | — | — | — |

## 5. Record Rules

| Rule ID | Model | Domain | Group | Perms |
|---------|-------|--------|-------|-------|
| rule_journal_unrestricted_full | account.journal | `[('id', 'not in', user.journal_ids.ids)]` | group_restrict_journal_user | RWCUD |
| rule_journal_restricted_readonly | account.journal | `[('id', 'in', user.journal_ids.ids)]` | group_restrict_journal_user | R only |
| rule_move_unrestricted_full | account.move | `[('journal_id', 'not in', user.journal_ids.ids)]` | group_restrict_journal_user | RWCUD |
| rule_move_restricted_readonly | account.move | `[('journal_id', 'in', user.journal_ids.ids)]` | group_restrict_journal_user | R only |
| rule_payment_unrestricted_full | account.payment | `[('journal_id', 'not in', user.journal_ids.ids)]` | group_restrict_journal_user | RWCUD |
| rule_payment_restricted_readonly | account.payment | `[('journal_id', 'in', user.journal_ids.ids)]` | group_restrict_journal_user | R only |

## 6. Security Groups

| Group XML ID | Name | Implied Groups | Purpose |
|--------------|------|-----------------|---------|
| group_restrict_journal_user | Restricted Journal: User | base.group_user | Receives record rules when admin assigns journals |
| group_restrict_journal_manager | Restricted Journal: Manager | account.group_account_manager | Can configure restrictions on user forms |
