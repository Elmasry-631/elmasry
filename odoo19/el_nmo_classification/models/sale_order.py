from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_payment_type = fields.Selection([
        ('cash', 'Cash'),
        ('credit', 'Credit'),
    ], string='Payment Type',
       related='partner_id.commercial_partner_id.payment_type',
       help='Customer payment type.')

    partner_classification_id = fields.Many2one(
        comodel_name='customer.classification',
        string='Customer Classification',
        related='partner_id.commercial_partner_id.classification_id',
        store=True,
        help='Classification of the customer (stored for search/group).',
    )

    partner_effective_credit_limit = fields.Float(
        string='Effective Credit Limit',
        digits=(16, 2),
        related='partner_id.commercial_partner_id.effective_credit_limit',
        help='Customer effective credit limit at order time.',
    )

    partner_credit_policy = fields.Selection(
        selection=[
            ('block', 'Block Sale'),
            ('warning', 'Warning Only'),
        ],
        string='Credit Policy',
        related='partner_id.commercial_partner_id.credit_policy',
        help='Credit policy from the customer classification.',
    )

    partner_outstanding = fields.Monetary(
        string='Outstanding',
        related='partner_id.commercial_partner_id.credit',
        currency_field='currency_id',
        help='Current outstanding balance of the customer.',
    )

    partner_remaining_credit = fields.Float(
        string='Remaining Credit',
        digits=(16, 2),
        compute='_compute_partner_remaining_credit',
        help='Available credit remaining (credit limit - outstanding).',
    )

    payment_gateway_id = fields.Many2one(
        'sale.payment.gateway', string='Payment Gateway'
    )

    @api.depends('partner_effective_credit_limit', 'partner_outstanding')
    def _compute_partner_remaining_credit(self):
        for order in self:
            remaining = order.partner_effective_credit_limit - order.partner_outstanding
            order.partner_remaining_credit = max(remaining, 0.0)

    @api.onchange('partner_id')
    def _onchange_partner_id_payment_gateway(self):
        if self.partner_id:
            self.payment_gateway_id = self.partner_id.payment_gateway_id

    def action_confirm(self):
        if not self.env.context.get('credit_approval_bypass'):
            warning_msg = self._check_classification_credit()
        else:
            warning_msg = None
        result = super().action_confirm()
        if warning_msg:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Credit Limit Warning'),
                    'message': warning_msg,
                    'type': 'warning',
                    'sticky': True,
                    'next': {'type': 'ir.actions.act_window_close'},
                },
            }
        return result

    def _check_classification_credit(self):
        warning_msg = ''
        for order in self:
            partner = order.partner_id.commercial_partner_id.sudo()

            if partner.payment_type == 'cash':
                continue

            if not partner.classification_id:
                continue

            effective_limit = partner.effective_credit_limit
            if effective_limit <= 0:
                continue

            projected_total = partner.credit + order.amount_total
            if projected_total <= effective_limit:
                continue

            exceeded_by = projected_total - effective_limit
            policy = partner.credit_policy

            msg_parts = [
                f"<b>Customer:</b> {partner.display_name}",
                f"<b>Classification:</b> {partner.classification_id.display_name}",
                f"<b>Credit Limit:</b> {effective_limit:,.2f}",
                f"<b>Current Outstanding:</b> {partner.credit:,.2f}",
                f"<b>This Order:</b> {order.amount_total:,.2f}",
                f"<b>Projected Total:</b> {projected_total:,.2f}",
                f"<b>Exceeded By:</b> {exceeded_by:,.2f}",
                f"<b>Credit Policy:</b> {'Block Sale' if policy == 'block' else 'Warning Only'}",
            ]
            body = '<br/>'.join(msg_parts)
            html_body = (
                f"<p><b>Credit Limit {'Exceeded!' if policy == 'block' else 'Warning'}</b></p>"
                f"{body}"
            )

            order.message_post(body=html_body, subject=_('Credit Limit Warning'))

            if policy == 'block':
                raise UserError(
                    _(
                        "Credit Limit Exceeded!\n\n"
                        "Customer: %s\n"
                        "Classification: %s\n"
                        "Credit Limit: %s\n"
                        "Current Outstanding: %s\n"
                        "This Order: %s\n"
                        "Projected Total: %s\n"
                        "Exceeded By: %s\n\n"
                        "Credit Policy: Block Sale.\n"
                        "Contact credit management or change the customer's classification."
                    ) % (
                        partner.display_name,
                        partner.classification_id.display_name,
                        f"{effective_limit:,.2f}",
                        f"{partner.credit:,.2f}",
                        f"{order.amount_total:,.2f}",
                        f"{projected_total:,.2f}",
                        f"{exceeded_by:,.2f}",
                    )
                )

            warning_msg += (
                f"\u26a0\ufe0f {partner.display_name}: Credit limit exceeded by {exceeded_by:,.2f}.\n"
            )

        return warning_msg or None
