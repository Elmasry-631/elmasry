from odoo import fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    attendance_sheet_id = fields.Many2one(
        "rm.attendance.sheet",
        string="Attendance Sheet",
        readonly=True,
        copy=False,
    )
