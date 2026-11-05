# Hospital Management System

- **المسار والإصدار:** `odoo19/el_hospital` — Odoo 19
- **إصدار الحزمة:** `19.0.1.0.0`
- **الترخيص المعلن:** `LGPL-3`
- **الملخص المعلن:** Complete hospital management: patients, appointments, EMR, wards, lab, pharmacy, billing

## الصلاحيات والحماية المكتشفة

### ACL

- access_hospital_department_user: model=model_hospital_department, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_department_admin: model=model_hospital_department, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_physician_user: model=model_hospital_physician, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_physician_doctor: model=model_hospital_physician, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_physician_admin: model=model_hospital_physician, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_patient_user: model=model_hospital_patient, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_patient_reception: model=model_hospital_patient, group=group_hospital_reception, read/write/create/delete=1/1/1/1
- access_hospital_patient_doctor: model=model_hospital_patient, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_patient_admin: model=model_hospital_patient, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_patient_allergy_user: model=model_hospital_patient_allergy, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_patient_allergy_doctor: model=model_hospital_patient_allergy, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_patient_allergy_admin: model=model_hospital_patient_allergy, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_patient_disease_user: model=model_hospital_patient_disease, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_patient_disease_doctor: model=model_hospital_patient_disease, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_patient_disease_admin: model=model_hospital_patient_disease, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_appointment_user: model=model_hospital_appointment, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_appointment_reception: model=model_hospital_appointment, group=group_hospital_reception, read/write/create/delete=1/1/1/1
- access_hospital_appointment_doctor: model=model_hospital_appointment, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_appointment_admin: model=model_hospital_appointment, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_medical_record_user: model=model_hospital_medical_record, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_medical_record_doctor: model=model_hospital_medical_record, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_medical_record_admin: model=model_hospital_medical_record, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_prescription_user: model=model_hospital_prescription, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_prescription_doctor: model=model_hospital_prescription, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_prescription_pharmacy: model=model_hospital_prescription, group=group_hospital_pharmacy, read/write/create/delete=1/1/1/1
- access_hospital_prescription_admin: model=model_hospital_prescription, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_prescription_line_user: model=model_hospital_prescription_line, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_prescription_line_doctor: model=model_hospital_prescription_line, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_prescription_line_pharmacy: model=model_hospital_prescription_line, group=group_hospital_pharmacy, read/write/create/delete=1/1/1/1
- access_hospital_prescription_line_admin: model=model_hospital_prescription_line, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_ward_user: model=model_hospital_ward, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_ward_nurse: model=model_hospital_ward, group=group_hospital_nurse, read/write/create/delete=1/1/1/1
- access_hospital_ward_admin: model=model_hospital_ward, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_bed_user: model=model_hospital_bed, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_bed_nurse: model=model_hospital_bed, group=group_hospital_nurse, read/write/create/delete=1/1/1/1
- access_hospital_bed_admin: model=model_hospital_bed, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_admission_user: model=model_hospital_admission, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_admission_nurse: model=model_hospital_admission, group=group_hospital_nurse, read/write/create/delete=1/1/1/1
- access_hospital_admission_doctor: model=model_hospital_admission, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_admission_admin: model=model_hospital_admission, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_lab_test_user: model=model_hospital_lab_test, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_lab_test_lab: model=model_hospital_lab_test, group=group_hospital_lab, read/write/create/delete=1/1/1/1
- access_hospital_lab_test_doctor: model=model_hospital_lab_test, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_lab_test_admin: model=model_hospital_lab_test, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_radiology_user: model=model_hospital_radiology_order, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_radiology_lab: model=model_hospital_radiology_order, group=group_hospital_lab, read/write/create/delete=1/1/1/1
- access_hospital_radiology_doctor: model=model_hospital_radiology_order, group=group_hospital_doctor, read/write/create/delete=1/1/1/1
- access_hospital_radiology_admin: model=model_hospital_radiology_order, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_medicament_user: model=model_hospital_medicament, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_medicament_pharmacy: model=model_hospital_medicament, group=group_hospital_pharmacy, read/write/create/delete=1/1/1/1
- access_hospital_medicament_admin: model=model_hospital_medicament, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_invoice_billing_user: model=model_hospital_invoice_billing, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_invoice_billing_reception: model=model_hospital_invoice_billing, group=group_hospital_reception, read/write/create/delete=1/1/1/1
- access_hospital_invoice_billing_admin: model=model_hospital_invoice_billing, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_invoice_billing_line_user: model=model_hospital_invoice_billing_line, group=group_hospital_user, read/write/create/delete=1/0/0/0
- access_hospital_invoice_billing_line_reception: model=model_hospital_invoice_billing_line, group=group_hospital_reception, read/write/create/delete=1/1/1/1
- access_hospital_invoice_billing_line_admin: model=model_hospital_invoice_billing_line, group=group_hospital_admin, read/write/create/delete=1/1/1/1
- access_hospital_dashboard_user: model=model_hospital_dashboard, group=group_hospital_user, read/write/create/delete=1/1/1/1

### المجموعات وقواعد السجلات

- المجموعات: `group_hospital_user`, `group_hospital_reception`, `group_hospital_lab`, `group_hospital_pharmacy`, `group_hospital_nurse`, `group_hospital_doctor`, `group_hospital_admin`, `group_hospital_admin`, `group_hospital_doctor`, `group_hospital_nurse`, `group_hospital_reception`, `group_hospital_lab`, `group_hospital_pharmacy`
- قواعد السجلات: `rule_hospital_company`

### واجهات HTTP ورفع الصلاحيات

- لا توجد عناصر معلنة في ملفات الموديول.

مواضع `sudo()` المرصودة:

- لا توجد عناصر معلنة في ملفات الموديول.

أخفِ الأسرار الفعلية من سجلات النظام، وراجع ACL وrecord rules على قاعدة بيانات الاختبار. إخفاء زر في الواجهة لا يفرض وحده صلاحية على استدعاء ORM أو RPC.