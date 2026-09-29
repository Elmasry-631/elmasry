from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin


class ConstructionProgressBillingControls(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.progress.billing'

    commercial_status = fields.Selection([('draft','Draft'),('certified','Certified'),('invoiced','Invoiced'),('paid','Paid'),('cancelled','Cancelled')], default='draft', tracking=True)
    retention_percent = fields.Float(string='Retention %', default=0.0)
    advance_recovery = fields.Monetary(string='Advance Recovery', currency_field='currency_id')
    other_deductions = fields.Monetary(string='Other Deductions', currency_field='currency_id')
    net_commercial_amount = fields.Monetary(compute='_compute_commercial_amounts', store=True, currency_field='currency_id')
    retention_amount = fields.Monetary(compute='_compute_commercial_amounts', store=True, currency_field='currency_id')
    currency_id = fields.Many2one(related='company_id.currency_id', store=True)

    @api.depends('total_amount','retention_percent','advance_recovery','other_deductions')
    def _compute_commercial_amounts(self):
        for rec in self:
            rec.retention_amount = rec.total_amount * rec.retention_percent / 100.0
            rec.net_commercial_amount = max(0.0, rec.total_amount - rec.retention_amount - rec.advance_recovery - rec.other_deductions)

    @api.constrains('retention_percent','advance_recovery','other_deductions')
    def _check_commercial(self):
        for rec in self:
            if not 0 <= rec.retention_percent <= 100: raise ValidationError(_('Retention percentage must be between 0 and 100.'))
            if rec.advance_recovery < 0 or rec.other_deductions < 0: raise ValidationError(_('Commercial deductions cannot be negative.'))

class ConstructionRaBillingLineControls(models.Model):
    _inherit = 'el_construction.ra.billing.line'

    previous_quantity = fields.Float(compute='_compute_cumulative_controls')
    current_quantity = fields.Float(compute='_compute_cumulative_controls')
    cumulative_quantity = fields.Float(compute='_compute_cumulative_controls')
    remaining_quantity = fields.Float(compute='_compute_cumulative_controls')

    @api.depends('quantity', 'budget_line_id', 'ra_billing_id.state', 'ra_billing_id.subcontract_id')
    def _compute_cumulative_controls(self):
        for line in self:
            previous = 0.0
            if line.ra_billing_id and line.budget_line_id:
                approved_lines = self.search([
                    ('budget_line_id', '=', line.budget_line_id.id),
                    ('ra_billing_id.state', '=', 'approved'),
                    ('id', '!=', line.id),
                ])
                previous = sum(approved_lines.mapped('quantity'))
            line.previous_quantity = previous
            line.current_quantity = line.quantity
            line.cumulative_quantity = previous + line.quantity
            line.remaining_quantity = max(0.0, line.budget_line_id.quantity - line.cumulative_quantity) if line.budget_line_id else 0.0

    @api.constrains('quantity', 'budget_line_id')
    def _check_cumulative_quantity(self):
        for line in self:
            if line.budget_line_id and line.cumulative_quantity > line.budget_line_id.quantity:
                raise ValidationError(_('Cumulative RA quantity cannot exceed the budget quantity.'))

class ConstructionRaCommercialControls(ConstructionWorkflowMixin, models.Model):
    _inherit = 'el_construction.ra.billing'

    retention_percent = fields.Float(string='Retention %', default=0.0)
    retention_amount = fields.Float(compute='_compute_ra_commercial', store=True)
    advance_recovery = fields.Float(string='Advance Recovery', default=0.0)
    other_deductions = fields.Float(string='Other Deductions', default=0.0)
    net_certified_amount = fields.Float(compute='_compute_ra_commercial', store=True)

    @api.depends('total_amount','retention_percent','advance_recovery','other_deductions')
    def _compute_ra_commercial(self):
        for rec in self:
            rec.retention_amount = rec.total_amount * rec.retention_percent / 100.0
            rec.net_certified_amount = max(0.0, rec.total_amount - rec.retention_amount - rec.advance_recovery - rec.other_deductions)

    @api.constrains('retention_percent','advance_recovery','other_deductions')
    def _check_ra_commercial(self):
        for rec in self:
            if not 0 <= rec.retention_percent <= 100: raise ValidationError(_('Retention percentage must be between 0 and 100.'))
            if rec.advance_recovery < 0 or rec.other_deductions < 0: raise ValidationError(_('RA deductions cannot be negative.'))
