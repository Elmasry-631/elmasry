# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    el_allowed_pos_payment_method_ids = fields.Many2many(
        "pos.payment.method",
        string="Allowed POS Payment Methods",
        help="Payment methods this customer may use in the Point of Sale. "
             "Leave empty to fall back to the POS default payment methods.",
    )

    def _load_pos_data_fields(self, config_id):
        # Expose the allowed methods to the POS frontend so the payment
        # screen can filter its buttons per order partner. commercial_partner_id
        # rides along because an order can be set to a child (invoice)
        # address while the restriction lives on its parent.
        return super()._load_pos_data_fields(config_id) + [
            "el_allowed_pos_payment_method_ids",
            "commercial_partner_id",
        ]
