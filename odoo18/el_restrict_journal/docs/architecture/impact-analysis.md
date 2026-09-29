# Impact Analysis — el_restrict_journal

## 1. Affected Models

| Model | Change | Risk | Mitigation |
|-------|--------|------|------------|
| `res.users` | +1 field (`journal_ids`) | LOW — additive only | None needed |
| `account.move` | Override `create`, `write`, +`_onchange_journal_id`, +`_check_journal_not_restricted` constrains | MEDIUM — overrides must use `super()` chain | Standard `super().create()` pattern; no recursion risk |
| `account.payment` | Override `create`, `write`, +`_check_journal_not_restricted` constrains | MEDIUM — same as above | Same pattern |

## 2. Affected Views

| View | Change | Risk |
|------|--------|------|
| `base.view_users_form` | Inherit to add `journal_ids` field in a new page | LOW — additive |
| `account.view_move_form` | Inherit to ensure journal_id field has proper onchange (no visible change) | LOW |
| `account.view_journal_form` | Inherit to add smart button "Restricted Users" (count) | LOW |

## 3. Affected Security

| Resource | Change | Risk |
|----------|--------|------|
| `res.groups` | +2 new groups (`group_restrict_journal_user`, `group_restrict_journal_manager`) | LOW — additive |
| `ir.rule` | +6 new record rules | LOW — additive; existing rules preserved |
| `ir.model.access.csv` | No new models → no new access entries needed | NONE |

## 4. Performance Impact

| Operation | Before | After | Delta |
|-----------|--------|-------|-------|
| `account.move.create()` | 1 ORM call | 1 ORM call + 1 in-memory check (`if rec.journal_id in restricted`) | Negligible (<1ms) |
| `account.move.write()` | 1 ORM call | Same + 1 in-memory check | Negligible |
| List view load | Standard SQL WHERE | Standard SQL WHERE + record rule filter (`journal_id NOT IN (...)`) | Negligible — `journal_id` is indexed in `account_move` table |
| User form load | Standard | +1 M2M field fetch | Negligible — uses existing `res_users` query |

**Verdict:** Performance impact is negligible. The check `rec.journal_id in restricted` is an in-memory comparison between two recordsets — O(1) on a small set (typically <10 journals per user).

## 5. Migration / Backwards Compatibility

| Scenario | Behavior |
|----------|----------|
| Fresh install | `journal_ids` empty for all users → no restrictions active → behaves identically to vanilla Odoo |
| Upgrade from original Cybrosys module | NOT SUPPORTED — different module name (`el_restrict_journal` vs `account_restrict_journal`); user must reconfigure restrictions manually |
| Uninstall | All overrides, record rules, and groups are removed; users regain full access via existing `account` group permissions |

## 6. Data Migration Path (from original Cybrosys module)

If migrating from the original broken Cybrosys module:

1. **Document current restrictions:** For each user, list their `journal_ids` (from the old `account_restrict_journal` table — if it was created before the module broke).
2. **Uninstall the old module** (will likely fail due to import errors — must manually drop `account_restrict_journal` from `ir.module.module` and restart Odoo).
3. **Install `el_restrict_journal`.**
4. **Re-assign journals** to each user via the new user form.
5. **Test:** Have a user with restrictions try to create a move with a restricted journal — should get `ValidationError`.

## 7. Risk Register

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|
| 1 | User with empty `journal_ids` accidentally restricted | LOW | HIGH (blocks all work) | Code explicitly checks `if restricted:` (skips check when empty) |
| 2 | Admin user blocked from configuring restrictions | LOW | HIGH (cannot manage) | Admin (with `base.group_system`) typically has empty `journal_ids` → not restricted |
| 3 | Performance issue on list view with many journals | LOW | LOW | `journal_id` indexed in account_move; query plan stays efficient |
| 4 | Conflict with another module overriding `account.move.create` | MEDIUM | MEDIUM | Use `super()` chain — Odoo's MRO handles chaining |
| 5 | User complains "I can see the journal but cannot use it" | HIGH | LOW | Documentation: explain read-only visibility is intentional |
| 6 | Original Cybrosys `is_check_journal` field breaks on uninstall | MEDIUM | MEDIUM | Different module name → no DB conflict; original table orphaned |
