# Requirements Summary — el_hospital

## Target
- Odoo version: 19
- Module name: `el_hospital`
- License: LGPL-3
- Author: Ibrahim Elmasry

## Purpose
نظام إدارة مستشفى متكامل يغطي: المرضى، المواعيد، السجل الطبي (EMR)،
الإقامة والأسرّة، التحاليل والأشعة، الصيدلية والفواتير، ومتابعة
الوصفات والفحوصات — مع تكامل كامل مع HR + Accounting + Stock.

## Models Needed

### Core
1. `hospital.patient` — بيانات المريض (ربط بـ res.partner)
2. `hospital.appointment` — المواعيد بين المريض والطبيب
3. `hospital.medical.record` (EMR) — السجل الطبي للمريض
4. `hospital.prescription` — الوصفات الطبية + `hospital.prescription.line`
5. `hospital.department` — أقسام المستشفى

### Wards & Beds
6. `hospital.ward` — الغرف والأجنحة
7. `hospital.bed` — الأسرّة
8. `hospital.admission` — دخول وخروج المرضى (Inpatient)

### Laboratory & Radiology
9. `hospital.lab.test` — التحاليل المخبرية
10. `hospital.radiology.order` — طلبات الأشعة

### Pharmacy & Billing
11. `hospital.medicament` — الأدوية (ربط بـ product.product)
12. `hospital.invoice.billing` — الفواتير الطبية (ربط بـ account.move)

### Doctors / Staff (extend HR)
13. `hospital.physician` — الأطباء (ربط بـ hr.employee / res.users)

## Features
- إدارة كاملة للمرضى (CRUD + search + smart views)
- نظام مواعيد متكامل (تأكيد، إلغاء، إعادة جدولة)
- سجل طبي إلكتروني لكل مريض (EMR) مع التاريخ الكامل
- وصفات طبية قابلة للطباعة (PDF report)
- إدارة أقسام، غرف وأسرّة مع تتبع الإشغال
- دخول/خروج المرضى (Admission/Discharge workflow)
- طلبات تحاليل مخبرية وأشعة مع النتائج
- صيدلية: أصناف أدوية مع مخزون
- فواتير طبية مدمجة مع Accounting
- تكامل مع HR للأطباء والموظفين
- Dashboard بإحصائيات ورسوم بيانية (Chart.js)
- مجموعات أمنية (Roles): Doctor, Nurse, Receptionist, Lab Tech, Pharmacist, Admin
- تقارير PDF (وصفة، تذكرة مرض، فاتورة)
- Workflow states + automated email notifications

## Integration
- `hr` — الأطباء كموظفين
- `account` — الفواتير والمدفوعات
- `stock` — مخزون الأدوية والمستلزمات
- `mail` — chatter + email templates

## Open Questions
- لا توجد أسئلة مفتوحة — النطاق محدد والموافقة تمت.
