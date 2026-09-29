# -*- coding: utf-8 -*-
"""
Extension of stock.quant for Warehouse-Based Access Control.

This model extends stock.quant (inventory quantities) to enforce
warehouse-based filtering. Quants are filtered by their location.

Security Level: BACKEND (Database-level enforcement via ir.rule)
"""

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # ============================================
    # Field Definitions
    # ============================================

    is_user_accessible = fields.Boolean(
        string='Accessible to Current User',
        compute='_compute_is_user_accessible',
        help="Technical field for UI filtering",
    )
    
    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
        related='location_id.warehouse_id',
        store=False,
        readonly=True,
        help="Warehouse this quant belongs to (via location)",
    )

    # ============================================
    # Compute Methods
    # ============================================

    def _compute_is_user_accessible(self):
        """Check accessibility based on quant's location."""
        user = self.env.user
        
        if user._is_admin():
            self.is_user_accessible = True
            return
        
        allowed_loc_ids = user._get_allowed_location_ids()
        
        for record in self:
            record.is_user_accessible = record.location_id.id in allowed_loc_ids

    # ============================================
    # Create Override
    # ============================================

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to enforce warehouse restrictions on quants.
        """
        user = self.env.user
        
        if not user._is_admin():
            allowed_loc_ids = user._get_allowed_location_ids()
            
            for vals in vals_list:
                location_id = vals.get('location_id')
                
                if location_id and location_id not in allowed_loc_ids:
                    location = self.env['stock.location'].sudo().browse(location_id)
                    if location.usage in ('customer','supplier','inventory','transit','view','production'):
                        continue
                    raise AccessError(_(
                        "Cannot create inventory quantity at location '%s'. "
                        "You don't have access to this location/warehouse."
                    ) % (location.display_name if location.exists() else str(location_id)))
        
        return super(StockQuant, self).create(vals_list)

    # ============================================
    # Write Override
    # ============================================

    def write(self, vals):
        """
        Override write to enforce warehouse restrictions.
        """
        user = self.env.user
        
        if not user._is_admin() and 'location_id' in vals:
            allowed_loc_ids = user._get_allowed_location_ids()
            new_location_id = vals.get('location_id')
            
            if new_location_id and new_location_id not in allowed_loc_ids:
                location = self.env['stock.location'].browse(new_location_id)
                raise AccessError(_(
                    "Cannot move inventory quantity to location '%s'. "
                    "You don't have access to this location/warehouse."
                ) % (location.display_name if location.exists() else str(new_location_id)))
        
        return super(StockQuant, self).write(vals)



    # ============================================
    # Action Overrides - Filter stock report by user's warehouse
    # ============================================

    def _get_quants_action(self, domain=None, extend=False):
        action = super()._get_quants_action(domain=domain, extend=extend)
        user = self.env.user
        if not user._is_admin():
            allowed = user._get_allowed_location_ids()
            if not allowed:
                action['domain'] = [('id', '=', False)]
            else:
                # Merge with existing domain
                from odoo.osv.expression import AND
                existing = action.get('domain') or []
                action['domain'] = AND([existing, [('location_id', 'in', allowed)]])
        return action

    @api.model
    def action_view_inventory(self):
        action = super().action_view_inventory()
        user = self.env.user
        if not user._is_admin():
            allowed = user._get_allowed_location_ids()
            if not allowed:
                action['domain'] = [('id', '=', False)]
            else:
                from odoo.osv.expression import AND
                existing = action.get('domain') or []
                action['domain'] = AND([existing, [('location_id', 'in', allowed)]])
        return action

    # ============================================
    # Domain Helpers
    # ============================================

    @api.model
    def _get_location_domain(self):
        """Domain for location_id field."""
        return self.env.user._get_location_domain()

    @api.model
    def _get_product_domain(self):
        """
        Domain for product_id - no restriction by default.
        Products are not warehouse-specific.
        """
        return []

    @api.model
    def _get_lot_domain(self):
        """Domain for lot/serial number - filter by location context."""
        return []
