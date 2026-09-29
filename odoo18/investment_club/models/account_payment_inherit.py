# investment_club/models/account_payment_inherit.py
from odoo import models, fields, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    investment_subscription_id = fields.Many2one(
        'investment.subscription',
        string='Investment Subscription',
        readonly=True,
        copy=False,
    )

    # Clear breakdown shown on the payment form
    # (Participation amount + Admin fees = Payment total)
    investment_amount = fields.Monetary(
        string='Participation Amount',
        currency_field='currency_id',
        readonly=True,
        copy=False,
        help='Participation/investment amount only (excluding administrative fees)',
    )

    investment_admin_fees = fields.Monetary(
        string='Administrative Fees',
        currency_field='currency_id',
        readonly=True,
        copy=False,
        help='Administrative fees added to the payment',
    )

    investment_line_ids = fields.One2many(
        related='move_id.line_ids',
        string='Journal Items',
    )

    def action_view_investment_subscription(self):
        self.ensure_one()
        if not self.investment_subscription_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('Investment'),
            'res_model': 'investment.subscription',
            'res_id': self.investment_subscription_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    # ===== Hooks =====

    def action_post(self):
        res = super().action_post()
        # Confirming the payment (from the investment or from the payment
        # form itself) ACTIVATES the linked investment automatically.
        self.mapped('investment_subscription_id')._activate_after_payment()
        return res

    def action_cancel(self):
        subs = self.mapped('investment_subscription_id')
        res = super().action_cancel()
        # Cancelling the payment puts the investment back to draft.
        subs._sync_after_payment_cancel()
        return res
