from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_classification_id = fields.Many2one(
        comodel_name='customer.classification',
        string='Customer Classification',
        related='partner_id.commercial_partner_id.classification_id',
        store=True,
    )

    partner_effective_credit_limit = fields.Float(
        string='Effective Credit Limit',
        digits=(16, 2),
        related='partner_id.commercial_partner_id.effective_credit_limit',
    )

    partner_credit_policy = fields.Selection(
        selection=[
            ('block', 'Block Sale'),
            ('warning', 'Warning Only'),
        ],
        string='Credit Policy',
        related='partner_id.commercial_partner_id.credit_policy',
    )

    def action_post(self):
        warning_msg = self._check_invoice_credit()
        result = super().action_post()
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

    def _check_invoice_credit(self):
        warning_msg = ''
        for invoice in self:
            if invoice.move_type not in ('out_invoice', 'out_refund'):
                continue

            partner = invoice.partner_id.commercial_partner_id

            if not partner.classification_id:
                continue

            effective_limit = partner.effective_credit_limit
            if effective_limit <= 0:
                continue

            invoice_amount = invoice.amount_total if invoice.move_type == 'out_invoice' else -invoice.amount_total
            projected_total = partner.credit + invoice_amount

            if projected_total <= effective_limit:
                continue

            exceeded_by = projected_total - effective_limit
            policy = partner.credit_policy

            msg_parts = [
                f"<b>Customer:</b> {partner.display_name}",
                f"<b>Classification:</b> {partner.classification_id.display_name}",
                f"<b>Credit Limit:</b> {effective_limit:,.2f}",
                f"<b>Current Outstanding:</b> {partner.credit:,.2f}",
                f"<b>This Invoice:</b> {invoice_amount:,.2f}",
                f"<b>Projected Total:</b> {projected_total:,.2f}",
                f"<b>Exceeded By:</b> {exceeded_by:,.2f}",
                f"<b>Credit Policy:</b> {'Block Sale' if policy == 'block' else 'Warning Only'}",
            ]
            body = '<br/>'.join(msg_parts)
            html_body = (
                f"<p><b>Credit Limit {'Exceeded!' if policy == 'block' else 'Warning'}</b></p>"
                f"{body}"
            )

            invoice.message_post(body=html_body, subject=_('Credit Limit Warning'))

            if policy == 'block':
                raise UserError(
                    _(
                        "Credit Limit Exceeded!\n\n"
                        "Customer: %s\n"
                        "Classification: %s\n"
                        "Credit Limit: %s\n"
                        "Current Outstanding: %s\n"
                        "This Invoice: %s\n"
                        "Projected Total: %s\n"
                        "Exceeded By: %s\n\n"
                        "Credit Policy: Block Sale.\n"
                        "Contact credit management or change the customer's classification."
                    ) % (
                        partner.display_name,
                        partner.classification_id.display_name,
                        f"{effective_limit:,.2f}",
                        f"{partner.credit:,.2f}",
                        f"{invoice_amount:,.2f}",
                        f"{projected_total:,.2f}",
                        f"{exceeded_by:,.2f}",
                    )
                )

            warning_msg += (
                f"\u26a0\ufe0f {partner.display_name}: Credit limit exceeded by {exceeded_by:,.2f}.\n"
            )

        return warning_msg or None
