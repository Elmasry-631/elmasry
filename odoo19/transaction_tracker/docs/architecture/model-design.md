# Transaction Tracker — Architecture Documentation

## Model Design

### transaction.log

| Field | Type | Description |
|-------|------|-------------|
| name | Char | Auto-generated sequence (TXN/000001) |
| user_id | Many2one(res.users) | User who performed the operation |
| model_name | Char | Technical model name (e.g. sale.order) |
| res_id | Integer | Database ID of affected record |
| record_display_name | Char | Display name of affected record |
| operation | Selection | create / write / unlink / read |
| module_name | Char | Addon that owns the model |
| old_values | Text | JSON snapshot before change |
| new_values | Text | JSON snapshot after change |
| changed_fields | Char | Comma-separated list of changed fields |
| ip_address | Char | Client IP address |
| company_id | Many2one(res.company) | Company |
| is_suspicious | Boolean | Flagged as suspicious (bulk ops) |
| note | Text | Additional notes |

### transaction.tracker.config

| Field | Type | Description |
|-------|------|-------------|
| model_id | Many2one(ir.model) | Model to configure |
| model_name | Char | Related model technical name |
| track_create | Boolean | Track create operations |
| track_write | Boolean | Track write operations |
| track_unlink | Boolean | Track delete operations |
| track_read | Boolean | Track read operations (default: False) |
| active | Boolean | Active flag |

## Data Flow

```
User Action (Create/Write/Unlink)
        │
        ▼
Base.create() / write() / unlink()  ←── Hook intercepts
        │
        ▼
_should_track() check
        │
        ├── SKIP (excluded model / context flag / no config)
        │
        └── PROCEED
                │
                ▼
        _track_create/write/unlink()
                │
                ▼
        Snapshot old/new values
                │
                ▼
        transaction.log._log_operation()
                │
                ▼
        Create log record (sudo + skip_transaction_tracking)
                │
                ▼
        Log stored (immutable)
```

## Security Matrix

| Group | transaction.log | transaction.tracker.config |
|-------|----------------|--------------------------|
| Tracker Manager | Read all | Read, Write, Create |
| Tracker User | Read own only | No access |

## State Machine

This module has no state machine. Log records are immutable — no state transitions.
