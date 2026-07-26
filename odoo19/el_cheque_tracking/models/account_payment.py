# -*- coding: utf-8 -*-
"""Account.payment extension: optional link to a cheque."""
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AccountPayment(models.Model):
    _inherit = "account.payment"

    cheque_id = fields.Many2one(
        string="Cheque",
        comodel_name="cheque.cheque",
        ondelete="restrict",
        index=True,
        copy=False,
    )

    @api.constrains("cheque_id", "partner_id", "payment_type")
    def _check_cheque_consistency(self):
        for pay in self:
            if not pay.cheque_id:
                continue
            cheque = pay.cheque_id
            if cheque.cheque_type == "received" and pay.payment_type == "outbound":
                raise UserError(
                    _("The cheque type must match the payment: use a received "
                      "cheque with inbound payments or an issued cheque with "
                      "outbound payments.")
                )
            if cheque.cheque_type == "issued" and pay.payment_type == "inbound":
                raise UserError(
                    _("The cheque type must match the payment: use a received "
                      "cheque with inbound payments or an issued cheque with "
                      "outbound payments.")
                )
            if cheque.partner_id and cheque.partner_id != pay.partner_id:
                raise UserError(
                    _("The payment partner must match the partner on the selected cheque.")
                )

    @api.onchange("cheque_id")
    def _onchange_cheque_id(self):
        if self.cheque_id:
            cheque = self.cheque_id
            if cheque.partner_id:
                self.partner_id = cheque.partner_id
            if cheque.amount:
                self.amount = cheque.amount
            if cheque.currency_id:
                self.currency_id = cheque.currency_id
