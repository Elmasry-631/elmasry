# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


# ============================================================
# Overtime Rule
# ============================================================
class HrAttendanceRuleOvertime(models.Model):
    _name = 'hr.attendance.rule.overtime'
    _description = 'HR Attendance Overtime Rule'
    _order = 'type, name'
    _rec_name = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    type = fields.Selection([
        ('working_day', 'Overtime On Working Days'),
        ('weekend', 'Overtime On Weekends'),
        ('public_holiday', 'Overtime On Public Holidays'),
    ], string='Type', required=True)
    apply_after_minutes = fields.Float(
        string='Apply After (minutes)',
        default=0.0,
        help="Overtime will be calculated only after this number of minutes.",
    )
    rate = fields.Float(
        string='Rate',
        default=1.0,
        required=True,
        help="Multiplier applied to the employee hourly rate. "
             "1.5 = 150% of the hourly rate.",
    )
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    _unique_type_company = models.Constraint(
        'unique(type, company_id)',
        'Only one overtime rule per type per company is allowed.',
    )


# ============================================================
# Lateness Rule
# ============================================================
class HrAttendanceRuleLateness(models.Model):
    _name = 'hr.attendance.rule.lateness'
    _description = 'HR Attendance Lateness Rule'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    unit = fields.Selection([
        ('hours', 'Hours'),
        ('minutes', 'Minutes'),
    ], string='Step Unit', default='hours', required=True,
        help="Unit used to configure the lateness step ranges.")
    tier_ids = fields.One2many(
        'hr.attendance.rule.lateness.tier',
        'lateness_id',
        string='Tiers',
        copy=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    def get_tier(self, occurrence):
        """Return the tier covering the ``occurrence``-th lateness.

        Each tier declares its own occurrence range, so a single rule can
        escalate: tier 1 = first lateness, tier 2 = second lateness, ...
        Tiers are matched on their range, not on their position in the list,
        so the order they were created in does not matter.
        """
        self.ensure_one()
        candidates = self.tier_ids.filtered(
            lambda t: t.occurrence_from <= occurrence <= t.occurrence_to
        )
        if not candidates:
            return self.env['hr.attendance.rule.lateness.tier']
        return min(candidates, key=lambda t: t.occurrence_from)

    def get_step(self, amount, occurrence=1):
        """Return the lateness step for ``amount`` at the given occurrence.

        ``amount`` is expressed in the rule ``unit`` (hours by default).
        """
        self.ensure_one()
        tier = self.get_tier(occurrence)
        if not tier:
            return self.env['hr.attendance.rule.lateness.step']
        if self.unit == 'hours':
            return tier.get_step_for_hours(amount)
        return tier.get_step_for_minutes(amount)

    def get_step_for_minutes(self, late_minutes, occurrence=1):
        """Same as :meth:`get_step` but the amount is given in minutes."""
        self.ensure_one()
        tier = self.get_tier(occurrence)
        if not tier:
            return self.env['hr.attendance.rule.lateness.step']
        return tier.get_step_for_minutes(late_minutes)

    def get_step_for_hours(self, late_hours, occurrence=1):
        """Same as :meth:`get_step` but the amount is given in hours."""
        return self.get_step_for_minutes((late_hours or 0.0) * 60.0, occurrence)


class HrAttendanceRuleLatenessTier(models.Model):
    """One repetition level of the lateness escalation.

    A tier owns its own steps, so configuring "2nd lateness" happens in its
    own record instead of being mixed in a single flat step list.
    """
    _name = 'hr.attendance.rule.lateness.tier'
    _description = 'HR Attendance Lateness Tier'
    _order = 'lateness_id, sequence, occurrence_from'
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        default=lambda self: _('Lateness Tier'),
    )
    lateness_id = fields.Many2one(
        'hr.attendance.rule.lateness',
        string='Lateness Rule',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sequence = fields.Integer(string='Sequence', default=10)
    occurrence_from = fields.Integer(
        string='Occurrences From',
        default=1,
        required=True,
        help="First repetition count this tier covers. "
             "1 = first lateness in the period.",
    )
    occurrence_to = fields.Integer(
        string='Occurrences To',
        default=1,
        required=True,
        help="Last repetition count this tier covers. Use a large number to "
             "cover this level and every repetition after it.",
    )
    step_ids = fields.One2many(
        'hr.attendance.rule.lateness.step',
        'tier_id',
        string='Lateness Steps',
        copy=True,
    )
    step_count = fields.Integer(
        string='Steps',
        compute='_compute_step_count',
    )
    unit = fields.Selection(
        related='lateness_id.unit',
        string='Step Unit',
    )
    company_id = fields.Many2one(
        'res.company',
        related='lateness_id.company_id',
        store=True,
    )

    @api.depends('step_ids')
    def _compute_step_count(self):
        for rec in self:
            rec.step_count = len(rec.step_ids)

    @api.constrains('occurrence_from', 'occurrence_to')
    def _check_occurrence_ranges(self):
        for rec in self:
            if rec.occurrence_to < rec.occurrence_from:
                raise UserError(_(
                    "Lateness tier '%s': 'Occurrences To' (%s) cannot be "
                    "smaller than 'Occurrences From' (%s)."
                ) % (rec.name, rec.occurrence_to, rec.occurrence_from))

    @api.constrains('lateness_id', 'occurrence_from', 'occurrence_to')
    def _check_no_overlap(self):
        for rec in self:
            others = rec.lateness_id.tier_ids - rec
            overlapping = others.filtered(
                lambda t: t.occurrence_from <= rec.occurrence_to
                and t.occurrence_to >= rec.occurrence_from
            )
            if overlapping:
                raise UserError(_(
                    "Lateness tiers must not overlap: '%s' conflicts with '%s'."
                ) % (rec.name, overlapping[0].name))

    def get_step_for_minutes(self, late_minutes):
        """Return the matching step for the given lateness minutes."""
        self.ensure_one()
        candidates = self.step_ids.filtered(
            lambda s: s.from_minutes <= late_minutes <= s.to_minutes
        )
        if not candidates:
            return self.env['hr.attendance.rule.lateness.step']
        return max(candidates, key=lambda s: s.from_minutes)

    def get_step_for_hours(self, late_hours):
        """Same as :meth:`get_step_for_minutes` but the amount is in hours."""
        return self.get_step_for_minutes((late_hours or 0.0) * 60.0)

    def action_open_rule(self):
        """Go back to the parent lateness rule."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lateness Rule'),
            'res_model': 'hr.attendance.rule.lateness',
            'res_id': self.lateness_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_tier(self):
        """Open this tier so its steps can be configured."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Lateness Tier'),
            'res_model': 'hr.attendance.rule.lateness.tier',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }


