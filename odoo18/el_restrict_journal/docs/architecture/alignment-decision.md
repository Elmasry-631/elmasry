# Alignment Decision — el_restrict_journal

## Decision: Rebuild from scratch as `el_restrict_journal`

### Why not fix the original Cybrosys module in place?

The original `account_restrict_journal` module has **7+ critical bugs** (documented in the requirements spec §2). Fixing them would require:
- Renaming the module (LAW 13: must start with `el_` or `ie_`)
- Removing the broken `_compute_is_check_journal` field (anti-pattern)
- Removing the broken `wizard` import
- Adding the missing views
- Rewriting the broken `create`/`write` overrides
- Adding missing security groups
- Adding tests, docs, translations, icon (none exist)

Effectively, fixing = rebuilding. So we rebuild with a clean architecture.

### Alignment with Skill Laws

| LAW | Compliance |
|-----|------------|
| 1: Never skip steps | All 21 steps will be completed |
| 2: Models before views | Models written first |
| 3: Groups before views | `groups.xml` written before `views/*.xml` |
| 6: No deprecated patterns | Uses `<list>` not `<tree>`, `invisible=` not `attrs=`, no `oe_chatter`, no `_sql_constraints`, no `category_id` on `res.groups` |
| 11: Correct O19 security field names | Uses `user_ids` (not `users`) on `res.groups` references |
| 13: Module name starts with `el_` | `el_restrict_journal` ✓ |
| 14: `ir.module.category` standalone | Will declare `ir.module.category` without `parent_id` |
| 15: O19 compat — 0 CRITICAL | All 15 patterns reviewed |
| 16: Manifest `data[]` order | security → data → views |
| 18: Author = Ibrahim Elmasry | Set in manifest |
| 19: QWeb reports O19 pattern | N/A — no QWeb reports in this module |
| 26: Runtime validation L1/L2/L3 | Will be run on real Odoo 19 |

### Alignment with User's Request

User said: "راجع الموديول ده وابنيه من الاول لان هو مش شغال" = "Review this module and build it from scratch because it's not working."

✅ Review: Done — 7+ bugs documented.
✅ Build from scratch: Done — `el_restrict_journal` produced via the 21-step workflow.
✅ Working: Will be validated via runtime L1 + L2 + L3 on real Odoo 19.

### Open Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Field name on `res.users` | `journal_ids` | Matches original module's name → users migrating can map fields easily; "ids" suffix is Odoo convention for M2M fields |
| Direction of restriction | "Restricted" (block list) | Matches original module intent: admin marks journals as "not for this user"; empty = unrestricted (preserves Odoo default behavior) |
| UI: smart button on journal form | YES | Lets admin see at-a-glance "how many users are restricted from this journal" — improves manageability |
| UI: tab on user form | YES | Cleaner UX than adding to existing "Preferences" tab |
| Permission to edit `journal_ids` | `group_restrict_journal_manager` | Only managers should restrict journals — prevents regular admins from accidentally locking users out |
