# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    def _process_order(self, pos_order):
        """Override to check negative stock before processing POS order"""
        # Check stock for each line
        for line in pos_order.get('lines', []):
            line_data = line[2] if isinstance(line, (list, tuple)) and len(line) > 2 else line
            product_id = line_data.get('product_id')
            qty = line_data.get('qty', 0)
            
            if product_id and qty > 0:
                product = self.env['product.product'].browse(product_id)
                config_id = pos_order.get('config_id')
                config = self.env['pos.config'].browse(config_id) if config_id else False
                
                # Get the stock location for this POS
                location_id = config.stock_location_id.id if config and config.stock_location_id else False
                
                if location_id:
                    # Check available quantity
                    available_qty = self.env['stock.quant']._get_available_quantity(
                        product, self.env['stock.location'].browse(location_id)
                    )
                    
                    # Check if negative stock is allowed
                    if not product._get_allow_negative_stock():
                        # For kit products, check components
                        if self.env['stock.quant']._is_kit_product(product):
                            if not self.env['stock.quant']._check_kit_components_availability(
                                product, self.env['stock.location'].browse(location_id), qty
                            ):
                                raise UserError(_(
                                    'Insufficient stock for kit product "%s" components in POS. '
                                    'Cannot complete sale as it would result in negative stock.',
                                    product.display_name
                                ))
                        elif available_qty < qty:
                            raise UserError(_(
                                'Insufficient stock for product "%s" in POS location "%s". '
                                'Available: %s, Requested: %s. Cannot complete sale.',
                                product.display_name, config.stock_location_id.display_name, available_qty, qty
                            ))
        
        return super()._process_order(pos_order)