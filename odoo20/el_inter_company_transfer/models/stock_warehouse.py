# -*- coding: utf-8 -*-
from odoo import models, api


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.model
    def name_search(self, name='', domain=None, operator='ilike', limit=100):
        """Allow inter-company transfer requests to list the warehouses of the source company.

        By default the warehouses are filtered by the company the user currently
        works in (multi-company record rule). When the user picks the company
        owning the stock, its warehouses have to be selectable even when the
        user is not working in that company, hence the superuser access.
        """
        if self.env.context.get('el_inter_company_warehouse'):
            return super(StockWarehouse, self.sudo()).name_search(
                name=name, domain=domain, operator=operator, limit=limit
            )
        return super().name_search(name=name, domain=domain, operator=operator, limit=limit)
