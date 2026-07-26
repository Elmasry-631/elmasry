# -*- coding: utf-8 -*-
"""Account.payment.register extension: prefill cheque from context."""
from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    cheque_id = fields.Many2one(
        string="Cheque",
        comodel_name="cheque.cheque",
        ondelete="restrict",
    )

    def _create_payment_vals_from_wizard(self):
        vals = super()._create_payment_vals_from_wizard()
        if self.cheque_id:
            vals["cheque_id"] = self.cheque_id.id
        return vals
