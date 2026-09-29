# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class ChannelOrderMappings(models.Model):
    _inherit = 'channel.order.mappings'

    salla_last_resync_at = fields.Datetime(
        string='Salla Last Resync',
        copy=False,
        index=True,
        help='Last time the stalled-order resync cron attempted to re-import this '
             'order from Salla. Used to rotate the backlog so the same oldest '
             'mappings are not retried every run.',
    )
