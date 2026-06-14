from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """
    Extension of sale.order to display customer classification info
    and enforce credit check on confirmation.

    Injection Point: action_confirm() — pre-hook before super().
    """

    _inherit = 'sale.order'

    # ── Related Fields (Display + Search) ────────────────────────

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

    # ── Override: Credit Check on Confirm ────────────────────────

    def action_confirm(self):
        """
        Pre-hook: check classification credit limit before confirming.
        - block → raises UserError, order stays draft
        - warning → posts to chatter, confirms, returns notification
        """
        warning_msg = self._check_classification_credit()
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
        """
        Verify credit limit for orders whose customer has a classification
        with an effective credit limit > 0.

        Calculation:
            projected_total = partner.credit + order.amount_total

        Returns:
            warning message string if policy is 'warning' and limit exceeded
        Raises:
            UserError if policy is 'block' and limit exceeded
        """
        warning_msg = ''
        for order in self:
            partner = order.partner_id.commercial_partner_id

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
                f"⚠️ {partner.display_name}: Credit limit exceeded by {exceeded_by:,.2f}.\n"
            )

        return warning_msg or None