from odoo import api, fields, models
from odoo.exceptions import ValidationError


class RmLatenessRule(models.Model):
    _name = "rm.lateness.rule"
    _description = "Lateness Rule"
    _rec_name = "name"

    name = fields.Char(required=True, translate=True)
    step_ids = fields.One2many("rm.lateness.step", "rule_id", string="Lateness Steps")
    active = fields.Boolean(default=True)
    policy_id = fields.Many2one("rm.attendance.policy", string="Policy", ondelete="cascade")
    company_id = fields.Many2one(related="policy_id.company_id", store=True, readonly=True)

    def get_penalty(self, minutes, hourly_rate):
        self.ensure_one()
        step = self.step_ids.filtered(lambda s: s.active and s.matches(minutes))[:1]
        if not step:
            return 0.0
        return step.get_penalty(minutes, hourly_rate)


class RmLatenessStep(models.Model):
    _name = "rm.lateness.step"
    _description = "Lateness Penalty Step"
    _order = "min_minutes, max_minutes"

    rule_id = fields.Many2one("rm.lateness.rule", required=True, ondelete="cascade")
    name = fields.Char(compute="_compute_name", store=True)
    min_minutes = fields.Integer(string="Min Minutes", required=True)
    max_minutes = fields.Integer(string="Max Minutes", help="Use 0 for no upper limit.")
    step_type = fields.Selection(
        [("rate", "Rate"), ("amount", "Fixed Amount")],
        required=True,
        default="rate",
    )
    rate_value = fields.Float(string="Rate Value", digits=(16, 4))
    fixed_amount = fields.Float(string="Fixed Amount", digits=(16, 2))
    penalty_calc = fields.Selection(
        [("time_based", "Time-Based"), ("flat", "Flat")],
        string="Penalty Calculation",
        required=True,
        default="time_based",
    )
    active = fields.Boolean(default=True)

    @api.depends("min_minutes", "max_minutes", "step_type")
    def _compute_name(self):
        for step in self:
            upper = step.max_minutes if step.max_minutes else "+"
            step.name = f"{step.min_minutes}-{upper} min ({step.step_type})"

    @api.constrains("min_minutes", "max_minutes", "rate_value", "fixed_amount")
    def _check_values(self):
        for step in self:
            if step.min_minutes < 0 or step.max_minutes < 0:
                raise ValidationError(self.env._("Minutes cannot be negative."))
            if step.max_minutes and step.max_minutes < step.min_minutes:
                raise ValidationError(self.env._("Max minutes must be greater than min minutes."))
            if step.rate_value < 0 or step.fixed_amount < 0:
                raise ValidationError(self.env._("Penalty values cannot be negative."))

    def matches(self, minutes):
        self.ensure_one()
        return minutes >= self.min_minutes and (not self.max_minutes or minutes <= self.max_minutes)

    def get_penalty(self, minutes, hourly_rate):
        self.ensure_one()
        if self.step_type == "amount" or self.penalty_calc == "flat":
            return self.fixed_amount
        charged_minutes = max(minutes - self.min_minutes + 1, 0)
        if self.max_minutes:
            charged_minutes = min(charged_minutes, self.max_minutes - self.min_minutes + 1)
        return (charged_minutes / 60.0) * hourly_rate * self.rate_value
