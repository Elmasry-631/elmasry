# API Reference — el_restrict_journal

## 1. Python API

### `res.users.journal_ids`

- **Type:** `Many2many → account.journal`
- **Access:** Read-only for non-managers; RW for `group_restrict_journal_manager`; admin always
- **Purpose:** Lists journals this user is restricted from using

```python
# Check if a user is restricted from a journal
user = self.env.user
journal = self.env['account.journal'].browse(42)
if journal in user.journal_ids:
    print("User is restricted from this journal")
```

### `account.move.create(vals_list)` (overridden)

- **Behavior:** After `super().create()`, checks each new record's `journal_id`. If the journal is in `user.journal_ids`, raises `ValidationError`.
- **Bypass:** Set `user.journal_ids = False` (clear restrictions) before the create call.

### `account.move.write(vals)` (overridden)

- **Behavior:** After `super().write()`, if `vals` contains `journal_id`, checks each record's new journal. Raises `ValidationError` if restricted.

### `account.move._onchange_journal_id()` (NEW)

- **Triggered:** When user changes `journal_id` in the form view
- **Behavior:** If the new journal is restricted, clears `journal_id` and returns a warning dict
- **Returns:** `{'warning': {'title': ..., 'message': ...}}` or `None`

### `account.move._check_journal_not_restricted()` (NEW constraint)

- **Triggered:** On any create/write that touches `journal_id`
- **Behavior:** Raises `ValidationError` if `rec.journal_id in user.journal_ids`

### Same methods exist on `account.payment` (except `_onchange_journal_id`)

### `account.journal.restricted_user_count` (computed)

- **Type:** `Integer`
- **Computed:** `_compute_restricted_user_count()` — single SQL query for all journals in `self`
- **Purpose:** Powers future smart button (currently unused in views)

## 2. XML-RPC API

No new XML-RPC endpoints. All restriction enforcement is automatic via the ORM.

To configure restrictions via XML-RPC:

```python
import xmlrpc.client

url = "http://localhost:8069"
db = "your_db"
uid = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common").authenticate(
    db, "admin", "password", {}
)
models = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/object")

# Restrict user 7 from journal 42
models.execute_kw(db, uid, "password", "res.users", "write", [
    [7],
    {"journal_ids": [(6, 0, [42])]},
])
```

## 3. Caveats

- **Admin bypass:** Users with `is_admin = True` are NEVER restricted (their `journal_ids` is typically empty)
- **Empty list = unrestricted:** A user with `journal_ids = False` has full access
- **No bulk bypass:** There is no `sudo()` shortcut in user code — restrictions apply to all non-admin users
- **Cron jobs:** Cron jobs run as `uid = 1` (admin), so they are never restricted
