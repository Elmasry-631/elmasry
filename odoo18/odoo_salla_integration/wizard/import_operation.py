# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields, models


class ImportOperation(models.TransientModel):
    _inherit = 'import.operation'

    salla_filter_type = fields.Selection(
        string='Filter Type',
        selection=[
            ('all', 'All'),
            ('id', 'By ID'),
            ('date', 'By Date')
        ],
        default='all',
        required=True,
    )
    salla_object_id = fields.Char('Object ID')
    salla_from_date = fields.Datetime()
    salla_to_date = fields.Datetime()
    salla_enable_keyword = fields.Boolean() 
    salla_product_keyword = fields.Char() # product name(full name or a part) or sku
    salla_skip_product_images = fields.Boolean(
        string='Skip images for this import',
        help='Force skip product image downloads for this import run only.',
    )
    salla_order_status = fields.Selection([
        ('566146469','Under Review'),
        ('1473353380','Pending Payment'),
        ('814202285','Shipped'),
        ('349994915','Delivery in Progress'),
        ('1723506348','Delivered'),
        ('1298199463','Completed'),
        ('525144736','Canceled'),
    ])

    def import_with_filter(self, **kw):
        channel = self.channel_id
        if channel.channel == 'salla' and kw.get('object') == 'sale.order' and not kw.get('from_cron'):
            # Same per-channel lock as the order crons: a manual import running at
            # the same time as the sweep/resync cron used to end in
            # "could not serialize access due to concurrent update".
            if not channel._salla_try_acquire_order_import_lock():
                return channel.display_message(
                    "<p class='text-warning'>A Salla order import is already running for this "
                    "channel (scheduled action or another user). Please try again in a few minutes.</p>"
                )
            try:
                return super().import_with_filter(**kw)
            finally:
                channel._salla_release_order_import_lock()
        return super().import_with_filter(**kw)

    def salla_get_filter(self):
        kw = {
                'filter_type': self.salla_filter_type,
                'salla_product_keyword':self.salla_product_keyword,
                'salla_enable_keyword':self.salla_enable_keyword,
                'salla_order_status': self.salla_order_status,
              }
        if self.salla_skip_product_images and self.object == 'product.template':
            kw['skip_product_images_force'] = True
        if self.salla_filter_type == 'id':
            kw['object_id'] = self.salla_object_id
        if self.salla_filter_type == "date":
            kw.update({
                'salla_from_date': self.salla_from_date,
                'salla_to_date': self.salla_to_date,
            })
        return kw
