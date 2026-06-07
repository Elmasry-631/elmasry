# تحليل شامل لموديول `bi_employee_travel_managment` (Odoo 19)

---

## 📌 اسم الموديول ووصفه

**الاسم:** HR Employee Travel Expense in Odoo

**المُعرف التقني:** `bi_employee_travel_managment`

**المطور:** BROWSEINFO

**الفئة:** الموارد البشرية (Human Resources)

### الوصف العام
هذا الموديول يتيح إدارة سفر الموظفين ومصروفات السفر بشكل شامل. يقوم بتنظيم طلبات السفر للموظفين بدءاً من الإنشاء، ثم التأكيد، ثم الموافقة، ثم العودة من السفر، ثم إنشاء المصروفات الفعلية وتقديمها كطلب مصروفات في نظام hr.expense المدمج.

### الوظائف الرئيسية:
- إنشاء طلبات سفر مع تفاصيل كاملة (الغرض، المشروع، العناوين، التواريخ)
- سير عمل كامل: Draft → Confirmed → Approved → Returned → Submitted
- تحديد الدفعات المقدمة (Advance Payments)
- إنشاء المصروفات تلقائياً من الدفعات المقدمة
- ربط المشاريع والحسابات التحليلية
- تقرير PDF شامل لطلب السفر

---

## 📦 الإصدار والتبعيات

| العنصر | القيمة |
|---|---|
| **الإصدار** | 19.0.0.0 |
| **الترخيص** | OPL-1 |
| **السعر** | 30 يورو |
| **التطبيق الرئيسي** | نعم (`application: True`) |
| **التبعيات** | `base`, `hr`, `hr_expense`, `project` |

---

## 🏗️ الموديلات (Models)

### 1️⃣ `travel.expence` (بند مصروف السفر)

> ⚠️ ملاحظة: الاسم يحتوي خطأ إملائي - expence بدلاً من expense

| الحقل | النوع | الوصف |
|---|---|---|
| `product_id` | `Many2one('product.product')` | المنتج المرتبط (يجب أن يكون قابلاً للتصرف كمصروفات). **إلزامي** |
| `unit_price` | `Float` | سعر الوحدة. **إلزامي** |
| `product_qty` | `Float` | الكمية. **إلزامي** |
| `name` | `Char` | ملاحظة/وصف المصروف |
| `currency_id` | `Many2one('res.currency')` | العملة |

---

### 2️⃣ `travel.request` (طلب السفر — الموديل الرئيسي)

#### الحقول الأساسية:

| الحقل | النوع | الوصف |
|---|---|---|
| `name` | `Char` (readonly) | رقم الطلب (يُولّد تلقائياً: TR/0001) |
| `employee_id` | `Many2one('hr.employee')` | الموظف صاحب الطلب. **إلزامي** |
| `department_manager_id` | `Many2one('hr.employee')` | مدير القسم (يُملأ تلقائياً) |
| `department_id` | `Many2one('hr.department')` | القسم |
| `job_id` | `Many2one('hr.job')` | المسمى الوظيفي. **إلزامي** |
| `travel_purpose` | `Char` | غرض السفر. **إلزامي** |
| `project_id` | `Many2one('project.task')` | المشروع المرتبط. **إلزامي** |
| `account_analytic_id` | `Many2one('account.analytic.account')` | الحساب التحليلي (يُنشأ تلقائياً) |

#### حقول التواريخ:

| الحقل | النوع | الوصف |
|---|---|---|
| `req_date` | `Date` | تاريخ تقديم الطلب (تلقائي) |
| `confirm_date` | `Date` | تاريخ التأكيد |
| `approve_date` | `Date` | تاريخ الموافقة |
| `req_departure_date` | `Datetime` | تاريخ المغادرة المطلوب. **إلزامي** |
| `req_return_date` | `Datetime` | تاريخ العودة المطلوب. **إلزامي** |
| `available_departure_date` | `Datetime` | تاريخ المغادرة الفعلي |
| `available_return_date` | `Datetime` | تاريخ العودة الفعلي |

#### حقول تفاصيل السفر:

| الحقل | النوع | الوصف |
|---|---|---|
| `from_city` / `to_city` | `Char` | مدينة الانطلاق / الوجهة |
| `from_state_id` / `to_state_id` | `Many2one('res.country.state')` | الولاية |
| `from_country_id` / `to_country_id` | `Many2one('res.country')` | البلد |
| `days` | `Char` (compute) | عدد الأيام المحسوب |
| `phone_no` / `email` | `Char` | رقم التواصل / البريد الإلكتروني |

#### حقول وسائل النقل:

| الحقل | النوع | الوصف |
|---|---|---|
| `req_travel_mode_id` | `Many2one('travel.mode')` | وسيلة النقل المطلوبة للذهاب |
| `return_mode_id` | `Many2one('travel.mode')` | وسيلة النقل المطلوبة للعودة |
| `departure_mode_travel_id` | `Many2one('travel.mode')` | وسيلة النقل الفعلية للذهاب |
| `return_mode_travel_id` | `Many2one('travel.mode')` | وسيلة النقل الفعلية للعودة |

#### حقول أخرى:

