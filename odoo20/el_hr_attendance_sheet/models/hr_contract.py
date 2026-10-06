from odoo import api, fields, models


class HrContract(models.Model):
    _inherit = 'hr.version'

    attendance_policy_id = fields.Many2one(
        'hr.attendance.policy',
        string='Attendance Policy',
        help="Select the attendance policy that determines how overtime, "
             "lateness and absence are calculated for this contract.",
        tracking=True,
    )


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    attendance_policy_id = fields.Many2one(
        related='version_id.attendance_policy_id',
        string='Attendance Policy',
        readonly=False,
        inherited=True,
        groups="hr.group_hr_manager",
        tracking=True,
    )
