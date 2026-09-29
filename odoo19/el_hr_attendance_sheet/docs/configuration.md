# Configuration — el_hr_attendance_sheet

> Setup steps to configure the module after installation.

## 1. Install the Module

1. Go to **Apps** → search "Attendance Sheet"
2. Click **Install** on "HR Attendance Sheet And Policies"
3. Wait for dependencies to install (hr_attendance, hr_payroll, hr_holidays)

## 2. Configure Attendance Policy

A policy is the container that combines overtime, lateness and absence rules.

### 2.1 Create Overtime Rules

Go to: **Attendance → Attendance Sheets → Configuration → Rules → Overtime Rules**

Create 3 rules (one per type):

| Name | Type | Apply After (min) | Rate |
|------|------|-------------------|------|
| OT Working Days | working_day | 30 | 1.5 |
| OT Weekends | weekend | 0 | 2.0 |
| OT Public Holidays | public_holiday | 0 | 3.0 |

### 2.2 Create Lateness Rule

Go to: **Configuration → Rules → Lateness Rules**

Create a rule with multiple steps:

| From (min) | To (min) | Penalty Type | Rate | Initial Rate | Amount |
|------------|----------|--------------|------|--------------|--------|
| 0 | 15 | rate | 1.0 | 1.0 | — |
| 15 | 30 | rate | 1.5 | 1.0 | — |
| 30 | 60 | rate | 2.0 | 1.0 | — |
| 60 | 9999 | amount | — | — | 25.00 |

### 2.3 Create Absence Rule

Go to: **Configuration → Rules → Absence Rules**

Create a rule with steps:

| From (days) | To (days) | Rate |
|-------------|-----------|------|
| 1 | 3 | 1.0 |
| 4 | 7 | 1.5 |
| 8 | 9999 | 2.0 |

### 2.4 Create the Policy

Go to: **Configuration → Attendance Policies**

Create a policy:

| Field | Value |
|-------|-------|
| Name | Standard Policy 2026 |
| Company | (your company) |
| Overtime Rule (Working Days) | OT Working Days |
| Overtime Rule (Weekends) | OT Weekends |
| Overtime Rule (Public Holidays) | OT Public Holidays |
| Lateness Rule | (the rule you just created) |
| Absence Rule | (the rule you just created) |

## 3. Assign Policy to Contracts

Go to: **Employees → Contracts** → open each contract

In the **Attendance Policy** group, select the policy you created.

> **Tip:** Use developer mode + list view to bulk-assign the policy to multiple contracts.

## 4. Define Public Holidays (optional)

Go to: **Attendance → Attendance Sheets → Configuration → Public Holidays**

1. Create a new record (e.g. "National Day 2026")
2. Set date_from and date_to
3. In the Lines tab, specify which employees/departments/tags this holiday applies to
4. Click **Activate** to make it effective

Leave the Lines empty + add only a department → holiday applies to all employees in that department.

## 5. Ensure Contracts Have Working Schedule

Each contract must have a `resource_calendar_id` set (standard Odoo field under "Working Schedule"). The sheet uses this to compute planned hours per day.

If a contract has no working schedule, sheet computation will raise:
> "Contract XYZ has no working schedule (resource.calendar)."

## 6. Configure Salary Structure

The module ships an "Attendance Structure" salary structure with 4 rules:

| Code | Name | Category | Formula (summary) |
|------|------|----------|-------------------|
| OVERT | Overtime | Allowance | `OT_hours × (wage/240) × rate` |
| LATE | Lateness Deduction | Deduction | `-(late_hours × wage/240)` |
| ABS | Absence Deduction | Deduction | `-(absence_days × wage/30 × step_rate)` |
| DIFF | Difference Time | Deduction | `-(diff_hours × wage/240)` |

You can modify these formulas via **Payroll → Configuration → Rules** after install.

## 7. User Groups

Assign users to the appropriate group:

| Group | Best for |
|-------|----------|
| Attendance Sheet User | Employees who only need to view their own sheets |
| Attendance Sheet Officer | HR staff who create/approve sheets |
| Attendance Sheet Manager | HR managers who configure rules/policies |

The admin user is automatically added to the Manager group on install.

## 8. Multi-Company Setup

If you have multiple companies:
1. Create separate policies per company (the company_id field on policy)
2. Create separate rules per company
3. Assign each contract the policy from its own company

Record rules automatically restrict access to the user's companies.

## 9. Optional: Cron Job for Monthly Batch

For monthly payroll, you can set up a scheduled action to auto-generate batches:

1. Go to **Settings → Technical → Automation → Scheduled Actions**
2. Create a new action:
   - Name: "Monthly Attendance Sheet Batch"
   - Model: hr.attendance.sheet.batch.wizard
   - Method: action_create_batch
   - Frequency: monthly (1st of each month)

> Note: The wizard requires user context. For full automation, write a custom method that creates the batch directly.

---

*Author: Ibrahim Elmasry*
