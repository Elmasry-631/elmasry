# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    x_driver_name = fields.Many2one(
        'x.pilot',
        string='اسم الطيار',
        ondelete='restrict',
        help='اسم الطيار المسؤول عن التوصيل. بيتم مزامنته تلقائياً مع أمر البيع المرتبط.',
    )

    def write(self, vals):
        res = super().write(vals)
        if 'x_driver_name' in vals and not self.env.context.get('syncing_driver_name'):
            for move in self:
                move._sync_driver_name_to_orders()
        return res

    def _sync_driver_name_to_orders(self):
        """
        مزامنة عكسية: لما اسم الطيار يتغير على الفاتورة، بيترجع لأمر البيع
        المرتبط، وأمر البيع بدوره بينشر القيمة على باقي الفواتير والحركات المخزنية.
        """
        self.ensure_one()
        orders = self.line_ids.sale_line_ids.order_id.filtered(
            lambda o: o.x_driver_name != self.x_driver_name
        )
        for order in orders:
            order.with_context(syncing_driver_name=True).sudo().write({
                'x_driver_name': self.x_driver_name.id or False,
            })
