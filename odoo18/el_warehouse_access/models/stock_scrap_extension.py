# -*- coding: utf-8 -*-
"""
Extension of stock.scrap for Warehouse-Based Access Control.

This model extends stock.scrap to enforce warehouse-based filtering.
Scraps are restricted by their location_id.

Security Level: BACKEND (Database-level enforcement via ir.rule)
"""

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockScrap(models.Model):
    _inherit = 'stock.scrap'

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
        compute='_compute_warehouse_id',
        store=False,
        readonly=True,
        help="Warehouse this scrap belongs to",
    )

    # ============================================
    # Compute Methods
    # ============================================

    def _compute_is_user_accessible(self):
        """Check accessibility based on scrap location."""
        user = self.env.user
        
        if user._is_admin():
            self.is_user_accessible = True
            return
        
        allowed_loc_ids = user._get_allowed_location_ids()
        
        for record in self:
            record.is_user_accessible = record.location_id.id in allowed_loc_ids

    def _compute_warehouse_id(self):
        """Determine warehouse from scrap location."""
        warehouses = self.env['stock.warehouse'].search([])
        
        for record in self:
            if not record.location_id:
                record.warehouse_id = False
                continue
                
            for wh in warehouses:
                wh_locations = self.env['stock.location']
                for loc_field in ['lot_stock_id', 'view_location_id']:
                    if wh[loc_field]:
                        wh_locations |= wh[loc_field]
                
                children = self.env['stock.location'].search([
                    ('id', 'child_of', wh_locations.ids)
                ])
                
                if record.location_id.id in children.ids:
                    record.warehouse_id = wh
                    break
            else:
                record.warehouse_id = False

    # ============================================
    # Create Override
    # ============================================

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to enforce warehouse restrictions on scraps.
        """
        user = self.env.user
        
        if not user._is_admin():
            allowed_loc_ids = user._get_allowed_location_ids()
            
            for vals in vals_list:
                location_id = vals.get('location_id')
                
                if location_id and location_id not in allowed_loc_ids:
                    location = self.env['stock.location'].browse(location_id)
                    raise AccessError(_(
                        "Cannot create scrap at location '%s'. "
                        "You don't have access to this location/warehouse."
                    ) % (location.display_name if location.exists() else str(location_id)))
        
        return super(StockScrap, self).create(vals_list)

    # ============================================
    # Action Validate Override
    # ============================================

    def action_validate(self):
        """
        Override action_validate to verify user still has access.
        """
        user = self.env.user
        
        if not user._is_admin():
            allowed_loc_ids = user._get_allowed_location_ids()
            
            for record in self:
                if record.location_id.id not in allowed_loc_ids:
                    raise AccessError(_(
                        "Cannot validate scrap '%s' - you don't have access "
                        "to its location '%s'."
                    ) % (record.name, record.location_id.display_name))
        
        return super(StockScrap, self).action_validate()

    # ============================================
    # Domain Helpers
    # ============================================

    @api.model
    def _get_location_domain(self):
        """Domain for location_id field."""
        return self.env.user._get_location_domain()

    @api.model
    def _get_product_domain(self):
        """Domain for product_id - no restriction."""
        return []

    @api.model
    def _get_picking_type_domain(self):
        """Domain for picking_id field."""
        return self.env.user._get_picking_type_domain()

    @api.onchange('location_id')
    def _onchange_location_check(self):
        """Warn about location access."""
        user = self.env.user
        
        if not user._is_admin() and self.location_id:
            allowed_loc_ids = user._get_allowed_location_ids()
            
            if self.location_id.id not in allowed_loc_ids:
                return {
                    'warning': {
                        'title': _('Location Access Warning'),
                        'message': _(
                            "You don't have access to location '%s'. "
                            "You may not be able to validate this scrap."
                        ) % self.location_id.display_name,
                    }
                }
        
        return {}
