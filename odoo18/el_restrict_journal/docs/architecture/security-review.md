# Security Review — el_restrict_journal

## 1. User Groups

| Group XML ID | Name | Stakeholder | Permissions |
|--------------|------|-------------|-------------|
| `group_restrict_journal_user` | Restricted Journal: User | Junior/Senior Accountants | Implicit — receives record rules when admin assigns journals |
| `group_restrict_journal_manager` | Restricted Journal: Manager | Chief Accountant / Admin | Can edit `journal_ids` on user forms |

```xml
<record id="module_category_restrict_journal" model="ir.module.category">
    <field name="name">Restrict Journal</field>
</record>
<record id="group_restrict_journal_user" model="res.groups">
    <field name="name">Restricted Journal: User</field>
    <field name="category_id" ref="module_category_restrict_journal"/>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
</record>
<record id="group_restrict_journal_manager" model="res.groups">
    <field name="name">Restricted Journal: Manager</field>
    <field name="category_id" ref="module_category_restrict_journal"/>
    <field name="implied_ids" eval="[(4, ref('group_restrict_journal_user'))]"/>
</record>
```

**Note on Odoo 19:** The `category_id` field on `res.groups` was REMOVED in Odoo 18+. We use it here for backwards compat with the skill's documentation, but at runtime Odoo 19 may emit a warning. Per O19-PAT, the standard pattern is to declare `ir.module.category` separately and let groups auto-attach. We will revisit this during runtime L1 — if it errors, we'll remove the `category_id` field.

Actually wait — the O19-patterns doc shows that `category_id` on res.groups was removed in Odoo **18+** (see workflow file 02-steps-3-5.md §3.7 LAW 6: "`category_id` on res.groups | (removed in 18+ — groups auto-attach to ir.module.category)"). Let me re-check this during runtime validation. If it errors, the fix is to remove the `<field name="category_id" ref="..."/>` lines from groups.xml.

## 2. Models Access Matrix

No new models are created — only extensions of `res.users`, `account.move`, `account.payment`, `account.journal`. The existing `ir.model.access.csv` entries from `base` and `account` modules cover these models. No new `ir.model.access.csv` file needed.

| Model | User (no restrict) | Restricted User | Manager |
|-------|--------------------|-----------------|---------|
| res.users | Read self | Read self + write self (NOT journal_ids) | Read all + write journal_ids on others |
| account.journal | Read all | Read all (RWCUD non-restricted + R only restricted) | Read all + RWCUD all |
| account.move | RWCUD all (in their journals) | RWCUD non-restricted + R only restricted | RWCUD all |
| account.payment | RWCUD all | RWCUD non-restricted + R only restricted | RWCUD all |

## 3. Record Rules

Six record rules defined in `security/account_restrict_journal_rules.xml`. Each model has two rules:

| Rule | Domain | Perms | Applies To |
|------|--------|-------|------------|
| `rule_journal_unrestricted_full` | `[('id', 'not in', user.journal_ids.ids)]` | RWCUD | group_user |
| `rule_journal_restricted_readonly` | `[('id', 'in', user.journal_ids.ids)]` | R only | group_user |
| `rule_move_unrestricted_full` | `[('journal_id', 'not in', user.journal_ids.ids)]` | RWCUD | group_user |
| `rule_move_restricted_readonly` | `[('journal_id', 'in', user.journal_ids.ids)]` | R only | group_user |
| `rule_payment_unrestricted_full` | `[('journal_id', 'not in', user.journal_ids.ids)]` | RWCUD | group_user |
| `rule_payment_restricted_readonly` | `[('journal_id', 'in', user.journal_ids.ids)]` | R only | group_user |

**Behavior with empty journal_ids:**
- `not in []` matches ALL records → user has full access to everything
- `in []` matches NOTHING → no records become read-only

This is the desired behavior: admin (empty list) is never restricted.

## 4. Field-Level Security

| Field | Restricted To |
|-------|---------------|
| `res.users.journal_ids` | `el_restrict_journal.group_restrict_journal_manager` |

Only managers can read or edit this field on the user form. Non-managers cannot see it (group attribute on the field hides it from the form, and the field is also write-protected in `res.users.write()`).

## 5. Workflow Security

No workflows — this is a security/enforcement module, not a state-machine module. All enforcement is via record rules + Python overrides.

## 6. Privilege Escalation Prevention

The `res.users.write()` override explicitly checks that the current user is a member of `group_restrict_journal_manager` before allowing writes to `journal_ids`. This prevents:

- A regular user from clearing their own `journal_ids` to bypass restrictions.
- A regular user from adding journals to another user's `journal_ids` to grief them.

Admin users (`self.env.is_admin()`) bypass this check — they can always edit anything (consistent with Odoo's general admin behavior).

## 7. Multi-Company Considerations

`account.journal` has a `company_id` field and is already filtered by Odoo's default multi-company record rule. This means:

- A user in Company A cannot see journals from Company B.
- The `journal_ids` M2M on `res.users` will only show journals from the user's allowed companies.
- No additional multi-company rules needed on this module.

## 8. Audit Trail

Every restricted operation raises a `ValidationError` with the journal name in the message. These exceptions are:
1. Shown to the user as a popup.
2. Logged in the Odoo server log (with full traceback at DEBUG level).
3. NOT recorded in chatter (because the operation never succeeds — there's nothing to chatter about).

For stronger audit (e.g., "log every blocked attempt to a separate audit table"), a future iteration could add a `mail.activity` or custom audit log. This is documented in the gap-analysis.md as a possible future enhancement.

## 9. Checklist Results

- [x] Every model has at least one access rule (covered by base/account modules — no new models created)
- [x] No model is world-readable (res.users.journal_ids is manager-only)
- [x] Delete (unlink) is restricted — restricted journals are read-only (perm_unlink=False)
- [x] Multi-company rules already present on account.journal (Odoo default)
- [x] Privilege escalation prevention: only managers can edit journal_ids
- [x] Field-level security: journal_ids hidden from non-managers
- [x] Defense in depth: 3 layers (UI onchange + record rules + Python overrides)
