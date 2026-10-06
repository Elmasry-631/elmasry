# -*- coding: utf-8 -*-
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    el_pos_default_payment_method_ids = fields.Many2many(
        "pos.payment.method",
        relation="el_pos_config_default_payment_rel",
        string="Default Payment Methods",
        help="Payment methods shown for customers that do not have a "
             "specific allowed list. Leave empty to show all payment "
             "methods of this POS.",
    )
