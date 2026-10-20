# Attendance Sheet Repair Report

## Changes applied

- Split overtime totals by `working_day`, `weekend`, and `public_holiday`; payroll now applies each policy's configured rate independently.
- Expanded stored payslip compute dependencies to cover the sheet totals and line fields used by the computation.
- Disabled monetary calculation in the `DIFF` salary rule for now. The raw difference overlaps with lateness and absence deductions, so charging it without an explicit business policy can double-deduct the same hours. The field remains available for reporting. Enable a deduction only after the business owner defines how it interacts with `LATE`, `ABS`, paid leave, and overtime.
- Added ORM-level state transition checks for attendance sheets, batches, and public holidays; prevented direct status writes from bypassing workflow actions and blocked changes to key attendance data after approval, completion, or cancellation. Attendance lines can only be created/edited/deleted while the parent sheet is Draft or Computed (with cancelled-sheet cleanup allowed).
- Added company consistency checks between sheet, employee, contract, and attendance policy.
- Changed batch generation to create sheets only for the selected employees (when selected), without creating and deleting unrelated sheets. Failed employees remain visible with an error message; per-employee savepoints prevent one failure from leaving partial computation changes.
- Added company record rules for attendance-sheet lines, batch lines, public-holiday lines, and the nested lateness/absence rules. Added officer access rules so the employee-self rules do not unintentionally narrow officer/manager access within allowed companies.
- Propagated the `DIFF` rule alongside the other attendance salary rules.
- Converted attendance and leave datetimes to the work-calendar timezone when assigning them to local work dates; handled ambiguous/non-existent local times deterministically.

## Static validation performed

- Python source compiled with `compileall`.
- All XML files parsed successfully with `lxml`.
- No Odoo server or configured database was available in this repair environment, so module installation, ORM tests, salary-rule evaluation, access-rule behavior, and payroll integration were **not** runtime-tested.

## Remaining business decisions / runtime checks

1. Define whether a negative hour difference is independently deductible. Current `DIFF` monetary result is deliberately zero to avoid double-deduction with lateness/absence.
2. Confirm fallback overtime multipliers for missing day-type rules (currently 1.5, matching the existing fallback behavior).
3. Test overnight attendances. Attendance intervals are currently assigned to the local date of check-in; a single attendance crossing local midnight is not split across two daily lines.
4. Run Odoo 19 Community install/upgrade tests and the module's `TransactionCase` suite, including multi-company record-rule checks and a payslip calculation for each overtime day type.
