from odoo import fields, models


class ResourceCalendarLeaves(models.Model):
    _inherit = "resource.calendar.leaves"

    active_for_overtime = fields.Boolean(
        string="Active for Overtime",
        default=True,
        help="If enabled, attendance on this public holiday uses holiday overtime rules.",
    )
    rm_public_holiday = fields.Boolean(
        string="Attendance Public Holiday",
        default=False,
        help="Marks this company time off as a public holiday for attendance sheets.",
    )
    employee_ids = fields.Many2many(
        "hr.employee",
        "rm_public_holiday_employee_rel",
        "leave_id",
        "employee_id",
        string="Eligible Employees",
    )
    department_ids = fields.Many2many(
        "hr.department",
        "rm_public_holiday_department_rel",
        "leave_id",
        "department_id",
        string="Eligible Departments",
    )
    employee_category_ids = fields.Many2many(
        "hr.employee.category",
        "rm_public_holiday_category_rel",
        "leave_id",
        "category_id",
        string="Eligible Employee Tags",
    )

    def applies_to_employee(self, employee):
        self.ensure_one()
        if not employee:
            return False
        if self.employee_ids and employee not in self.employee_ids:
            return False
        if self.department_ids and employee.department_id not in self.department_ids:
            return False
        if self.employee_category_ids and not (employee.category_ids & self.employee_category_ids):
            return False
        return True
