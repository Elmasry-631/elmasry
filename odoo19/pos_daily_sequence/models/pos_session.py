# -*- coding: utf-8 -*-

from odoo import fields, models


class PosSession(models.Model):
    _inherit = 'pos.session'

    daily_sequence_id = fields.Many2one(
        'ir.sequence',
        string='Session Order Sequence',
        copy=False,
        readonly=True,
        help='Sequence used for resetting POS order numbers within this session.',
    )