class HrAttendanceRuleLatenessStep(models.Model):
    _name = 'hr.attendance.rule.lateness.step'
    _description = 'HR Attendance Lateness Step'
    _order = 'from_minutes'

    tier_id = fields.Many2one(
        'hr.attendance.rule.lateness.tier',
        string='Lateness Tier',
        required=True,
        ondelete='cascade',
        index=True,
    )
    from_minutes = fields.Float(string='From (minutes)', required=True)
    to_minutes = fields.Float(
        string='To (minutes)',
        required=True,
        help="Use a large number for the upper bound of the last step.",
    )
    from_hours = fields.Float(
        string='From (hours)',
        compute='_compute_hour_range',
        inverse='_inverse_hour_range',
        store=True,
        readonly=False,
        help="Convenience view of 'From (minutes)' expressed in hours.",
    )
    to_hours = fields.Float(
        string='To (hours)',
        compute='_compute_hour_range',
        inverse='_inverse_hour_range',
        store=True,
        readonly=False,
        help="Convenience view of 'To (minutes)' expressed in hours.",
    )
    penalty_type = fields.Selection([
        ('rate', 'Rate (multiplier on hourly rate)'),
        ('hours', 'Hours (penalty hours)'),
        ('amount', 'Amount (fixed deduction)'),
    ], string='Penalty Type', required=True, default='rate')
    rate = fields.Float(
        string='Rate',
        default=1.0,
        help="Multiplier applied to initial rate. 1.5 = 150% of initial rate. "
             "Ignored when the penalty type is 'Hours' or 'Amount'.",
    )
    penalty_hours = fields.Float(
        string='Penalty (hours)',
        default=0.0,
        help="Fixed number of penalised hours charged when this step is hit. "
             "Used when the penalty type is 'Hours': a step of 0-15 minutes "
             "with 2 hours charges 2 paid hours, whatever the exact lateness.",
    )
    initial_rate = fields.Float(
        string='Initial Rate',
        default=1.0,
        help="Base rate the multiplier applies to (usually 1.0).",
    )
    amount = fields.Float(
        string='Amount',
        help="Fixed amount deducted when this step is hit.",
    )
    lateness_id = fields.Many2one(
        'hr.attendance.rule.lateness',
        related='tier_id.lateness_id',
        string='Lateness Rule',
        store=True,
        index=True,
    )
    company_id = fields.Many2one(
        'res.company',
        related='tier_id.company_id',
        store=True,
    )

    @api.depends('from_minutes', 'to_minutes')
    def _compute_hour_range(self):
        for rec in self:
            rec.from_hours = round((rec.from_minutes or 0.0) / 60.0, 4)
            rec.to_hours = round((rec.to_minutes or 0.0) / 60.0, 4)

    def _inverse_hour_range(self):
        """Write both bounds together so the range constraint sees them at once.

        A shared inverse is used for ``from_hours`` and ``to_hours`` so that
        editing the step in hours updates the stored minute range atomically,
        instead of triggering the range constraint on a half-updated record.
        """
        for rec in self:
            rec.with_context(lateness_hours_inverse=True).write({
                'from_minutes': (rec.from_hours or 0.0) * 60.0,
                'to_minutes': (rec.to_hours or 0.0) * 60.0,
            })

    @api.constrains('from_minutes', 'to_minutes')
    def _check_ranges(self):
        for rec in self:
            if rec.to_minutes < rec.from_minutes:
                raise UserError(_(
                    "Step 'To' (%s) cannot be smaller than 'From' (%s)."
                ) % (rec.to_minutes, rec.from_minutes))


