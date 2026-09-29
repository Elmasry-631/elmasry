import secrets

from odoo import api, fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin

_APPROVAL_TOKEN = secrets.token_urlsafe(32)


class ConstructionVariationOrder(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.variation.order'
    _description = 'Construction Variation Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Reference', readonly=True, default='New', copy=False, tracking=True)
    project_id = fields.Many2one('el_construction.project', required=True, index=True, ondelete='restrict')
    sub_project_id = fields.Many2one('el_construction.sub.project', index=True, ondelete='restrict')
    company_id = fields.Many2one('res.company', related='project_id.company_id', store=True, index=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True)
    date = fields.Date(default=fields.Date.context_today, required=True)
    reason = fields.Text(required=True)
    description = fields.Text()
    state = fields.Selection([('draft','Draft'),('submitted','Submitted'),('approved','Approved'),('rejected','Rejected'),('cancelled','Cancelled')], default='draft', tracking=True)
    line_ids = fields.One2many('el_construction.variation.order.line', 'variation_id')
    amount = fields.Monetary(compute='_compute_amount', store=True, currency_field='currency_id')
    approved_by = fields.Many2one('res.users', readonly=True)
    approved_on = fields.Datetime(readonly=True)
    approval_line_ids = fields.One2many('el_construction.variation.approval', 'variation_id', string='Approval History', readonly=True, copy=False)

    @api.depends('line_ids.amount')
    def _compute_amount(self):
        for rec in self:
            rec.amount = sum(rec.line_ids.mapped('amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('el_construction.variation.order') or 'New'
        return super().create(vals_list)

    def write(self, vals):
        for rec in self:
            if rec.state in ('approved', 'rejected', 'cancelled') and set(vals) - {'message_follower_ids'}:
                raise UserError(_('Finalized Variation Orders cannot be modified.'))
        return super().write(vals)

    def action_submit(self):
        if any(not r.line_ids for r in self):
            raise UserError(_('A Variation Order must contain at least one line.'))
        return self._transition('submitted', {'draft': {'submitted'}})

    def action_approve(self):
        Approval = self.env['el_construction.approval.matrix']
        ApprovalLine = self.env['el_construction.variation.approval']
        for rec in self:
            self.env.cr.execute('SELECT id FROM el_construction_variation_order WHERE id = %s FOR UPDATE', [rec.id])
            rec.invalidate_recordset()
            if rec.state != 'submitted':
                raise UserError(_('Only Submitted Variation Orders can be approved.'))
            if rec.create_uid == self.env.user:
                raise UserError(_('Separation of duties: the user who created a Variation Order cannot approve it.'))
            if not rec.reason or not rec.reason.strip():
                raise UserError(_('Variation reason is required.'))
            matrix = Approval.get_approval_matrix('el_construction.variation.order', rec.amount, rec.company_id)
            if matrix:
                if self.env.user not in matrix.approver_ids:
                    raise UserError(_('You are not authorized to approve this Variation Order under the configured Approval Matrix.'))
                if ApprovalLine.search_count([('variation_id', '=', rec.id), ('user_id', '=', self.env.user.id)]):
                    raise UserError(_('You have already approved this Variation Order.'))
                ApprovalLine.sudo().with_context(_construction_approval_token=_APPROVAL_TOKEN).create({
                    'variation_id': rec.id,
                    'matrix_id': matrix.id,
                    'user_id': self.env.user.id,
                    'approved_on': fields.Datetime.now(),
                })
                approvals = ApprovalLine.search_count([('variation_id', '=', rec.id)])
                if approvals < matrix.required_approvals:
                    rec.message_post(body=_('Approval recorded: %s/%s approvals received.') % (approvals, matrix.required_approvals))
                    continue
                rec.write({'approved_by': self.env.user.id, 'approved_on': fields.Datetime.now()})
                rec._transition('approved', {'submitted': {'approved'}})
            else:
                if not self.env.user.has_group('el_construction_management.group_construction_manager'):
                    raise UserError(_('Only Construction Managers can approve Variation Orders when no Approval Matrix is configured.'))
                rec.write({'approved_by': self.env.user.id, 'approved_on': fields.Datetime.now()})
                rec._transition('approved', {'submitted': {'approved'}}, manager=True)
        return True

    def action_reject(self):
        return self._transition('rejected', {'submitted': {'rejected'}})

    def action_cancel(self):
        return self._transition('cancelled', {'draft': {'cancelled'}, 'submitted': {'cancelled'}})


class ConstructionVariationApproval(models.Model):
    _name = 'el_construction.variation.approval'
    _description = 'Variation Order Approval'
    _order = 'id desc'

    variation_id = fields.Many2one('el_construction.variation.order', required=True, ondelete='cascade')
    matrix_id = fields.Many2one('el_construction.approval.matrix', required=True)
    user_id = fields.Many2one('res.users', required=True)
    approved_on = fields.Datetime(readonly=True)

    _variation_approval_unique = models.Constraint(
        'unique(variation_id, user_id)',
        'A user can approve a Variation Order only once.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        if self.env.context.get('_construction_approval_token') != _APPROVAL_TOKEN:
            raise AccessError(_('Variation approvals can only be created through the Variation Order approval action.'))
        records = super().create(vals_list)
        for rec in records:
            if rec.variation_id.state != 'submitted':
                raise ValidationError(_('Approval can only be recorded while the Variation Order is Submitted.'))
            if rec.user_id not in rec.variation_id.company_id.user_ids:
                raise ValidationError(_('Approver must belong to the Variation Order company.'))
        return records

    def write(self, vals):
        if self.env.context.get('_construction_approval_token') != _APPROVAL_TOKEN:
            raise AccessError(_('Variation approval records are immutable. Use the Variation Order approval action.'))
        return super().write(vals)

    def unlink(self):
        raise AccessError(_('Variation approval records cannot be deleted.'))

    @api.constrains('variation_id')
    def _check_unique(self):
        for rec in self:
            count = self.search_count([('variation_id', '=', rec.variation_id.id), ('user_id', '=', rec.user_id.id)])
            if count > 1:
                raise ValidationError(_('You can only approve a Variation Order once.'))


class ConstructionVariationOrderLine(models.Model):
    _name = 'el_construction.variation.order.line'
    _description = 'Variation Order Line'
    _order = 'id'

    variation_id = fields.Many2one('el_construction.variation.order', required=True, ondelete='cascade')
    boq_line_id = fields.Many2one('el_construction.boq.line', required=True, ondelete='restrict')
    product_id = fields.Many2one('product.product', related='boq_line_id.product_id', store=True)
    description = fields.Char(related='boq_line_id.description', store=True)
    quantity = fields.Float(default=1.0)
    unit_price = fields.Float(default=0.0)
    amount = fields.Float(compute='_compute_amount', store=True)

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.unit_price

    @api.constrains('quantity', 'unit_price', 'variation_id', 'boq_line_id')
    def _check_values(self):
        for rec in self:
            if rec.quantity == 0:
                raise ValidationError(_('Variation quantity cannot be zero.'))
            if rec.boq_line_id and rec.variation_id and rec.boq_line_id.boq_id.project_id != rec.variation_id.project_id:
                raise ValidationError(_('Variation BOQ Line must belong to the same Project.'))

    def write(self, vals):
        for rec in self:
            if rec.variation_id.state != 'draft':
                raise UserError(_('Variation Order lines can only be changed while the Variation Order is Draft.'))
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        if any(r.variation_id.state != 'draft' for r in records):
            raise UserError(_('Variation Order lines can only be created while the Variation Order is Draft.'))
        return records

    def unlink(self):
        if any(r.variation_id.state != 'draft' for r in self):
            raise UserError(_('Variation Order lines can only be deleted while the Variation Order is Draft.'))
        return super().unlink()
