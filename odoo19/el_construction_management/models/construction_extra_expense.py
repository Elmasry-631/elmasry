from .workflow_mixin import ConstructionWorkflowMixin, _WORKFLOW_TOKEN, _WORKFLOW_CREATE_CONTEXT_KEY
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionExtraExpense(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.extra.expense'
    _description = 'Construction Extra Expense'
    _inherit = ['mail.thread']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True)
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    date = fields.Date(string='Date', default=fields.Date.context_today)
    description = fields.Text(string='Description')
    expense_type = fields.Selection([
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('labour', 'Labour'),
        ('transport', 'Transport'),
        ('permit', 'Permit/Fees'),
        ('other', 'Other'),
    ], string='Expense Type', default='other')

    product_id = fields.Many2one('product.product', string='Product')
    budget_line_id = fields.Many2one(
        'el_construction.budget.line', string='Budget Line', ondelete='set null', index=True,
        # domain removed - Odoo 19 toPyValue(undefined) crashes on conditional domains (py_utils.js:47 "Invalid type")
        # filtering is handled in _onchange_budget_line_id and _check_budget_line_consistency
    )
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Float(string='Unit Price')
    amount = fields.Float(string='Amount', compute='_compute_amount', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    approved_by = fields.Many2one('res.users', string='Approved By')
    source_move_line_id = fields.Many2one(
        'account.move.line', string='Source Vendor Bill Line', index=True, copy=False,
        ondelete='restrict', readonly=True,
    )
    _source_move_line_unique = models.Constraint(
        'unique(source_move_line_id)',
        'A vendor bill line can create only one construction Extra Expense.',
    )

    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.extra.expense') or 'New'
            # A posted vendor-bill line is already an accounting approval source;
            # do not force the accountant through a second Construction Manager step.
            if vals.get('source_move_line_id'):
                vals['state'] = 'approved'
                vals['approved_by'] = self.env.user.id
        records = self.browse()
        for vals in vals_list:
            creator = self.with_context(**{_WORKFLOW_CREATE_CONTEXT_KEY: _WORKFLOW_TOKEN}) if vals.get('source_move_line_id') else self
            records |= super(ConstructionExtraExpense, creator).create([vals])
        return records

    @api.constrains('project_id', 'sub_project_id', 'budget_line_id', 'company_id')
    def _check_budget_line_consistency(self):
        for rec in self:
            if rec.sub_project_id and rec.sub_project_id.project_id != rec.project_id:
                raise ValidationError(_('Sub Project must belong to the selected Project.'))
            if rec.budget_line_id:
                if rec.budget_line_id.project_id != rec.project_id or rec.budget_line_id.sub_project_id != rec.sub_project_id:
                    raise ValidationError(_('Budget Line must belong to the same Project and Sub Project.'))
                if rec.budget_line_id.company_id != rec.company_id:
                    raise ValidationError(_('Budget Line company must match the expense company.'))
                if rec.product_id and rec.budget_line_id.product_id and rec.product_id != rec.budget_line_id.product_id:
                    raise ValidationError(_('Expense Product must match the Budget Line Product.'))

    @api.onchange('project_id', 'sub_project_id', 'product_id')
    def _onchange_budget_line_id(self):
        for rec in self:
            if not rec.project_id:
                rec.budget_line_id = False
                continue
            domain = [('project_id', '=', rec.project_id.id)]
            if rec.sub_project_id:
                domain.append(('sub_project_id', '=', rec.sub_project_id.id))
            if rec.product_id:
                domain.append(('product_id', '=', rec.product_id.id))
            candidates = self.env['el_construction.budget.line'].search(domain)
            rec.budget_line_id = candidates[:1] if len(candidates) == 1 else False

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.unit_price

    @api.constrains('quantity', 'unit_price')
    def _check_values(self):
        for rec in self:
            if rec.quantity <= 0:
                raise ValidationError(_('Expense quantity must be greater than zero.'))
            if rec.unit_price < 0:
                raise ValidationError(_('Expense unit price cannot be negative.'))

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def action_confirm(self):
        return self._transition('confirmed', {'draft': {'confirmed'}})

    def action_approve(self):
        self._require_manager()
        return self._transition('approved', {'confirmed': {'approved'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}, 'confirmed': {'cancelled'}}, manager=True)

    def action_reset_draft(self):
        return self._transition('draft', {'cancelled': {'draft'}}, manager=True)
