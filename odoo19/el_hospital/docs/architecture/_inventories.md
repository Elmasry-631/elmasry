# Architecture Inventories — el_hospital

## 1. Model Inventory

### 1.1 `hospital.department` (أقسام المستشفى)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | required |
| code | Char | unique |
| head_physician_id | Many2one(hospital.physician) | |
| bed_capacity | Integer | |
| notes | Text | |

**Methods:** none
**States:** none (master data)

---

### 1.2 `hospital.physician` (الأطباء)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | related to partner |
| partner_id | Many2one(res.partner) | required |
| employee_id | Many2one(hr.employee) | optional link to HR |
| user_id | Many2one(res.users) | the doctor's login |
| specialization | Char | e.g. Cardiology |
| department_id | Many2one(hospital.department) | |
| medical_license | Char | required, unique |
| phone | Char | related from partner |
| email | Char | related from partner |
| image_1920 | Image | related from partner |
| active | Boolean | |

**Methods:** `_compute_name`, `onchange_partner_id`

---

### 1.3 `hospital.patient` (المرضى)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | computed from partner |
| ref | Char | sequential (sequence) = patient code |
| partner_id | Many2one(res.partner) | required |
| birth_date | Date | |
| age | Integer | computed |
| gender | Selection | male/female/other |
| blood_type | Selection | A/B/AB/O + Rh |
| phone | Char | related |
| email | Char | related |
| address | Char | related |
| physician_id | Many2one(hospital.physician) | primary doctor |
| department_id | Many2one(hospital.department) | |
| allergy_ids | One2many(hospital.patient.allergy) | |
| chronic_disease_ids | One2many(hospital.patient.disease) | |
| appointment_count | Integer | computed |
| admission_count | Integer | computed |
| active | Boolean | |

**Methods:** `_compute_name`, `_compute_age`, `_compute_appointment_count`,
`_compute_admission_count`, `action_open_appointments`, `action_open_admissions`

**Constraints:** unique partner_id (one patient record per partner)

---

### 1.4 `hospital.patient.allergy` (حساسية المريض)
| Field | Type | Notes |
|-------|------|-------|
| patient_id | Many2one(hospital.patient) | |
| name | Char | required (allergy name) |
| severity | Selection | mild/moderate/severe |
| notes | Text | |

### 1.5 `hospital.patient.disease` (الأمراض المزمنة)
| Field | Type | Notes |
|-------|------|-------|
| patient_id | Many2one(hospital.patient) | |
| name | Char | required |
| diagnosed_date | Date | |
| notes | Text | |

---

### 1.6 `hospital.appointment` (المواعيد)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | sequence AP/00001 |
| patient_id | Many2one(hospital.patient) | required |
| physician_id | Many2one(hospital.physician) | required |
| department_id | Many2one(hospital.department) | |
| appointment_date | Datetime | required |
| duration | Float | hours |
| state | Selection | draft/confirmed/done/cancelled |
| type | Selection | consultation/follow_up/emergency |
| notes | Text | |
| medical_record_id | Many2one(hospital.medical.record) | created after visit |

**Methods:** `action_confirm`, `action_done`, `action_cancel`,
`action_draft`, `_compute_is_today`

**States:** draft → confirmed → done / cancelled

---

### 1.7 `hospital.medical.record` (EMR — السجل الطبي)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | sequence MR/00001 |
| patient_id | Many2one(hospital.patient) | required |
| physician_id | Many2one(hospital.physician) | required |
| appointment_id | Many2one(hospital.appointment) | |
| record_date | Datetime | default now |
| chief_complaint | Text | الشكوى الرئيسية |
| diagnosis | Text | |
| treatment | Text | |
| notes | Text | |
| prescription_ids | One2many(hospital.prescription) | |
| lab_test_ids | One2many(hospital.lab.test) | |
| radiology_order_ids | One2many(hospital.radiology.order) | |

**Methods:** `action_create_prescription`

---

### 1.8 `hospital.prescription` (الوصفات)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | sequence RX/00001 |
| patient_id | Many2one(hospital.patient) | required |
| physician_id | Many2one(hospital.physician) | required |
| medical_record_id | Many2one(hospital.medical.record) | |
| prescription_date | Datetime | default now |
| line_ids | One2many(hospital.prescription.line) | |
| state | Selection | draft/done |
| notes | Text | |

### 1.9 `hospital.prescription.line` (أدوية الوصفة)
| Field | Type | Notes |
|-------|------|-------|
| prescription_id | Many2one(hospital.prescription) | |
| medicament_id | Many2one(hospital.medicament) | required |
| dosage | Char | e.g. "500mg" |
| frequency | Char | e.g. "2x/day" |
| duration | Char | e.g. "7 days" |
| quantity | Float | qty to dispense |
| instructions | Text | |

---

### 1.10 `hospital.ward` (الغرف/الأجنحة)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | required |
| code | Char | unique |
| department_id | Many2one(hospital.department) | |
| ward_type | Selection | general/private/icu/maternity/pediatric |
| floor | Char | |
| bed_capacity | Integer | default 1 |
| bed_count | Integer | computed (beds in this ward) |
| occupied_count | Integer | computed |
| available_count | Integer | computed |
| notes | Text | |

