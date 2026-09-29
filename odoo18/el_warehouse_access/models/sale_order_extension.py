# -*- coding: utf-8 -*-
from odoo import models, api, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Dynamic domain based on user's allowed warehouses
    warehouse_id = fields.Many2one(domain=lambda self: self._domain_warehouse_id())

    @api.model
    def _domain_warehouse_id(self):
        user = self.env.user
        if user._is_admin():
            return []
        wh_ids = user._get_allowed_warehouse_ids()
        if not wh_ids:
            return [('id', '=', False)]
        return [('id', 'in', wh_ids)]

    @api.model_create_multi
    def create(self, vals_list):
        user = self.env.user
        if not user._is_admin():
            allowed = set(user._get_allowed_warehouse_ids())
            for vals in vals_list:
                wh_id = vals.get('warehouse_id')
                if wh_id and int(wh_id) not in allowed:
                    vals['warehouse_id'] = list(allowed)[0] if allowed else False
        return super().create(vals_list)
