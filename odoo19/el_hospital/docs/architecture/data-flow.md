# Data Flow — el_hospital

## Main Patient Journey (من استقبال المريض لحد الخروج)

```
1. Reception: Register patient → hospital.patient (from res.partner)
                         │
2. Reception: Book appointment → hospital.appointment (draft)
                         │
3. Doctor:   Confirm appointment → confirmed
                         │
4. Doctor:   See patient → create medical record → hospital.medical.record
             └─ appointment.state = done
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
   prescription    lab.test    radiology.order
   (pharmacy)      (lab)       (radiology)
            │            │            │
            └────────────┼────────────┘
                         │
5. Billing:  Create billing → hospital.invoice.billing
             └─ action_create_invoice → account.move (posted)
                         │
6. (if Inpatient) Admission → hospital.admission → bed occupied
                         │
7. Discharge: action_discharge → bed freed, billing finalized
```

## Inpatient (Admission) Flow

```
Doctor requests admission
  → hospital.admission (draft)
  → select ward + bed (only available beds shown)
  → action_admit → bed.state = occupied
  → ... treatment ...
  → action_discharge → bed.state = available, discharge_date set
  → billing updated (room charges)
```

## Lab/Radiology Flow

```
Doctor requests (from medical record or standalone)
  → hospital.lab.test (requested) / hospital.radiology.order (requested)
  → Lab Tech: action_start → in_progress
  → Lab Tech: enter result + action_complete → completed
  → result visible in medical record
```

## Pharmacy Flow

```
Doctor creates prescription → hospital.prescription (draft)
  → Pharmacist dispenses from stock (hospital.medicament.stock_qty)
  → prescription.action_done
  → (optional) billing line created for pharmacy items
```

## Billing Flow

```
Reception/Billing creates → hospital.invoice.billing (draft)
  → add lines (consultation, lab, radiology, pharmacy, room)
  → action_create_invoice → creates account.move (draft)
  → account.move posted → patient invoiced
  → payment registered → account.move paid → billing.state = paid
```

## Dashboard Data Flow

```
Dashboard (hospital.dashboard) reads:
  - count patients by department
  - count appointments today/week/month
  - count admissions (active)
  - bed occupancy rate
  - revenue (sum of paid billing)
  - lab/radiology pending

Rendered via OWL client action + Chart.js (lazy-loaded).
Data fetched via controller /hospital/dashboard/data (JSON).
```
