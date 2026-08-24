from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreditApprovalWizard(models.TransientModel):
    _name = 'credit.approval.wizard'
    _description = 'Credit Approval Wizard'

    sale_order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale Order',
        required=True,
        readonly=True,
    )

    request_id = fields.Many2one(
        comodel_name='credit.approval.request',
        string='Approval Request',
        required=True,
        readonly=True,
    )

    request_state = fields.Selection(
        related='request_id.state',
        string='Request State',
        readonly=True,
    )

    customer_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer',
        readonly=True,
    )

    credit_limit = fields.Float(
        string='Credit Limit',
        readonly=True,
    )

    credit_used = fields.Float(
        string='Credit Used',
        readonly=True,
    )

    order_amount = fields.Monetary(
        string='Order Amount',
        readonly=True,
        currency_field='currency_id',
    )

    exceeded_by = fields.Float(
        string='Exceeded By',
        readonly=True,
    )

    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        readonly=True,
    )

    rejection_reason_id = fields.Many2one(
        comodel_name='credit.rejection.reason',
        string='Rejection Reason',
        domain="[('active', '=', True)]",
    )

    rejection_notes = fields.Text(
        string='Additional Notes',
    )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')

        if active_model == 'sale.order' and active_id:
            so = self.env['sale.order'].browse(active_id)
            request = self.env['credit.approval.request'].search([
                ('sale_order_id', '=', so.id),
                ('state', 'in', ('draft', 'submitted')),
            ], limit=1)
            if request:
                defaults.update({
                    'sale_order_id': so.id,
                    'request_id': request.id,
                    'customer_id': request.partner_id.id,
                    'credit_limit': request.credit_limit,
                    'credit_used': request.credit_used,
                    'order_amount': request.order_amount,
                    'exceeded_by': request.exceeded_by,
                    'currency_id': request.currency_id.id,
                })
        return defaults

    def action_approve(self):
        self.ensure_one()
        if self.request_id.state != 'submitted':
            raise UserError(_('This request is no longer pending approval.'))
        self.request_id.with_user(self.env.user).action_approve()
        return {'type': 'ir.actions.act_window_close'}

    def action_reject(self):
        self.ensure_one()
        if self.request_id.state != 'submitted':
            raise UserError(_('This request is no longer pending approval.'))
        if not self.rejection_reason_id:
            raise UserError(_('Please select a rejection reason.'))
        self.request_id.with_user(self.env.user).write({
            'rejection_reason_id': self.rejection_reason_id.id,
            'rejection_notes': self.rejection_notes,
        })
        self.request_id.with_user(self.env.user).action_reject()
        return {'type': 'ir.actions.act_window_close'}
