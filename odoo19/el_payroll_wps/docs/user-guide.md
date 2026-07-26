# User Guide — el_payroll_wps

## Audience
HR Officer responsible for monthly WPS submission.

## Frequency
Once per month, after all payslips for that month are validated.

## Steps

### 1. Validate the payslips
Before running the export, make sure every payslip for the target month is in `validated` or `paid` state. Draft or cancelled payslips are NOT included.

**Path:** Payroll → Payslips → select all → Action → Confirm → (Action → Set to Paid if applicable).

### 2. Open the WPS Export wizard
**Path:** Payroll → WPS Export

A modal opens with a single field: `Month`. It defaults to today's date.

### 3. Pick the month
- Click the date picker.
- Select ANY day inside the month you want to export.
- The day you pick doesn't matter — only the year and month are used.

### 4. Click "Export CSV"
- If no validated payslips exist for that month → red error modal.
- If payslips exist → browser downloads `Salary_<Month>_<Year>.csv` immediately.

### 5. Submit to the bank
- Log in to your bank's WPS portal.
- Upload the CSV file.

## What each column means

| Column | What to verify |
|--------|----------------|
| Bank | Should match your company's WPS-registered bank |
| Account | Should be the employee's IBAN (or local equivalent) |
| Salary(total) | Net salary of the employee for the month |
| Notice(month) | The month name (e.g. `July`) |
| Name | Employee's full name as in HR |
| ID number | National ID / Iqama / Passport |
| address | Employee's state/province (from `private_state_id`) |
| wage | Basic wage (basic salary only — no allowances) |
| house | Housing allowance (0 if not entitled) |
| Others | Allowances − Deductions — informational |
| discount | Total deductions as a **positive** number (e.g. `200.00`) |

## Editing `x_others` manually
1. Open the payslip.
2. After the `note` field, find `Others`.
3. Type your value.
4. Save.

The override persists until you click **Compute Sheet** again.

## Common Scenarios

### "I need to re-export last month"
- Pick any date in last month in the wizard.

### "An employee's bank account is missing"
- CSV row will have empty `Bank` and `Account` columns for that employee.
- Fix: HR → Employees → open employee → set Primary Bank Account.

### "I made a mistake on a payslip and need to re-export"
1. Open the payslip.
2. Set to Draft (if it was validated/paid).
3. Make corrections.
4. Compute Sheet → Confirm → (Set to Paid if applicable).
5. Re-run the WPS Export wizard.

## What NOT to do
- Don't rename salary rule codes (`BASIC`, `HOUALLOW`, `NET`) — the wizard looks them up by code.
- Don't rename salary rule categories (`ALW`, `DED`).
- Don't edit the CSV file in Excel and re-save — Excel may strip the UTF-8 BOM.
