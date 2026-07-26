# State Machine Design — el_cheque_tracking

## Received cheque lifecycle

```
                ┌─────────┐
                │  draft  │ ← create
                └────┬────┘
                     │ action_receive()
                     │ posts: Dr Cheques Received / Cr Receivable
                     ▼
                ┌──────────┐
        ┌──────│ holding  │──────┐
        │       └──────────┘      │
        │ action_return()         │ action_deposit()
        │ (via wizard)            │ posts: Dr Under Collection / Cr Cheques Received
        │                         │ (validates PDC due date + max re-deposits)
        ▼                         ▼
   ┌──────────┐              ┌───────────┐
   │ returned │◀─────action_return()────│ deposited │
   └────┬─────┘       (via wizard)      └─────┬─────┘
        │                                    │ action_clear()
        │ re-deposit                         │ posts: Dr Bank / Cr Under Collection
        │ (via batch deposit wizard,         ▼
        │  max-attempt validated)       ┌──────────┐
        └──────────────────────────────▶│ cleared  │
                                        └──────────┘
                                             │
                                             │ action_return() (via wizard)
                                             ▼
                                        ┌──────────┐
                                        │ returned │
                                        └──────────┘
```

## Issued cheque lifecycle

```
                ┌─────────┐
                │  draft  │ ← create
                └────┬────┘
                     │ action_approve()
                     │ posts: Dr Payable / Cr Cheques Issued
                     ▼
                ┌──────────┐
                │ approved │
                └────┬─────┘
                     │ action_hand_over()
                     │ (no entry — records physical delivery)
                     ▼
                ┌──────────────┐
        ┌──────│ handed_over  │──────┐
        │       └──────────────┘      │
        │ action_return()             │ action_cash()
        │ (via wizard,                │ posts: Dr Cheques Issued / Cr Bank
        │  reverses issue liability)  ▼
        │                       ┌────────┐
        ▼                       │ cashed │
   ┌──────────┐                  └────────┘
   │ returned │
   └──────────┘

   From draft / approved / handed_over:
                     │ action_void()
                     │ (reverses any posted entries)
                     ▼
                ┌─────────┐
                │  void   │
                └─────────┘

   From draft only:
                     │ action_cancel()
                     ▼
                ┌───────────┐
                │ cancelled │ ──action_reset_to_draft()──▶ draft
                └───────────┘
```

## State → accounting entry map

| Cheque type | From → To | Debit | Credit | Stage tag |
|---|---|---|---|---|
| Received | Draft → Holding | Cheques Received | Receivable (partner) | receipt |
| Received | Holding → Deposited | Under Collection | Cheques Received | deposit |
| Received | Deposited → Cleared | Bank | Under Collection | clearance |
| Received | Deposited/Cleared → Returned | reversal of latest move | reversal of latest move | return |
| Received | Returned + bank charges | Bank Charges (expense) | Bank | return |
| Received | Returned + penalty | Receivable (partner) | Penalty Income | return |
| Issued | Draft → Approved | Payable (partner) | Cheques Issued | issue |
| Issued | Handed Over → Cashed | Cheques Issued | Bank | cash |
| Issued | Handed Over → Returned | reversal of issue move | reversal of issue move | return |
| Issued | Draft/Approved/Handed-Over → Void | reversal of latest move | reversal of latest move | void |
