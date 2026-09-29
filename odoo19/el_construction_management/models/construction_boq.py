from .workflow_mixin import ConstructionWorkflowMixin
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class ConstructionBoq(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.boq'
    _description = 'Bill of Quantities'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('locked', 'Locked'),
        ('cancelled', 'Cancelled'),
    ], default='draft', tracking=True)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True, index=True)
    sub_project_id = fields.Many2one(
        'el_construction.sub.project', string='Sub Project', index=True,
    )
    company_id = fields.Many2one(
        'res.company', string='Company', required=True,
        default=lambda self: self.env.company, index=True,
    )
    work_type_id = fields.Many2one('el_construction.work.type', string='Work Type')
    work_sub_type_id = fields.Many2one(
        'el_construction.work.sub.type', string='Work Sub Type')

    length = fields.Float(string='Length', default=1.0)
    width = fields.Float(string='Width', default=1.0)
    height = fields.Float(string='Height', default=1.0)
    nos = fields.Float(string='Nos', default=1.0)
    quantity = fields.Float(string='Quantity', compute='_compute_quantity', store=True)

    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    description = fields.Text(string='Description')
    line_ids = fields.One2many('el_construction.boq.line', 'boq_id', string='BOQ Lines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.boq') or 'New'
            vals.setdefault('company_id', self.env.company.id)
        records = super().create(vals_list)
        records._check_consistency()
        return records

    def write(self, vals):
        for record in self:
            if record.state in ('approved', 'locked', 'cancelled') and set(vals) - {'message_follower_ids'}:
                raise UserError(_('Approved, locked, or cancelled BOQs cannot be modified.'))
        protected = {'project_id', 'sub_project_id', 'company_id', 'work_type_id', 'work_sub_type_id'}
        if protected.intersection(vals):
            for record in self:
                if record.line_ids.mapped('budget_line_ids').filtered(lambda bl: bl.budget_id.state in ('approved', 'done')):
                    raise UserError(_('A BOQ linked to an Approved or Done Budget cannot change its project, company or work classification.'))
        result = super().write(vals)
        self._check_consistency()
        return result

    @api.depends('length', 'width', 'height', 'nos')
    def _compute_quantity(self):
        for rec in self:
            rec.quantity = rec.length * rec.width * rec.height * rec.nos

    @api.depends('line_ids.amount')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.line_ids.mapped('amount'))

    @api.constrains('length', 'width', 'height', 'nos')
    def _check_dimensions(self):
        for rec in self:
            if min(rec.length, rec.width, rec.height, rec.nos) < 0:
                raise ValidationError(_('BOQ dimensions and Nos cannot be negative.'))

    def _check_consistency(self):
        for rec in self:
            if rec.project_id and rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('BOQ company must match the project company.'))
            if rec.sub_project_id and rec.sub_project_id.project_id != rec.project_id:
                raise ValidationError(_('Sub Project must belong to the selected Project.'))
            if rec.sub_project_id and rec.sub_project_id.company_id != rec.company_id:
                raise ValidationError(_('BOQ company must match the sub-project company.'))
            if rec.work_sub_type_id and rec.work_sub_type_id.work_type_id != rec.work_type_id:
                raise ValidationError(_('Work Sub Type must belong to the selected Work Type.'))


    def action_approve(self):
        for rec in self:
            if not rec.line_ids:
                raise UserError(_('A BOQ must contain at least one line before approval.'))
        return self._transition('approved', {'draft': {'approved'}}, manager=True)

    def action_lock(self):
        return self._transition('locked', {'approved': {'locked'}}, manager=True)

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}, 'approved': {'cancelled'}}, manager=True)

    def action_reset_draft(self):
        return self._transition('draft', {'cancelled': {'draft'}}, manager=True)

    def action_create_budget(self):
        self.ensure_one()
        """Create/update a budget using the BOQ line as the stable business key.

        The previous implementation matched by product only, which overwrote
        separate BOQ lines having the same product. We now preserve a one-to-one
        BOQ-line-to-budget-line mapping.
        """
        for boq in self:
            if not boq.line_ids:
                raise UserError(_('You cannot create a budget from an empty BOQ.'))

            budget = self.env['el_construction.budget'].search([
                ('project_id', '=', boq.project_id.id),
                ('sub_project_id', '=', boq.sub_project_id.id),
                ('company_id', '=', boq.company_id.id),
            ], limit=1)
            if not budget:
                budget = self.env['el_construction.budget'].create({
                    'project_id': boq.project_id.id,
                    'sub_project_id': boq.sub_project_id.id,
                    'company_id': boq.company_id.id,
                })
            budget._check_editable()

            BudgetLine = self.env['el_construction.budget.line']
            for line in boq.line_ids:
                budget_line = BudgetLine.search([
                    ('budget_id', '=', budget.id),
                    ('boq_line_id', '=', line.id),
                ], limit=1)
                vals = {
                    'budget_id': budget.id,
                    'boq_line_id': line.id,
                    'product_id': line.product_id.id,
                    'description': line.description or (line.product_id.display_name if line.product_id else _('BOQ Line')),
                    'quantity': line.quantity,
                    'uom_id': line.uom_id.id,
                    'unit_price': line.unit_price,
                    'planned_amount': line.amount,
                    'work_type_id': boq.work_type_id.id,
                    'work_sub_type_id': boq.work_sub_type_id.id,
                }
                if budget_line:
                    budget_line.write(vals)
                else:
                    BudgetLine.create(vals)

            return {
                'name': _('Budget'),
                'type': 'ir.actions.act_window',
                'res_model': 'el_construction.budget',
                'view_mode': 'form',
                'res_id': budget.id,
            }
