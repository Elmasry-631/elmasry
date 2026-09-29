# -*- coding: utf-8 -*-
"""
Extension of stock.move for Warehouse-Based Access Control.

This model extends stock.move to enforce warehouse-based filtering.
Moves inherit security from their parent picking.

Security Level: BACKEND (Database-level enforcement via ir.rule)
"""

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class StockMove(models.Model):
    _inherit = 'stock.move'

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
        """Check accessibility based on picking's warehouse."""
        user = self.env.user
        
        if user._is_admin():
            self.is_user_accessible = True
            return
        
        allowed_wh_ids = user._get_allowed_warehouse_ids()
        
        for record in self:
            # Move gets its warehouse from picking's picking type
            if record.picking_id and record.picking_id.picking_type_id:
                wh_id = record.picking_id.picking_type_id.warehouse_id.id
                record.is_user_accessible = wh_id in allowed_wh_ids
            elif record.picking_type_id:
                wh_id = record.picking_type_id.warehouse_id.id
                record.is_user_accessible = wh_id in allowed_wh_ids
            else:
                # For moves without picking/picking type, check location
                location_allowed = False
                if record.location_id:
                    allowed_loc_ids = user._get_allowed_location_ids()
                    location_allowed = record.location_id.id in allowed_loc_ids
                record.is_user_accessible = location_allowed

    # ============================================
    # Create Override
    # ============================================

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to enforce warehouse restrictions on moves.
        Skip check when called from MRP (raw_material_production_id) to allow
        manufacturing moves for users with MRP access without requiring manual
        warehouse assignment on server.
        """
        user = self.env.user
        
        if not user._is_admin():
            # Allow MRP production moves even if warehouse not in allowed list
            # to avoid "Cannot create move" on server deploy
            has_mrp_context = any(
                vals.get('raw_material_production_id') or vals.get('production_id')
                for vals in vals_list
            )
            if has_mrp_context and user.has_group('mrp.group_mrp_user'):
                return super(StockMove, self).create(vals_list)

            allowed_wh_ids = user._get_allowed_warehouse_ids()
            
            for vals in vals_list:
                # Check via picking
                picking_id = vals.get('picking_id')
                if picking_id:
                    picking = self.env['stock.picking'].browse(picking_id)
                    if picking.exists() and picking.picking_type_id:
                        wh_id = picking.picking_type_id.warehouse_id.id
                        if wh_id not in allowed_wh_ids:
                            raise AccessError(_(
                                "Cannot create move: You don't have access to this warehouse."
                            ))
                
                # Check via picking type directly
                picking_type_id = vals.get('picking_type_id')
                if picking_type_id:
                    ptype = self.env['stock.picking.type'].browse(picking_type_id)
                    if ptype.exists():
                        wh_id = ptype.warehouse_id.id
                        if wh_id not in allowed_wh_ids:
                            raise AccessError(_(
                                "Cannot create move: You don't have access to this warehouse."
                            ))
        
        return super(StockMove, self).create(vals_list)

    # ============================================
    # Location Domain Helpers
    # ============================================

    @api.model
    def _get_source_location_domain(self):
        """Domain for source_location_id field based on user's warehouses."""
        return self.env.user._get_location_domain()

    @api.model
    def _get_dest_location_domain(self):
        """Domain for destination_location_id field based on user's warehouses."""
        return self.env.user._get_location_domain()

    @api.model
    def _get_picking_type_domain(self):
        """Domain for picking_type_id field based on user's warehouses."""
        return self.env.user._get_picking_type_domain()
