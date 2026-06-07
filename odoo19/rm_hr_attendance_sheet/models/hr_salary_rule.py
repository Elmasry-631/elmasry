from odoo import models


class HrSalaryRule(models.Model):
    _inherit = "hr.salary.rule"

    def _rm_configure_attendance_basic_rule(self):
        structure = self.env.ref("rm_hr_attendance_sheet.structure_attendance_sheet", raise_if_not_found=False)
        if not structure:
            return
        basic_rule = self.search(
            [
                ("struct_id", "=", structure.id),
                ("code", "=", "BASIC"),
            ],
            order="id",
            limit=1,
        )
        if not basic_rule:
            return
        basic_rule.write(
            {
                "name": "Basic Salary from Attendance Sheet",
                "condition_select": "none",
                "amount_select": "code",
                "amount_python_compute": """
sheet = payslip.attendance_sheet_id
if sheet:
    wage = sheet.version_id.wage or version.wage or 0.0
    planned = sheet.total_planned_hours or 0.0
    worked = sheet.total_worked_hours or 0.0
    result = wage * min(worked / planned, 1.0) if planned else wage
else:
    result = payslip.paid_amount
""",
            }
        )
