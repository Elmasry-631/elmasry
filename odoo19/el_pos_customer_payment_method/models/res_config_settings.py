# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_el_default_payment_method_ids = fields.Many2many(
        related="pos_config_id.el_pos_default_payment_method_ids",
        readonly=False,
        string="Default Payment Methods",
        help="Payment methods shown for customers that do not have a "
             "specific allowed list.",
    )
