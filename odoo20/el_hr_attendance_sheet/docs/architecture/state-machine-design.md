# State Machine Design — el_hr_attendance_sheet

> State machines for the 3 transactional models.

## 1. hr.attendance.sheet

```
                    ┌────────┐
        create      │ draft  │  ← action_draft() from cancelled
       ────────►    │        │
                    └────┬───┘
                         │ action_compute()
                         ▼
                    ┌──────────┐
                    │ computed │  ← action_compute() (re-compute)
                    │          │
                    └────┬─────┘
                         │ action_approve()
                         ▼
                    ┌──────────┐
                    │ approved │  ← action_approve() from done? NO
                    │          │    (approved is terminal-ish)
                    └────┬─────┘
                         │ action_done() (after payslip created)
                         ▼
                    ┌──────────┐
                    │   done   │  ← terminal
                    │          │
                    └──────────┘

  From draft, computed, approved → action_cancel() → cancelled
  From cancelled → action_draft() → draft

  Transitions table:
  ┌──────────────┬──────────────────┬──────────────────────────────┐
  │ From         │ To               │ Trigger / Validation         │
  ├──────────────┼──────────────────┼──────────────────────────────┤
  │ draft        │ computed         │ action_compute()             │
  │              │                  │  - Validates contract exists │
  │              │                  │  - Validates policy on       │
  │              │                  │    contract                  │
  │              │                  │  - Validates period not      │
  │              │                  │    overlapping another sheet │
  │ computed     │ computed         │ action_compute() (re-run)    │
  │ computed     │ approved         │ action_approve()             │
  │              │                  │  - HR Officer only           │
  │ approved     │ done             │ action_done()                │
  │              │                  │  - Requires payslip_id set   │
  │ draft,       │ cancelled        │ action_cancel()              │
  │ computed,    │                  │                              │
  │ approved     │                  │                              │
  │ cancelled    │ draft            │ action_draft()               │
  └──────────────┴──────────────────┴──────────────────────────────┘

  Selection field definition:
    state = fields.Selection([
        ('draft', 'Draft'),
        ('computed', 'Computed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True, copy=False)
```

## 2. hr.attendance.sheet.batch

```
                    ┌────────┐
        create      │ draft  │
       ────────►    │        │
                    └────┬───┘
                         │ action_generate_sheets()
                         │   (creates one sheet per employee in dept)
                         ▼
                    ┌───────────┐
                    │ confirmed │  ← all child sheets in 'computed' state
                    │           │
                    └────┬──────┘
                         │ action_done()
                         │   (all child sheets must be 'approved' or 'done')
                         ▼
                    ┌──────────┐
                    │   done   │  ← terminal
                    │          │
                    └──────────┘

  From draft, confirmed → action_cancel() → cancelled
  From cancelled → action_draft() → draft

  Selection:
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True, copy=False)
```

## 3. hr.attendance.public.holiday

```
                    ┌────────┐
        create      │ draft  │
       ────────►    │        │
                    └────┬───┘
                         │ action_activate()
                         ▼
                    ┌────────┐
                    │ active │  ← effective; used in overtime calc
                    │        │
                    └────┬───┘
                         │ action_cancel()
                         ▼
                    ┌──────────┐
                    │ cancelled│
                    └────┬─────┘
                         │ action_draft()
                         ▼
                    ┌────────┐
                    │ draft  │
                    └────────┘

  Selection:
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True, copy=False)
```

## State Machine Safety Rules

1. **Validate before transition** — every action_* method checks current state; raises UserError if invalid.
2. **No skip-ahead** — cannot go from draft to done directly.
3. **Cancel allowed only from non-terminal states** — done is terminal (can't cancel a sheet that already generated a payslip).
4. **Reset to draft** only from cancelled — prevents losing computation history.
5. **Tracking** — all transitions logged in chatter via `tracking=True` on the state field.
6. **Copy=False** on state — duplicate records always start in draft.

## Button Visibility Rules (in views)

| Button | Visible When |
|---|---|
| Compute | state == 'draft' OR state == 'computed' |
| Approve | state == 'computed' |
| Done | state == 'approved' |
| Cancel | state in ('draft', 'computed', 'approved') |
| Reset to Draft | state == 'cancelled' |
| Create Payslip | state == 'approved' AND not payslip_id |
| Change Data (on line) | parent.state == 'computed' |
