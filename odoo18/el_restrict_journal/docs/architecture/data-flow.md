# Data Flow — el_restrict_journal

## 1. Configuration Flow

```mermaid
sequenceDiagram
    actor Admin as Chief Accountant
    participant U as res.users form
    participant DB as PostgreSQL

    Admin->>U: Opens user record
    Admin->>U: Adds journals to journal_ids
    U->>DB: write(journal_ids=[...])
    DB-->>U: Saved
    U-->>Admin: Confirmation
```

## 2. account.move Create Flow

```mermaid
sequenceDiagram
    actor User as Accountant
    participant UI as account.move form
    participant AM as account.move (overridden)
    participant DB as PostgreSQL
    participant RR as Record Rules

    User->>UI: Selects journal + clicks Save
    UI->>AM: create(vals)
    AM->>DB: super().create(vals) → record
    AM->>AM: Check journal_id in user.journal_ids
    alt Restricted
        AM-->>UI: ValidationError
        UI-->>User: Error popup
    else Not restricted
        AM->>RR: Record rule check (write/create)
        RR-->>AM: Pass
        AM-->>UI: Success
        UI-->>User: Record saved
    end
```

## 3. account.move Write Flow

```mermaid
sequenceDiagram
    actor User as Accountant
    participant UI as account.move form
    participant AM as account.move (overridden)
    participant DB as PostgreSQL

    User->>UI: Changes journal_id + clicks Save
    UI->>AM: write({journal_id: X})
    AM->>DB: super().write(vals)
    AM->>AM: Check rec.journal_id in user.journal_ids
    alt Restricted
        AM-->>UI: ValidationError
    else Not restricted
        AM-->>UI: Success
    end
```

## 4. Onchange UX Flow (immediate feedback)

```mermaid
sequenceDiagram
    actor User as Accountant
    participant UI as account.move form
    participant AM as account.move (overridden)

    User->>UI: Selects restricted journal from dropdown
    UI->>AM: onchange_journal_id
    AM->>AM: Check journal_id in user.journal_ids
    alt Restricted
        AM->>UI: warning + journal_id cleared
        UI-->>User: "Journal X is restricted" popup
    else Not restricted
        AM-->>UI: No-op
    end
```

## 5. List View Read Flow (record rule enforcement)

```mermaid
sequenceDiagram
    actor User as Accountant
    participant UI as account.move list
    participant DB as PostgreSQL
    participant RR as Record Rules

    User->>UI: Opens list view
    UI->>DB: SELECT ... FROM account_move WHERE ...
    DB->>RR: Apply record rules
    RR->>RR: Filter: journal_id NOT IN user.journal_ids (full access)<br/>OR journal_id IN user.journal_ids (read-only)
    RR-->>DB: Combined WHERE clause
    DB-->>UI: Filtered result set
    UI-->>User: Shows list (restricted journals visible but read-only)
```

## 6. Critical Path: Defense in Depth

The restriction is enforced at **3 layers**, in order:

| Layer | Where | What | Bypassable? |
|-------|-------|------|-------------|
| 1 | UI Onchange | Clears journal_id + warning popup | Yes — user can disable JS |
| 2 | Record Rules | Filters list views, blocks write/create/unlink at ORM level | Hard (requires admin SQL) |
| 3 | Python Override + Constrains | `ValidationError` in `create`/`write`/constrains | No (without uninstall) |

A user who tries to bypass layer 1 (UI) will hit layer 2 (record rule blocks the operation at the ORM level). Even if they bypass layer 2 (via raw SQL or admin tools), layer 3 (Python constrains) catches the violation on the next `flush()` of the record.
