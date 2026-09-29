# State Machine Design — el_hospital

## 1. hospital.appointment (المواعيد)

```
                action_confirm        action_done
   draft       ────────────►   confirmed   ────────────►   done
      │                                           ▲
      │                  action_cancel              │
      └────────────────►  cancelled  ◄─────────────┘
```

| State | Label | Color | Permissions |
|-------|-------|-------|-------------|
| draft | Draft | grey | reception, doctor, admin |
| confirmed | Confirmed | blue | doctor, admin |
| done | Done | green | doctor, admin |
| cancelled | Cancelled | red | admin |

## 2. hospital.admission (الإقامة)

```
                action_admit               action_discharge
   draft       ────────────►   admitted   ───────────────►   discharged
      │                                               ▲
      │                  action_cancel                 │
      └────────────────►  cancelled  ◄─────────────────┘
```

Side effects:
- `action_admit`: sets bed.state = 'occupied', bed.admission_id = self
- `action_discharge`: sets bed.state = 'available', bed.admission_id = False

## 3. hospital.lab.test (التحاليل)

```
                action_start               action_complete
   requested   ────────────►  in_progress  ──────────────►  completed
      │                                                ▲
      │              action_cancel                      │
      └────────────►  cancelled  ◄──────────────────────┘
```

## 4. hospital.radiology.order (الأشعة)

Same as lab.test: requested → in_progress → completed / cancelled

## 5. hospital.prescription (الوصفات)

```
   draft   ────────────►   done
```

Simple two-state: draft → done (locked after print).

## 6. hospital.invoice.billing (الفواتير)

```
   draft   ──action_create_invoice──►   invoiced   ──(auto)──►   paid
```

- `draft`: editable
- `invoiced`: account.move created, linked
- `paid`: when linked move is paid (computed)

## 7. hospital.bed (الأسرّة)

```
   available   ──action_set_maintenance──►   maintenance
       ▲                                        │
       └──────────action_set_available──────────┘

   available   ──(admission.admit)──►   occupied   ──(discharge)──► available
```

Bed state is managed by admissions (occupied/available) and manual (maintenance).
