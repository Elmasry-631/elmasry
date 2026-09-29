from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionRaBilling(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.ra.billing'
    _description = 'RA Billing (Running Account)'
    _inherit = ['mail.thread']
    _order = 'id desc'
    _unique_subcontract_billing_no = models.Constraint(
        'UNIQUE(subcontract_id, billing_no)',
        'Billing No. must be unique per subcontract.',
    )

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    subcontract_id = fields.Many2one('el_construction.subcontract', string='Subcontract', required=True)
    project_id = fields.Many2one('el_construction.project', string='Project',
                                  related='subcontract_id.project_id', store=True, index=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project',
                                     related='subcontract_id.sub_project_id', store=True, index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 related='subcontract_id.company_id', store=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Subcontractor',
                                  related='subcontract_id.partner_id', store=True)
    date = fields.Date(string='Date', default=fields.Date.context_today)
    billing_no = fields.Integer(string='Billing No.')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)

    line_ids = fields.One2many('el_construction.ra.billing.line', 'ra_billing_id', string='Lines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total', store=True)
    previous_amount = fields.Float(string='Previous Billing Amount', compute='_compute_current')
    current_amount = fields.Float(string='Current Amount', compute='_compute_current')
    cumulative_amount = fields.Float(string='Cumulative Certified', compute='_compute_cumulative')
    remaining_contract = fields.Float(string='Remaining Contract', compute='_compute_cumulative')
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        subcontract_ids = sorted({v.get('subcontract_id') for v in vals_list if v.get('subcontract_id')})
        if subcontract_ids:
            self._lock_records(self.env['el_construction.subcontract'].browse(subcontract_ids))
        next_numbers = {}
        for subcontract_id in subcontract_ids:
            last = self.search([('subcontract_id', '=', subcontract_id)], order='billing_no desc', limit=1)
            next_numbers[subcontract_id] = (last.billing_no or 0) + 1
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.ra.billing') or 'New'
            if not vals.get('billing_no') and vals.get('subcontract_id'):
                subcontract_id = vals['subcontract_id']
                vals['billing_no'] = next_numbers[subcontract_id]
                next_numbers[subcontract_id] += 1
        return super().create(vals_list)

    @api.depends('line_ids.amount')
    def _compute_total(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('amount'))

    @api.depends('subcontract_id', 'date', 'total_amount')
    def _compute_current(self):
        subcontract_ids = self.mapped('subcontract_id').ids
        approved_totals = {}
        if subcontract_ids:
            grouped = self.read_group(
                [('subcontract_id', 'in', subcontract_ids), ('state', '=', 'approved')],
                ['subcontract_id', 'total_amount:sum'], ['subcontract_id'],
            )
            approved_totals = {g['subcontract_id'][0]: g['total_amount'] for g in grouped if g.get('subcontract_id')}
        for rec in self:
            rec.previous_amount = approved_totals.get(rec.subcontract_id.id, 0.0) - (rec.total_amount if rec.state == 'approved' else 0.0)
            rec.current_amount = rec.total_amount

    @api.constrains('subcontract_id', 'date')
    def _check_ra_context(self):
        for rec in self:
            if rec.subcontract_id and rec.subcontract_id.company_id != rec.subcontract_id.project_id.company_id:
                raise ValidationError(_('Subcontract company must match its Project company.'))

    @api.depends('subcontract_id', 'total_amount', 'state')
    def _compute_cumulative(self):
        subcontract_ids = self.mapped('subcontract_id').ids
        approved_totals = {}
        if subcontract_ids:
            grouped = self.read_group(
                [('subcontract_id', 'in', subcontract_ids), ('state', '=', 'approved')],
                ['subcontract_id', 'total_amount:sum'], ['subcontract_id'],
            )
            approved_totals = {g['subcontract_id'][0]: g['total_amount'] for g in grouped if g.get('subcontract_id')}
        for rec in self:
            approved = approved_totals.get(rec.subcontract_id.id, 0.0)
            rec.cumulative_amount = approved + (rec.total_amount if rec.state != 'approved' else 0.0)
            rec.remaining_contract = (rec.subcontract_id.contract_amount - rec.cumulative_amount) if rec.subcontract_id else 0.0

    def _check_ceiling(self):
        subcontract_ids = self.mapped('subcontract_id').ids
        approved_totals = {}
        if subcontract_ids:
            self._lock_records(self.env['el_construction.subcontract'].browse(subcontract_ids))
            self.mapped('subcontract_id').invalidate_recordset(['contract_amount'])
            grouped = self.read_group(
                [('subcontract_id', 'in', subcontract_ids), ('state', '=', 'approved')],
                ['subcontract_id', 'total_amount:sum'], ['subcontract_id'],
            )
            approved_totals = {g['subcontract_id'][0]: g['total_amount'] for g in grouped if g.get('subcontract_id')}
        for rec in self:
            if rec.total_amount < 0:
                raise ValidationError(_('RA Billing amount cannot be negative.'))
            approved_other = approved_totals.get(rec.subcontract_id.id, 0.0) - (rec.total_amount if rec.state == 'approved' else 0.0)
            if rec.subcontract_id and approved_other + rec.total_amount > rec.subcontract_id.contract_amount:
                raise ValidationError(_('Cumulative RA Billing cannot exceed the subcontract contract amount.'))

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        if any(k in vals for k in ('subcontract_id', 'line_ids')):
            for record in self:
                if record.state not in ('draft', 'rejected'):
                    raise UserError(_('Approved or submitted RA Billings cannot be changed.'))
        return super().write(vals)

    def action_submit(self):
        if not self.line_ids:
            raise UserError(_('RA Billing must contain at least one line.'))
        self._check_ceiling()
        return self._transition('submitted', {'draft': {'submitted'}})

    def action_approve(self):
        self._check_ceiling()
        return self._transition('approved', {'submitted': {'approved'}}, manager=True)

    def action_reject(self):
        return self._transition('rejected', {'submitted': {'rejected'}}, manager=True)

    def action_reset_draft(self):
        return self._transition('draft', {'rejected': {'draft'}}, manager=True)

