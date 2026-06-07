# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'

    daily_order_number = fields.Char(
        string='Daily Order #',
        readonly=True,
        copy=False,
        help='The daily order number assigned to this POS order.',
        index=True,
    )

    def _process_order(self, order, existing_order):
        """Assign the daily number in Odoo 19's POS synchronization flow."""
        if not existing_order and not order.get('daily_order_number'):
            session = self.env['pos.session'].browse(order.get('session_id'))
            config = session.config_id
            if config.exists() and config.use_daily_sequence:
                order['daily_order_number'] = config._generate_daily_order_number(session=session)

        return super()._process_order(order, existing_order)

    def read_pos_data(self, data, config):
        result = super().read_pos_data(data, config)
        if result.get('pos.order'):
            daily_numbers_by_id = {
                order.id: order.daily_order_number
                for order in self
            }
            for order_data in result['pos.order']:
                order_data['daily_order_number'] = daily_numbers_by_id.get(order_data['id'])
        return result

    def action_pos_order_paid(self):
        """Override to generate daily sequence number on payment."""
        result = super(PosOrder, self).action_pos_order_paid()
        for order in self:
            if order.config_id.use_daily_sequence and not order.daily_order_number:
                order.write({
                    'daily_order_number': order.config_id._generate_daily_order_number(session=order.session_id)
                })
        return result
