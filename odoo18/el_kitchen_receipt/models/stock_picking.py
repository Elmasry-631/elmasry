# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    x_driver_name = fields.Many2one(
        'x.pilot',
        string='اسم الطيار',
        ondelete='restrict',
        help='اسم الطيار المسؤول عن التوصيل. بيتم مزامنته تلقائياً مع أمر البيع المرتبط.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        pickings = super().create(vals_list)
        for picking in pickings:
            if not picking.x_driver_name:
                picking._pull_driver_name_from_order()
        return pickings

    def write(self, vals):
        res = super().write(vals)
        if 'x_driver_name' in vals and not self.env.context.get('syncing_driver_name'):
            for picking in self:
                picking._push_driver_name_to_order()
        return res

    def _get_source_order(self):
        self.ensure_one()
        return self.sale_id or self.env['sale.order'].search([
            ('name', '=', self.origin),
        ], limit=1)

    def _pull_driver_name_from_order(self):
        """عند إنشاء الحركة المخزنية: خُد اسم الطيار من أمر البيع."""
        self.ensure_one()
        sale = self._get_source_order()
        if sale and sale.x_driver_name != self.x_driver_name:
            self.with_context(syncing_driver_name=True).sudo().write({
                'x_driver_name': sale.x_driver_name.id or False,
            })

    def _push_driver_name_to_order(self):
        """مزامنة عكسية: تعديل الطيار على الحركة بينتشر لأمر البيع،
        وأمر البيع بدوره بينشر القيمة على باقي الفواتير والحركات."""
        self.ensure_one()
        sale = self._get_source_order()
        if sale and sale.x_driver_name != self.x_driver_name:
            sale.with_context(syncing_driver_name=True).sudo().write({
                'x_driver_name': self.x_driver_name.id or False,
            })