---

### 1.11 `hospital.bed` (الأسرّة)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | computed (ward + number) |
| ward_id | Many2one(hospital.ward) | required |
| bed_number | Char | required |
| state | Selection | available/occupied/maintenance |
| admission_id | Many2one(hospital.admission) | current admission |
| patient_id | Many2one(hospital.patient) | related from admission |

**Methods:** `_compute_name`, `action_set_maintenance`, `action_set_available`

---

### 1.12 `hospital.admission` (دخول/خروج المريض)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | sequence ADM/00001 |
| patient_id | Many2one(hospital.patient) | required |
| physician_id | Many2one(hospital.physician) | required |
| department_id | Many2one(hospital.department) | |
| ward_id | Many2one(hospital.ward) | |
| bed_id | Many2one(hospital.bed) | |
| admission_date | Datetime | default now |
| discharge_date | Datetime | |
| state | Selection | draft/admitted/discharged/cancelled |
| reason | Text | سبب الدخول |
| discharge_notes | Text | |
| days_count | Integer | computed |

**Methods:** `action_admit` (reserves bed → occupied),
`action_discharge` (frees bed → available), `_compute_days_count`

**States:** draft → admitted → discharged / cancelled

---

### 1.13 `hospital.lab.test` (التحاليل المخبرية)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | sequence LAB/00001 |
| patient_id | Many2one(hospital.patient) | required |
| physician_id | Many2one(hospital.physician) | requested by |
| medical_record_id | Many2one(hospital.medical.record) | |
| test_type | Selection | blood/urine/stool/tissue/other |
| test_name | Char | required |
| request_date | Datetime | default now |
| result_date | Datetime | |
| state | Selection | requested/in_progress/completed/cancelled |
| result | Text | |
| notes | Text | |

**States:** requested → in_progress → completed / cancelled

---

### 1.14 `hospital.radiology.order` (الأشعة)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | sequence RAD/00001 |
| patient_id | Many2one(hospital.patient) | required |
| physician_id | Many2one(hospital.physician) | requested by |
| medical_record_id | Many2one(hospital.medical.record) | |
| modality | Selection | xray/ct/mri/ultrasound/mammography |
| study_name | Char | required |
| request_date | Datetime | default now |
| result_date | Datetime | |
| state | Selection | requested/in_progress/completed/cancelled |
| result | Text | |
| image_ids | Many2many(ir.attachment) | attached images |
| notes | Text | |

---

### 1.15 `hospital.medicament` (الأدوية)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | |
| product_id | Many2one(product.product) | required, unique |
| product_tmpl_id | Many2one(product.template) | related |
| generic_name | Char | |
| form | Selection | tablet/capsule/syrup/injection/inhaler/other |
| strength | Char | e.g. "500mg" |
| is_prescription_required | Boolean | default True |
| stock_qty | Float | computed from stock.quant |
| active | Boolean | |

**Methods:** `_compute_stock_qty`

---

### 1.16 `hospital.invoice.billing` (الفواتير الطبية)
| Field | Type | Notes |
|-------|------|-------|
| name | Char | sequence BILL/00001 |
| patient_id | Many2one(hospital.patient) | required |
| partner_id | Many2one(res.partner) | related from patient |
| physician_id | Many2one(hospital.physician) | |
| move_id | Many2one(account.move) | linked invoice |
| billing_date | Date | default today |
| line_ids | One2many(hospital.invoice.billing.line) | |
| amount_total | Monetary | computed |
| state | Selection | draft/invoiced/paid |
| currency_id | Many2one(res.currency) | default company |

### 1.17 `hospital.invoice.billing.line`
| Field | Type | Notes |
|-------|------|-------|
| billing_id | Many2one(hospital.invoice.billing) | |
| name | Char | description |
| service_type | Selection | consultation/lab/radiology/pharmacy/room/other |
| quantity | Float | default 1 |
| price_unit | Monetary | |
| price_subtotal | Monetary | computed |

**Methods:** billing `action_create_invoice` (creates account.move)

---

## 2. View Inventory

