from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RmAbsenceRule(models.Model):
    _name = "rm.absence.rule"
    _description = "Absence Rule"
    _rec_name = "name"

    name = fields.Char(required=True, translate=True)
    step_ids = fields.One2many("rm.absence.step", "rule_id", string="Absence Steps")
    active = fields.Boolean(default=True)
    policy_id = fields.Many2one("rm.attendance.policy", string="Policy", ondelete="cascade")
    company_id = fields.Many2one(related="policy_id.company_id", store=True, readonly=True)

    def get_penalty(self, absence_count, daily_rate):
        self.ensure_one()
        step = self.step_ids.filtered(lambda s: s.active and s.matches(absence_count))[:1]
        if not step:
            return daily_rate
        return step.get_penalty(daily_rate)


class RmAbsenceStep(models.Model):
    _name = "rm.absence.step"
    _description = "Absence Penalty Step"
    _order = "min_days, max_days"

    rule_id = fields.Many2one("rm.absence.rule", required=True, ondelete="cascade")
    name = fields.Char(compute="_compute_name", store=True)
    min_days = fields.Integer(string="Min Days", required=True, default=1)
    max_days = fields.Integer(string="Max Days", help="Use 0 for no upper limit.")
    step_type = fields.Selection(
        [("rate", "Rate"), ("amount", "Fixed Amount per Day")],
        required=True,
        default="rate",
    )
    rate_value = fields.Float(string="Rate Value", default=1.0, digits=(16, 4))
    fixed_amount = fields.Float(string="Fixed Amount per Day", digits=(16, 2))
    active = fields.Boolean(default=True)

    @api.depends("min_days", "max_days", "step_type")
    def _compute_name(self):
        for step in self:
            upper = step.max_days if step.max_days else "+"
            step.name = f"{step.min_days}-{upper} days ({step.step_type})"

    @api.constrains("min_days", "max_days", "rate_value", "fixed_amount")
    def _check_values(self):
        for step in self:
            if step.min_days < 1:
                raise ValidationError(self.env._("Min days must be at least 1."))
            if step.max_days < 0:
                raise ValidationError(self.env._("Max days cannot be negative."))
            if step.max_days and step.max_days < step.min_days:
                raise ValidationError(self.env._("Max days must be greater than min days."))
            if step.rate_value < 0 or step.fixed_amount < 0:
                raise ValidationError(self.env._("Penalty values cannot be negative."))

    def matches(self, absence_count):
        self.ensure_one()
        return absence_count >= self.min_days and (not self.max_days or absence_count <= self.max_days)

    def get_penalty(self, daily_rate):
        self.ensure_one()
        if self.step_type == "amount":
            return self.fixed_amount
        return daily_rate * self.rate_value