# ============================================================
# Absence Rule
# ============================================================
class HrAttendanceRuleAbsence(models.Model):
    _name = 'hr.attendance.rule.absence'
    _description = 'HR Attendance Absence Rule'
    _order = 'name'

    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(string='Active', default=True)
    tier_ids = fields.One2many(
        'hr.attendance.rule.absence.tier',
        'absence_id',
        string='Tiers',
        copy=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    def get_tier(self, occurrence):
        """Return the tier covering the ``occurrence``-th absence.

        Each tier declares its own occurrence range, so a single rule can
        escalate: tier 1 = first absence, tier 2 = second absence, ...
        Tiers are matched on their range, not on their position in the list,
        so the order they were created in does not matter.
        """
        self.ensure_one()
        candidates = self.tier_ids.filtered(
            lambda t: t.occurrence_from <= occurrence <= t.occurrence_to
        )
        if not candidates:
            return self.env['hr.attendance.rule.absence.tier']
        return min(candidates, key=lambda t: t.occurrence_from)

    def get_step_for_days(self, absence_days, occurrence=1):
        """Return the absence step for ``absence_days`` at the given occurrence."""
        self.ensure_one()
        tier = self.get_tier(occurrence)
        if not tier:
            return self.env['hr.attendance.rule.absence.step']
        return tier.get_step_for_days(absence_days)


class HrAttendanceRuleAbsenceTier(models.Model):
    """One repetition level of the absence escalation.

    A tier owns its own steps, so configuring "2nd absence" happens in its own
    record instead of being mixed in a single flat step list.
    """
    _name = 'hr.attendance.rule.absence.tier'
    _description = 'HR Attendance Absence Tier'
    _order = 'absence_id, sequence, occurrence_from'
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        default=lambda self: _('Absence Tier'),
    )
    absence_id = fields.Many2one(
        'hr.attendance.rule.absence',
        string='Absence Rule',
        required=True,
        ondelete='cascade',
        index=True,
    )
    sequence = fields.Integer(string='Sequence', default=10)
    occurrence_from = fields.Integer(
        string='Absences From',
        default=1,
        required=True,
        help="First absence count this tier covers. 1 = first absence.",
    )
    occurrence_to = fields.Integer(
        string='Absences To',
        default=1,
        required=True,
        help="Last absence count this tier covers. Use a large number to "
             "cover this level and every absence after it.",
    )
    step_ids = fields.One2many(
        'hr.attendance.rule.absence.step',
        'tier_id',
        string='Absence Steps',
        copy=True,
    )
    step_count = fields.Integer(
        string='Steps',
        compute='_compute_step_count',
    )
    company_id = fields.Many2one(
        'res.company',
        related='absence_id.company_id',
        store=True,
    )

    @api.depends('step_ids')
    def _compute_step_count(self):
        for rec in self:
            rec.step_count = len(rec.step_ids)

    @api.constrains('occurrence_from', 'occurrence_to')
    def _check_occurrence_ranges(self):
        for rec in self:
            if rec.occurrence_to < rec.occurrence_from:
                raise UserError(_(
                    "Absence tier '%s': 'Absences To' (%s) cannot be smaller "
                    "than 'Absences From' (%s)."
                ) % (rec.name, rec.occurrence_to, rec.occurrence_from))

    @api.constrains('absence_id', 'occurrence_from', 'occurrence_to')
    def _check_no_overlap(self):
        for rec in self:
            others = rec.absence_id.tier_ids - rec
            overlapping = others.filtered(
                lambda t: t.occurrence_from <= rec.occurrence_to
                and t.occurrence_to >= rec.occurrence_from
            )
            if overlapping:
                raise UserError(_(
                    "Absence tiers must not overlap: '%s' conflicts with '%s'."
                ) % (rec.name, overlapping[0].name))

    def get_step_for_days(self, absence_days):
        """Return the matching step for the given absence days."""
        self.ensure_one()
        candidates = self.step_ids.filtered(
            lambda s: s.from_days <= absence_days <= s.to_days
        )
        if not candidates:
            return self.env['hr.attendance.rule.absence.step']
        return max(candidates, key=lambda s: s.from_days)

    def action_open_rule(self):
        """Go back to the parent absence rule."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Absence Rule'),
            'res_model': 'hr.attendance.rule.absence',
            'res_id': self.absence_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_open_tier(self):
        """Open this tier so its steps can be configured."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Absence Tier'),
            'res_model': 'hr.attendance.rule.absence.tier',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }


