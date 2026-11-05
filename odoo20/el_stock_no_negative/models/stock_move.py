# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _check_negative_stock_on_done(self):
        """Check negative stock when marking move as done"""
        for move in self:
            if move.state == 'done' and move.product_id.type == 'consu':
                # Check if negative stock is allowed
                if not move.product_id._get_allow_negative_stock():
                    # Get the location where stock is being removed from
                    location = move.location_id
                    if location.usage == 'internal':
                        available_qty = move.product_id.with_context(location=location.id).qty_available
                        if available_qty < 0:
                            raise UserError(_(
                                'Insufficient stock for product "%s" in location "%s". '
                                'Available: %s. Cannot validate transfer as it would result in negative stock.',
                                move.product_id.display_name, location.display_name, available_qty
                            ))

    def _action_done(self, cancel_backorder=False):
        """Override to check negative stock before validating move"""
        res = super()._action_done(cancel_backorder=cancel_backorder)
        self._check_negative_stock_on_done()
        return res