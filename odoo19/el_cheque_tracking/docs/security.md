# Security — el_cheque_tracking

## Security groups

The module defines 3 security groups, organized under one
`res.groups.privilege` (Odoo 19 pattern — no `ir.module.category`).

### `group_cheque_user` — Cheque User
- **Implied by:** `base.group_user`
- **Permissions:**
  - `cheque.cheque`: read, write, create (no unlink)
  - `cheque.deposit`: read, write, create (no unlink)
  - `cheque.return`: read-only
  - `cheque.return.reason`: read-only
  - All 3 wizards: full CRUD (transient)

### `group_cheque_manager` — Cheque Manager
- **Implied by:** `group_cheque_user`
- **Additional permissions:**
  - `cheque.cheque`: full CRUD (including unlink)
  - `cheque.deposit`: full CRUD
  - `cheque.return`: write + create (no unlink — returns are audited)
  - `cheque.return.reason`: full CRUD
- **Workflow capabilities:**
  - Approve issued cheques (`action_approve`)
  - Cash issued cheques (`action_cash`)
  - Return cheques (`action_return`)
  - Void issued cheques (`action_void`)
  - Reset cancelled cheques to draft (`action_reset_to_draft`)
  - Confirm/cancel deposits (`action_confirm`, `action_cancel`)

### `group_cheque_admin` — Cheque Administrator
- **Implied by:** `group_cheque_manager`
- **Default members:** `base.user_root`, `base.user_admin`
- **Additional capabilities:** full access to configuration, settings,
  and security overrides.

## ACL (Access Control List)

Defined in `security/ir.model.access.csv` — 11 rows covering all 7 models +
3 wizards.

| Model | User | Manager |
|---|---|---|
| `cheque.cheque` | r/w/c | r/w/c/u |
| `cheque.deposit` | r/w/c | r/w/c/u |
| `cheque.return` | r | r/w/c |
| `cheque.return.reason` | r | r/w/c/u |
| `cheque.deposit.wizard` | r/w/c/u | (inherited) |
| `cheque.return.wizard` | r/w/c/u | (inherited) |
| `cheque.print.wizard` | r/w/c/u | (inherited) |

## Record rules

Defined in `security/ir.rule.xml` — 5 multi-company rules.

| Rule | Model | Domain |
|---|---|---|
| `cheque_cheque_company_rule` | `cheque.cheque` | `[('company_id', 'in', company_ids)]` |
| `cheque_deposit_company_rule` | `cheque.deposit` | `[('company_id', 'in', company_ids)]` |
| `cheque_return_company_rule` | `cheque.return` | `[('company_id', 'in', company_ids)]` |
| `cheque_return_reason_company_rule` | `cheque.return.reason` | `[('company_id', 'in', company_ids)]` |
| `cheque_return_reason_user_rule` | `cheque.return.reason` | (user-group-scoped) |

## Button visibility

All lifecycle buttons in `cheque.cheque` form view use `groups=` attribute
to restrict visibility:

- **Receive** button: visible to `group_cheque_user`
- **Approve**, **Cash**, **Return**, **Void**, **Reset to Draft** buttons:
  visible only to `group_cheque_manager`
- **Hand Over**, **Cancel** buttons: visible to `group_cheque_user`

## Security considerations

1. **No field-level security (FLS)**: the cheque's `amount` field is visible
   to anyone with read access. If FLS is needed (e.g. hide amounts from
   junior staff), add `groups=` attribute on the field in the form view.
2. **No SQL injection risk**: all search domains use Odoo's ORM, not raw SQL.
3. **No CSRF risk**: no custom HTTP routes; all actions are object methods.
4. **No hardcoded credentials**: no credentials in data XML.