class HrAttendanceRuleAbsenceStep(models.Model):
    _name = 'hr.attendance.rule.absence.step'
    _description = 'HR Attendance Absence Step'
    _order = 'from_days'

    tier_id = fields.Many2one(
        'hr.attendance.rule.absence.tier',
        string='Absence Tier',
        required=True,
        ondelete='cascade',
        index=True,
    )
    from_days = fields.Integer(string='From (days)', required=True, default=1)
    to_days = fields.Integer(
        string='To (days)',
        required=True,
        default=9999,
        help="Use a large number for the upper bound of the last step.",
    )
    penalty_type = fields.Selection([
        ('rate', 'Rate (multiplier on daily wage)'),
        ('days', 'Days (fixed amount of days)'),
    ], string='Penalty Type', required=True, default='rate')
    rate = fields.Float(
        string='Rate',
        default=1.0,
        help="Multiplier applied to the daily wage. 1.5 = 150% deduction. "
             "Use it to escalate: 2.0 for the first absence, 3.0 when repeated.",
    )
    deduction_days = fields.Float(
        string='Deduction (days)',
        default=1.0,
        help="Number of days deducted when the penalty type is 'Days'.",
    )
    absence_id = fields.Many2one(
        'hr.attendance.rule.absence',
        related='tier_id.absence_id',
        string='Absence Rule',
        store=True,
        index=True,
    )
    company_id = fields.Many2one(
        'res.company',
        related='tier_id.company_id',
        store=True,
    )

    @api.constrains('from_days', 'to_days')
    def _check_ranges(self):
        for rec in self:
            if rec.to_days < rec.from_days:
                raise UserError(_(
                    "Step 'To' (%s) cannot be smaller than 'From' (%s)."
                ) % (rec.to_days, rec.from_days))

    def compute_deduction_days(self, absence_days):
        """Return the number of days to deduct for the given absence days."""
        self.ensure_one()
        return self.deduction_days or absence_days