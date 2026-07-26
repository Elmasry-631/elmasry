# -*- coding: utf-8 -*-
"""Account.payment.method extension: track the cheque inbound/outbound method."""
from odoo import fields, models


class AccountPaymentMethod(models.Model):
    _inherit = "account.payment.method"

    # No additional fields needed for v1; the cheque payment method is
    # created via data XML (data/account_payment_method_data.xml). This
    # class exists so that future per-method configuration (e.g. layout
    # coordinates, validation rules) has a clear extension point.
    cheque_tracking_enabled = fields.Boolean(
        string="Cheque Tracking Enabled",
        default=False,
        help="If enabled, payments created with this method will require "
             "a cheque to be selected on the payment record.",
    )
