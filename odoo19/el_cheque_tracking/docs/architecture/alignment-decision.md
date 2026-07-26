# Alignment Decision — el_cheque_tracking

## Key design decisions

### 1. Model namespace: `cheque.*` (not `el_cheque_tracking.*`)

**Decision:** Use `cheque.cheque`, `cheque.deposit`, `cheque.return`,
`cheque.return.reason` instead of `el_cheque_tracking.cheque`, etc.

**Rationale:**
- The `cheque.*` namespace is shorter and more readable in domain expressions
  (`[('cheque_id.cheque_type', '=', 'received')]`).
- It matches the convention used by other accounting-domain modules
  (`account.*`, `stock.*`, `hr.*`).
- The module technical name `el_cheque_tracking` already provides the
  author + domain prefix; duplicating it in every model name would be
  redundant.

**Trade-off:** The skill's MD014 validator warns about this, but the
warning is a style preference, not a correctness issue. The original
`cheque_tracking` module (from the dump) used the same convention.

### 2. `models.Constraint` (not `_sql_constraints`)

**Decision:** Use the Odoo 19 `models.Constraint` class for SQL constraints.

**Rationale:**
- `_sql_constraints` is deprecated in Odoo 19.
- `models.Constraint` provides better introspection and is the canonical
  O19 pattern (see `references/cookbook/05-verbatim-core-patterns.md`).

### 3. `res.groups.privilege` (not `ir.module.category`)

**Decision:** Use the Odoo 19 `res.groups.privilege` pattern for security
groups.

**Rationale:**
- `ir.module.category` + `category_id` is deprecated in Odoo 19.
- `res.groups.privilege` + `privilege_id` is the canonical O19 pattern
  (see `examples/ie_sale_workflow/security/groups.xml`).
- The privilege record carries `name` + `sequence` directly; no separate
  category record is needed.

### 4. `read_group` for partner cheque stats (not `search()` in a loop)

**Decision:** Use `read_group` to compute partner cheque counters + totals.

**Rationale:**
- `search()` in a `for partner in self:` loop is an N+1 anti-pattern.
- `read_group` computes all partner stats in a single SQL query.
- This is documented as the canonical pattern in
  `references/clean-code-rules.md` CC-901.

### 5. `_apply_return` as a method on `cheque.cheque` (not on the wizard)

**Decision:** The return wizard delegates to `cheque.cheque._apply_return()`.

**Rationale:**
- The accounting work (reversal + charges + penalty) belongs on the cheque
  model so it appears on the cheque's audit trail (`move_ids`).
- The wizard is only a UI layer; it should not contain business logic.
- This allows programmatic returns (e.g. from a server action) without
  going through the wizard.

### 6. Reports use `web.external_layout` (not `web.internal_layout`)

**Decision:** All 3 QWeb reports use `web.external_layout`.

**Rationale:**
- These are client-facing documents (cheque print, deposit slip, register).
- `web.internal_layout` is for internal documents (e.g. picking lists).
- The skill's R020 validator warns about this, but the warning is a false
  positive for client-facing reports.

### 7. Tests use `TransactionCase` with `@tagged("post_install", "-at_install")`

**Decision:** Use `TransactionCase` (not `HttpCase`) with post-install tagging.

**Rationale:**
- `TransactionCase` is appropriate for model-level tests that don't need
  a running HTTP server.
- `post_install` + `-at_install` ensures the test runs after the module
  is fully installed (so demo data is available).

### 8. Currency conversion via `_to_company_currency` helper

**Decision:** Centralize currency conversion in a `_to_company_currency`
helper method on `cheque.cheque`.

**Rationale:**
- Each accounting entry (receipt, deposit, clearance, return, issue, cash)
  needs to convert the cheque amount to company currency.
- The helper respects a manual `exchange_rate` if set, otherwise uses the
  automatic currency rate for the cheque date.
- Centralizing avoids duplication and makes future changes (e.g. different
  rate sources) easier.
