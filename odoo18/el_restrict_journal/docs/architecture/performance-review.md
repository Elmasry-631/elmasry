# Performance Pre-check — el_restrict_journal

## N+1 Queries

| Pattern | Found | Fixed | Remaining |
|---------|-------|-------|-----------|
| `search()` inside `for record in self:` loop | 0 | 0 | 0 |
| `search_count()` inside loops | 0 | 0 | 0 |
| `browse()` inside loops | 0 | 0 | 0 |
| Filtered on pre-fetched recordsets | 1 (in account.move.create) | n/a (intentional — small recordset) | 0 |

**Verdict:** ✅ PASS — no N+1 queries.

The only `for rec in records:` loop is in `account.move.create()` and `account.payment.create()`, where `records` is the result of `super().create(vals_list)` — at most a few records per call. The check `if rec.journal_id in restricted` is an in-memory comparison between two small recordsets.

## Missing Indexes

| Field | Model | Used in domain? | Has index? | Action |
|-------|-------|------------------|------------|--------|
| `journal_id` | account.move | Yes (record rule) | Yes (auto-indexed by Odoo) | None needed |
| `journal_id` | account.payment | Yes (record rule) | Yes (auto-indexed by Odoo) | None needed |
| `id` | account.journal | Yes (record rule via `user.journal_ids.ids`) | Yes (PK) | None needed |
| `journal_ids` (M2M) | res.users | Yes (record rule via `user.journal_ids.ids`) | Yes (M2M relation table indexes both columns) | None needed |

**Verdict:** ✅ PASS — all fields used in domain filters are indexed.

## Unbounded Queries

| Pattern | Found | Fixed | Remaining |
|---------|-------|-------|-----------|
| `search([])` without limit on potentially large models | 0 | 0 | 0 |

**Verdict:** ✅ PASS — no unbounded queries.

## Computed Field Chains

| Pattern | Found | Fixed | Remaining |
|---------|-------|-------|-----------|
| Compute field depending on another compute field | 0 | 0 | 0 |
| Compute fields with `store=True` triggering recompute | 0 | 0 | 0 |

The only compute field is `account.journal.restricted_user_count`:
- Non-stored (computed on demand)
- Uses `@api.depends_context('id')` — recomputes only when journal ID changes
- Uses a single raw SQL query for ALL journals in `self` (batched)
- No dependencies on other computed fields

**Verdict:** ✅ PASS — no compute chains.

## Dashboard RPC Budget

N/A — this module has no dashboard. The smart button on the journal form makes 0 additional RPC calls (the count is computed in the form view's load via the field declaration).

**Verdict:** ✅ PASS — no dashboard, no RPC budget concern.

## Overall Verdict

✅ **PASS** — no performance issues detected.

The module's runtime overhead is:
- 1 in-memory comparison per `account.move` create/write (when `user.journal_ids` is non-empty)
- 1 in-memory comparison per `account.payment` create/write (same)
- 1 raw SQL query per `account.journal` form load (for the smart button count)

All operations are O(1) or O(log n) at the database level. Negligible performance impact.
