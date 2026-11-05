# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def _check_negative_stock(self, product_id, location_id, qty, package_id=False, owner_id=False, lot_id=False, on_hand=False):
        """Check if the operation would result in negative stock"""
        # Skip check if negative stock is allowed globally
        param = self.env['ir.config_parameter'].sudo().search([('key', '=', 'stock.allow_negative_stock')], limit=1)
        if param and param.value == 'True':
            return True
        
        # Skip check for products that allow negative stock
        # product_id can be an integer or a product.product record
        if hasattr(product_id, 'id'):
            product_id = product_id.id
        self.env.cr.execute("""
            SELECT pt.allow_negative_stock
            FROM product_template pt
            JOIN product_product pp ON pp.product_tmpl_id = pt.id
            WHERE pp.id = %s
        """, (product_id,))
        result = self.env.cr.fetchone()
        if result and result[0]:
            return True
        
        # Skip check for locations that allow negative stock (e.g., supplier locations)
        # location_id can be an integer or a stock.location record
        if hasattr(location_id, 'id'):
            location_id = location_id.id
        location = self.env['stock.location'].browse(location_id)
        if location.usage == 'supplier':
            return True
        
        # Get product for later use
        product = self.env['product.product'].browse(product_id)
        
        # Check current quantity: on hand for reservations, available for real movements
        if on_hand:
            current_qty = self._get_on_hand_quantity(
                product, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id
            )
        else:
            current_qty = self._get_available_quantity(
                product, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=False
            )
        
        # If qty is negative (outgoing), check if we have enough
        if qty < 0 and current_qty + qty < 0:
            # Check if product is a kit (phantom BoM)
            if self._is_kit_product(product):
                # For kit products, check component availability
                if not self._check_kit_components_availability(product, location, abs(qty), lot_id, package_id, owner_id):
                    raise UserError(_(
                        'Insufficient stock for kit product "%s" components. '
                        'Cannot complete operation as it would result in negative stock.',
                        product.display_name
                    ))
            else:
                raise UserError(_(
                    'Insufficient stock for product "%s" in location "%s". '
                    'Available: %s, Requested: %s. Cannot complete operation as it would result in negative stock.',
                    product.display_name, location.display_name, current_qty, abs(qty)
                ))
        
        return True

    def _get_on_hand_quantity(self, product, location, lot_id=False, package_id=False, owner_id=False):
        """Sum of the quantities physically stored in the given location"""
        quants = self.sudo().search([
            ('product_id', '=', product.id),
            ('location_id', '=', location.id),
            ('lot_id', '=', lot_id.id if lot_id else False),
            ('package_id', '=', package_id.id if package_id else False),
            ('owner_id', '=', owner_id.id if owner_id else False),
        ])
        return sum(quants.mapped('quantity'))

    def _is_kit_product(self, product):
        """Check if product is a kit (phantom BoM)"""
        if 'mrp.bom' not in self.env.registry:
            return False
        bom = self.env['mrp.bom']._bom_find(product=product, company_id=self.env.company.id)
        return bom and bom.type == 'phantom'

    def _check_kit_components_availability(self, product, location, qty, lot_id=False, package_id=False, owner_id=False):
        """Check if all components of a kit product have enough stock"""
        if 'mrp.bom' not in self.env.registry:
            return True
        bom = self.env['mrp.bom']._bom_find(product=product, company_id=self.env.company.id)
        if not bom or bom.type != 'phantom':
            return True
        
        # Get all components needed for the requested quantity
        bom_qty = bom.product_qty
        factor = qty / bom_qty
        
        for line in bom.bom_line_ids:
            component = line.product_id
            component_qty = line.product_qty * factor
            
            # Check component availability
            available_qty = self._get_available_quantity(
                component, location, lot_id=lot_id, package_id=package_id, owner_id=owner_id, strict=False
            )
            
            if available_qty < component_qty:
                # Check if component allows negative stock
                component_sudo = component.sudo()
                if not component_sudo.product_tmpl_id.allow_negative_stock and not component_sudo.categ_id.allow_negative_stock:
                    return False
        
        return True

    @api.model
    def _update_available_quantity(self, product_id, location_id, quantity=False, reserved_quantity=False, lot_id=None, package_id=None, owner_id=None, in_date=None):
        """Override to add negative stock check"""
        # Check before updating
        self._check_negative_stock(product_id, location_id, quantity, package_id, owner_id, lot_id)
        
        return super()._update_available_quantity(
            product_id, location_id, quantity, reserved_quantity, lot_id, package_id, owner_id, in_date
        )

    def _update_reserved_quantity(self, product_id, location_id, quantity, lot_id=None, package_id=None, owner_id=None, strict=True):
        """Override to add negative stock check for reservations"""
        # Check before updating reservation: a reservation does not change the on hand
        # quantity, so the on hand quantity is the relevant one here.
        self._check_negative_stock(product_id, location_id, quantity, package_id, owner_id, lot_id, on_hand=True)
        
        return super()._update_reserved_quantity(
            product_id, location_id, quantity, lot_id, package_id, owner_id, strict
        )