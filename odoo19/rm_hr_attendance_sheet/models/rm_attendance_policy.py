from odoo import fields, models


class RmAttendancePolicy(models.Model):
    _name = "rm.attendance.policy"
    _description = "Attendance Policy"
    _rec_name = "name"
    _order = "effective_date desc, name"

    name = fields.Char(required=True, translate=True)
    effective_date = fields.Date(default=fields.Date.today, required=True)
    overtime_rule_ids = fields.One2many("rm.overtime.rule", "policy_id", string="Overtime Rules")
    lateness_rule_ids = fields.One2many("rm.lateness.rule", "policy_id", string="Lateness Rules")
    absence_rule_ids = fields.One2many("rm.absence.rule", "policy_id", string="Absence Rules")
    version_ids = fields.One2many("hr.version", "attendance_policy_id", string="Employee Records")
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
