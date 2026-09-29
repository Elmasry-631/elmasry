# -*- coding: utf-8 -*-
"""
Extension of stock.picking.type for Warehouse-Based Access Control.

This model extends stock.picking.type (operation types) to enforce
warehouse-based filtering.

Security Level: BACKEND (Database-level enforcement via ir.rule)
"""

from odoo import models, fields, api, _


class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    # ============================================
    # Field Definitions
    # ============================================

    is_user_accessible = fields.Boolean(
        string='Accessible to Current User',
        compute='_compute_is_user_accessible',
        help="Technical field for UI filtering",
    )

    # ============================================
    # Compute Methods
    # ============================================

    def _compute_is_user_accessible(self):
        """Check accessibility based on warehouse."""
        user = self.env.user
        
        if user._is_admin():
            self.is_user_accessible = True
            return
        
        allowed_wh_ids = user._get_allowed_warehouse_ids()
        
        for record in self:
            if record.warehouse_id:
                record.is_user_accessible = record.warehouse_id.id in allowed_wh_ids
            else:
                # Operation types without warehouse (global) - allow access
                record.is_user_accessible = True

    # ============================================
    # Create Override
    # ============================================

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to enforce warehouse restrictions.
        Only users with warehouse access can create operation types for that warehouse.
        """
        user = self.env.user
        
        if not user._is_admin():
            allowed_wh_ids = user._get_allowed_warehouse_ids()
            
            for vals in vals_list:
                warehouse_id = vals.get('warehouse_id')
                
                if warehouse_id and warehouse_id not in allowed_wh_ids:
                    warehouse = self.env['stock.warehouse'].browse(warehouse_id)
                    raise AccessError(_(
                        "Cannot create operation type for warehouse '%s'. "
                        "You don't have access to this warehouse."
                    ) % (warehouse.name if warehouse.exists() else str(warehouse_id)))
        
        return super(StockPickingType, self).create(vals_list)

    # ============================================
    # Domain Helpers
    # ============================================

    @api.model
    def _get_warehouse_domain(self):
        """Domain for warehouse_id field."""
        return self.env.user._get_warehouse_domain()

    @api.model
    def _get_default_location_domain(self):
        """Domain for default_location_src_id and default_location_dest_id."""
        return self.env.user._get_location_domain()

    @api.model
    def _get_return_location_domain(self):
        """Domain for default_location_return_id."""
        return self.env.user._get_location_domain()

    # ============================================
    # UI Helpers
    # ============================================

    @api.onchange('warehouse_id')
    def _onchange_warehouse_check(self):
        """Warn if user selects a warehouse they don't have access to."""
        user = self.env.user
        
        if not user._is_admin() and self.warehouse_id:
            allowed_wh_ids = user._get_allowed_warehouse_ids()
            
            if self.warehouse_id.id not in allowed_wh_ids:
                return {
                    'warning': {
                        'title': _('Warehouse Access Warning'),
                        'message': _(
                            "You don't have access to warehouse '%s'. "
                            "This operation type may not be visible to you after creation."
                        ) % self.warehouse_id.name,
                    }
                }
        
        return {}