| View ID | Type | Model | Fields Used | Notes |
|---------|------|-------|-------------|-------|
| view_hospital_patient_form | form | hospital.patient | all + notebook (allergies, diseases) | smart buttons |
| view_hospital_patient_list | list | hospital.patient | name, ref, gender, age, physician | |
| view_hospital_patient_search | search | hospital.patient | name, ref, physician, gender | filters + group by |
| view_hospital_physician_form | form | hospital.physician | all | |
| view_hospital_physician_list | list | hospital.physician | name, specialization, department | |
| view_hospital_physician_kanban | kanban | hospital.physician | name, image, specialization | |
| view_hospital_appointment_form | form | hospital.appointment | all + state buttons | statusbar |
| view_hospital_appointment_list | list | hospital.appointment | name, patient, physician, date, state | |
| view_hospital_appointment_calendar | calendar | hospital.appointment | date, patient, physician | color=physician |
| view_hospital_medical_record_form | form | hospital.medical.record | all + notebook (rx, lab, radio) | |
| view_hospital_medical_record_list | list | hospital.medical.record | name, patient, physician, date | |
| view_hospital_prescription_form | form | hospital.prescription | all + lines | |
| view_hospital_prescription_list | list | hospital.prescription | name, patient, physician, date | |
| view_hospital_department_form | form | hospital.department | all | |
| view_hospital_department_list | list | hospital.department | name, code, head | |
| view_hospital_ward_form | form | hospital.ward | all + bed stats | |
| view_hospital_ward_list | list | hospital.ward | name, code, dept, capacity, available | |
| view_hospital_bed_form | form | hospital.bed | all + state badge | |
| view_hospital_bed_list | list | hospital.bed | name, ward, state, patient | |
| view_hospital_admission_form | form | hospital.admission | all + state buttons | statusbar |
| view_hospital_admission_list | list | hospital.admission | name, patient, ward, bed, dates, state | |
| view_hospital_lab_test_form | form | hospital.lab.test | all + state buttons | |
| view_hospital_lab_test_list | list | hospital.lab.test | name, patient, test_name, state | |
| view_hospital_radiology_form | form | hospital.radiology.order | all + attachments | |
| view_hospital_radiology_list | list | hospital.radiology.order | name, patient, modality, state | |
| view_hospital_medicament_form | form | hospital.medicament | all | |
| view_hospital_medicament_list | list | hospital.medicament | name, generic, form, stock | |
| view_hospital_billing_form | form | hospital.invoice.billing | all + lines + invoice button | |
| view_hospital_billing_list | list | hospital.invoice.billing | name, patient, amount, state | |
| view_hospital_dashboard | form | hospital.dashboard | KPIs + chart | OWL/JS |

---

## 3. Action Inventory

| Action ID | Name | res_model | view_mode |
|-----------|------|-----------|-----------|
| action_hospital_patient | Patients | hospital.patient | list,form,kanban |
| action_hospital_physician | Physicians | hospital.physician | kanban,list,form |
| action_hospital_appointment | Appointments | hospital.appointment | calendar,list,form |
| action_hospital_appointment_today | Today's Appointments | hospital.appointment | list,form (domain today) |
| action_hospital_medical_record | Medical Records | hospital.medical.record | list,form |
| action_hospital_prescription | Prescriptions | hospital.prescription | list,form |
| action_hospital_department | Departments | hospital.department | list,form |
| action_hospital_ward | Wards | hospital.ward | list,form |
| action_hospital_bed | Beds | hospital.bed | list,form |
| action_hospital_admission | Admissions | hospital.admission | list,form |
| action_hospital_admission_active | Active Admissions | hospital.admission | list,form (domain admitted) |
| action_hospital_lab_test | Lab Tests | hospital.lab.test | list,form |
| action_hospital_radiology | Radiology Orders | hospital.radiology.order | list,form |
| action_hospital_medicament | Medicaments | hospital.medicament | list,form |
| action_hospital_billing | Billings | hospital.invoice.billing | list,form |
| action_hospital_dashboard | Dashboard | hospital.dashboard | form |

---

## 4. Button → Method Map

| Button (xml id) | Model | Method | Notes |
|-----------------|-------|--------|-------|
| appointment.action_confirm | hospital.appointment | `action_confirm` | draft→confirmed |
| appointment.action_done | hospital.appointment | `action_done` | confirmed→done |
| appointment.action_cancel | hospital.appointment | `action_cancel` | →cancelled |
| admission.action_admit | hospital.admission | `action_admit` | draft→admitted, reserve bed |
| admission.action_discharge | hospital.admission | `action_discharge` | admitted→discharged, free bed |
| admission.action_cancel | hospital.admission | `action_cancel` | →cancelled |
| lab.action_start | hospital.lab.test | `action_start` | requested→in_progress |
| lab.action_complete | hospital.lab.test | `action_complete` | in_progress→completed |
| lab.action_cancel | hospital.lab.test | `action_cancel` | →cancelled |
| radiology.action_start | hospital.radiology.order | `action_start` | requested→in_progress |
| radiology.action_complete | hospital.radiology.order | `action_complete` | in_progress→completed |
| radiology.action_cancel | hospital.radiology.order | `action_cancel` | →cancelled |
| bed.action_set_maintenance | hospital.bed | `action_set_maintenance` | →maintenance |
| bed.action_set_available | hospital.bed | `action_set_available` | →available |
| prescription.action_done | hospital.prescription | `action_done` | draft→done |
| billing.action_create_invoice | hospital.invoice.billing | `action_create_invoice` | creates account.move |
| medical_record.action_create_prescription | hospital.medical.record | `action_create_prescription` | opens prescription form |
| patient.action_open_appointments | hospital.patient | smart button → appointments | |
| patient.action_open_admissions | hospital.patient | smart button → admissions | |
| dashboard.action_open_dashboard | hospital.dashboard | opens dashboard | |
