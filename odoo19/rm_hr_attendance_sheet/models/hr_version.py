from odoo import fields, models


class HrVersion(models.Model):
    _inherit = "hr.version"

    attendance_policy_id = fields.Many2one(
        "rm.attendance.policy",
        string="Attendance Policy",
        check_company=True,
        tracking=True,
    )
