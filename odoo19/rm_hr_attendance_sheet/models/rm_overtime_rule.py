from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RmOvertimeRule(models.Model):
    _name = "rm.overtime.rule"
    _description = "Overtime Rule"
    _order = "ot_type, apply_after, rate"

    name = fields.Char(required=True, translate=True)
    ot_type = fields.Selection(
        [
            ("working_day", "Working Day"),
            ("weekend", "Weekend"),
            ("public_holiday", "Public Holiday"),
        ],
        string="Overtime Type",
        required=True,
        default="working_day",
    )
    apply_after = fields.Float(string="Apply After (minutes)", default=0.0, required=True)
    rate = fields.Float(string="Rate Multiplier", default=1.5, required=True, digits=(16, 4))
    active = fields.Boolean(default=True)
    policy_id = fields.Many2one("rm.attendance.policy", string="Policy", ondelete="cascade")
    company_id = fields.Many2one(related="policy_id.company_id", store=True, readonly=True)

    @api.constrains("apply_after", "rate")
    def _check_values(self):
        for rule in self:
            if rule.apply_after < 0:
                raise ValidationError(self.env._("Apply After cannot be negative."))
            if rule.rate < 0:
                raise ValidationError(self.env._("Rate cannot be negative."))
