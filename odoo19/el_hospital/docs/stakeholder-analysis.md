# Stakeholder Analysis — el_hospital

## Stakeholder Matrix

| # | Name/Title | Role | Influence | Impact | Attitude | Engagement |
|---|-----------|------|-----------|--------|----------|------------|
| 1 | Hospital Director (Sponsor) | Sponsor | High | High | Supportive | Monthly summary + KPI dashboard |
| 2 | Medical Director | Champion | High | High | Supportive | Weekly demo + clinical workflow review |
| 3 | Doctors (Physicians) | Key User | High | High | Neutral | Hands-on training + EMR/prescription feedback |
| 4 | Nurses | Key User | Medium | High | Neutral | Training on admission/discharge + wards |
| 5 | Receptionists / Front Desk | Key User | Low | High | Unknown | Training on patient registration + appointments |
| 6 | Lab Technicians | End User | Low | Medium | Unknown | Training on lab test entry + results |
| 7 | Pharmacists | End User | Low | Medium | Unknown | Training on pharmacy + stock |
| 8 | Accounting / Billing | Key User | Medium | High | Supportive | Integration demo + billing workflow |
| 9 | IT Admin | IT Admin | Medium | Medium | Supportive | Technical docs + deployment guide |

## Key Concerns to Address
- الأطباء يريدون واجهة سريعة للسجل الطبي والوصفات دون خطوات معقدة
- Receptionists يحتاجون بحث سريع عن المرضى وحجز المواعيد
- Billing يحتاج تكامل سلس مع Accounting (account.move)
- IT يريد موديول نظيف بدون تعارضات (prefix el_hospital_)
- Nurses يحتاجون رؤية واضحة للأسرّة وحالة الإقامة

## User Roles → Security Groups Mapping

| Stakeholder | Security Group | Permissions |
|-------------|---------------|-------------|
| Hospital Admin / Director | `group_hospital_admin` | Full access (read, write, create, unlink) |
| Doctor / Physician | `group_hospital_doctor` | Patients, appointments, EMR, prescriptions (full) |
| Nurse | `group_hospital_nurse` | Wards, beds, admissions (read/write) |
| Receptionist | `group_hospital_reception` | Patients, appointments (read/write) |
| Lab Technician | `group_hospital_lab` | Lab tests + radiology (read/write) |
| Pharmacist | `group_hospital_pharmacy` | Medicaments + pharmacy billing (read/write) |
| End User (read-only) | `group_hospital_user` | Read own/department records |

## Security Group Hierarchy (implied_ids)
```
group_hospital_user (base)
  └─ group_hospital_reception
  └─ group_hospital_lab
  └─ group_hospital_pharmacy
  └─ group_hospital_nurse
  └─ group_hospital_doctor
       └─ group_hospital_admin (top)
```