| الحقل | النوع | الوصف |
|---|---|---|
| `visa_agent_id` | `Many2one('res.partner')` | وكيل التأشيرة |
| `ticket_booking_agent_id` | `Many2one('res.partner')` | وكيل حجز التذاكر |
| `bank_id` | `Many2one('res.bank')` | البنك |
| `cheque_number` | `Char` | رقم الشيك |
| `advance_payment_ids` | `One2many('hr.expense')` | الدفعات المقدمة |
| `expense_ids` | `One2many('hr.expense')` | المصروفات الفعلية |

#### حالات سير العمل (State):

| الحالة | الوصف |
|---|---|
| `draft` | مسودة (افتراضية) |
| `confirmed` | مؤكدة |
| `approved` | معتمدة |
| `rejected` | مرفوضة |
| `returned` | تم العودة من السفر |
| `submitted` | تم تقديم المصروفات |

#### الطرق (Methods):

| الطريقة | الوصف |
|---|---|
| `onchange_employee()` | نسخ تلقائي للمدير والوظيفة والقسم عند اختيار الموظف |
| `check_dates()` | التحقق من صحة التواريخ (المغادرة قبل العودة) |
| `create()` | توليد رقم تسلسلي TR/XXXX |
| `write()` | إنشاء حساب تحليلي تلقائي عند تغيير المشروع |
| `action_confirm()` | نقل من draft إلى confirmed |
| `action_approve()` | نقل من confirmed إلى approved (يتطلب HR Travel Manager) |
| `action_reject()` | نقل من confirmed إلى rejected |
| `return_from_trip()` | نقل إلى returned ونسخ الدفعات المقدمة |
| `action_create_expence()` | إنشاء سجلات hr.expense ونقل إلى submitted |
| `action_draft()` | إعادة إلى draft |

---

### 3️⃣ `travel.mode` (وسائل النقل)

| الحقل | النوع | الوصف |
|---|---|---|
| `name` | `Char` | اسم وسيلة النقل |

---

### 4️⃣ `HrExpense` (يرث من `hr.expense`)

| الحقل | النوع | الوصف |
|---|---|---|
| `travel_id` | `Many2one('travel.request')` | ربط المصروف كدفعة مقدمة |
| `travel_expence_id` | `Many2one('travel.request')` | ربط المصروف كمصروف فعلي |

---

## 🖥️ الواجهات (Views)

### عرض القائمة (`view_travel_req_list`)
- يعرض: الموظف، المدير، القسم، الوظيفة، العملة، مقدم الطلب، المُؤكِّد، المُعتمِد

### عرض النموذج (`view_travel_req_form`)
- شريط حالة (statusbar): Draft → Confirmed → Approved → Returned
- أزرار سير العمل: Confirm, Approve/Reject, Return, Create Expenses, Reset To Draft
- زر ذكي "Expense" في حالة Submitted
- دفتر ملاحظات (Notebook) بأربع صفحات:
  1. Travel Request information
  2. Other Info
  3. Advance Payment
  4. Expenses

### القائمة (Menu)
- **Travel** (ترتيب 22)
  - Employee Travel Request (للجميع)
  - Travel Request To Approve (للمدراء فقط)

---

## 🖨️ التقارير (Reports)

- تقرير PDF شامل لطلب السفر
- يحتوي على: معلومات أساسية، تفاصيل السفر، معلومات أخرى، بيانات بنكية، الدفعات المقدمة، المصروفات الفعلية

---

## 🔒 الأمان (Security)

| المعرف | الاسم | الوصف |
|---|---|---|
| `hr_travel_manager_id` | HR Manager (Travel) | مجموعة المدراء المصرح لهم بالموافقة/الرفض |

جميع المستخدمين لديهم صلاحيات كاملة (قراءة، كتابة، إنشاء، حذف) على جميع الموديلات.

---

## 🚀 طريقة الاستخدام

1. **إنشاء طلب سفر:** Travel → Travel Request → New
2. **ملء البيانات:** اختيار الموظف (تلقائي: المدير، الوظيفة، القسم)، الغرض، المشروع، العناوين، التواريخ
3. **تأكيد الطلب:** الموظف يضغط "Confirm"
4. **الموافقة:** HR Travel Manager يوافق أو يرفض
5. **العودة من السفر:** بعد اكتمال السفر، يضغط "Return"
6. **إنشاء المصروفات:** يضغط "Create Expenses"
7. **طباعة التقرير:** يمكن طباعة تقرير PDF

---

## 🔧 ملاحظات تقنية

### ✅ نقاط القوة:
- سير عمل متكامل ومفهوم جيداً
- ربط مع موديلات hr.expense و project المدمجة
- تقرير PDF شامل
- 6 حالات سير عمل

### ⚠️ القصور:
- خطأ إملائي في اسم الموديل (`travel.expence`)
- خطأ في رسالة التحقق من التواريخ
- علامة `<openerp>` قديمة في التقرير
- أمان ضعيف (جميع المستخدمين لديهم صلاحيات حذف)
- حقل `project_id` من نوع `project.task` وليس `project.project`
- لا يوجد إشعارات أو بريد إلكتروني تلقائي