class ConstructionRaBillingLine(models.Model):
    _name = 'el_construction.ra.billing.line'
    _description = 'RA Billing Line'

    ra_billing_id = fields.Many2one('el_construction.ra.billing', string='RA Billing', required=True, ondelete='cascade')
    description = fields.Char(string='Description', required=True)
    budget_line_id = fields.Many2one(
        'el_construction.budget.line', string='Budget Line', ondelete='set null', index=True
    )
    quantity = fields.Float(string='Quantity', default=1.0)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    rate = fields.Float(string='Rate')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)
    completion_percentage = fields.Float(string='Completion (%)', default=100.0)

    @api.model_create_multi
    def create(self, vals_list):
        billings = self.env['el_construction.ra.billing'].browse([v.get('ra_billing_id') for v in vals_list if v.get('ra_billing_id')])
        if any(billing.state not in ('draft', 'rejected') for billing in billings):
            raise UserError(_('RA Billing lines can only be created while the billing is Draft or Rejected.'))
        return super().create(vals_list)

    @api.constrains('ra_billing_id', 'budget_line_id', 'completion_percentage', 'quantity', 'rate')
    def _check_line_values(self):
        for line in self:
            if not line.ra_billing_id:
                continue
            if not 0.0 <= line.completion_percentage <= 100.0:
                raise ValidationError(_('Completion percentage must be between 0 and 100.'))
            if line.quantity <= 0:
                raise ValidationError(_('RA Billing quantity must be greater than zero.'))
            if line.rate < 0:
                raise ValidationError(_('RA Billing rate cannot be negative.'))
            if line.budget_line_id:
                budget = line.budget_line_id.budget_id
                billing = line.ra_billing_id
                if budget.project_id != billing.project_id or budget.sub_project_id != billing.sub_project_id:
                    raise ValidationError(_('Budget Line must belong to the RA Billing Project and Sub Project.'))
                if budget.company_id != billing.company_id:
                    raise ValidationError(_('Budget Line company must match the RA Billing company.'))

    @api.depends('quantity', 'rate', 'completion_percentage')
    def _compute_amount(self):
        for line in self:
            line.amount = line.quantity * line.rate * line.completion_percentage / 100.0

    def write(self, vals):
        for line in self:
            if line.ra_billing_id.state not in ('draft', 'rejected'):
                raise UserError(_('RA Billing lines can only be changed while the billing is Draft or Rejected.'))
        return super().write(vals)

    def unlink(self):
        for line in self:
            if line.ra_billing_id.state not in ('draft', 'rejected'):
                raise UserError(_('RA Billing lines can only be deleted while the billing is Draft or Rejected.'))
        return super().unlink()
