# Model Design — el_hospital

## Design Principles

1. **Prefix everything**: كل النماذج تبدأ بـ `hospital.`، كل الـ XML IDs تبدأ بـ `el_hospital_`
2. **Respect Odoo conventions**: استخدام `mail.thread` + `mail.activity.mixin` للنماذج الرئيسية
3. **Sequence-based names**: كل النماذج التشغيلية لها sequence (AP/, MR/, RX/, ADM/, LAB/, RAD/, BILL/)
4. **State machines**: النماذج التشغيلية لها workflow states واضح
5. **Computed fields**: للإحصائيات والـ KPIs (counts, ages, days)
6. **Smart relations**: المريض = res.partner (إعادة استخدام بيانات الاتصال)
7. **Integration via M2O**: الطبيب → hr.employee، الفاتورة → account.move، الدواء → product.product

## Inheritance Strategy

| Model | Inheritance | Reason |
|-------|-------------|--------|
| hospital.patient | classic + inherits res.partner | reuse contact fields via related |
| hospital.physician | classic + relates to hr.employee | link to HR |
| hospital.medicament | classic + relates to product.product | link to stock |
| hospital.invoice.billing | classic + relates to account.move | link to accounting |

## Key Computed Fields

- `hospital.patient.age` — computed from birth_date
- `hospital.patient.appointment_count` — count of appointments
- `hospital.patient.admission_count` — count of admissions
- `hospital.ward.bed_count` — count beds
- `hospital.ward.occupied_count` — count occupied beds
- `hospital.ward.available_count` — count available beds
- `hospital.admission.days_count` — discharge - admission days
- `hospital.medicament.stock_qty` — from stock.quant
- `hospital.invoice.billing.amount_total` — sum of lines

## Constraints

- `hospital.patient`: unique partner_id (one record per partner)
- `hospital.physician`: unique medical_license
- `hospital.ward`: unique code
- `hospital.bed`: unique (ward_id, bed_number)
- All appointments: appointment_date >= now (on draft)
- All admissions: discharge_date > admission_date (on discharge)
