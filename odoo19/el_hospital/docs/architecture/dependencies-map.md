# Dependencies Map — el_hospital

## Module Dependencies (`__manifest__.py` → `depends`)

```python
'depends': ['base', 'mail', 'hr', 'stock', 'account', 'sale_management']
```

| Dependency | Reason |
|-----------|--------|
| `base` | core (res.partner, res.users, sequences) |
| `mail` | chatter, activities, mail templates |
| `hr` | hr.employee for physicians/staff |
| `stock` | stock.quant for medicament inventory |
| `account` | account.move for billing/invoicing |
| `sale_management` | product.template / product.product for medicaments |

## Model Dependencies (internal)

```
hospital.department
  ├─► hospital.physician (head_physician_id)
  ├─► hospital.ward (department_id)
  └─► hospital.patient (department_id)

hospital.physician
  └─► hr.employee, res.partner

hospital.patient
  ├─► res.partner (partner_id)
  ├─► hospital.physician (primary doctor)
  ├─► hospital.patient.allergy (allergy_ids)
  ├─► hospital.patient.disease (chronic_disease_ids)
  ├─► hospital.appointment (smart button)
  └─► hospital.admission (smart button)

hospital.appointment
  ├─► hospital.patient
  ├─► hospital.physician
  └─► hospital.medical.record (created after visit)

hospital.medical.record
  ├─► hospital.patient, hospital.physician, hospital.appointment
  ├─► hospital.prescription
  ├─► hospital.lab.test
  └─► hospital.radiology.order

hospital.prescription
  ├─► hospital.patient, hospital.physician, hospital.medical.record
  └─► hospital.prescription.line ─► hospital.medicament

hospital.ward
  ├─► hospital.department
  └─► hospital.bed

hospital.bed
  ├─► hospital.ward
  └─► hospital.admission (current)

hospital.admission
  ├─► hospital.patient, hospital.physician, hospital.ward, hospital.bed

hospital.lab.test
  └─► hospital.patient, hospital.physician, hospital.medical.record

hospital.radiology.order
  └─► hospital.patient, hospital.physician, hospital.medical.record

hospital.medicament
  └─► product.product, product.template, stock.quant

hospital.invoice.billing
  ├─► hospital.patient, hospital.physician
  ├─► hospital.invoice.billing.line
  └─► account.move
```

## Load Order (models/__init__.py)

Must respect dependencies — parent models first:

```python
from . import hospital_department
from . import hospital_physician
from . import hospital_patient
from . import hospital_appointment
from . import hospital_medical_record
from . import hospital_prescription
from . import hospital_ward
from . import hospital_bed
from . import hospital_admission
from . import hospital_lab_test
from . import hospital_radiology
from . import hospital_medicament
from . import hospital_billing
from . import hospital_dashboard
```
