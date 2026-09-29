# -*- coding: utf-8 -*-
"""
Extension of stock.picking for Warehouse-Based Access Control.

This model extends stock.picking to enforce warehouse-based filtering.
Security is enforced at TWO levels:
1. ir.rule (database-level) - prevents any data access outside warehouses
2. Domain filters (UI-level) - improves UX by hiding unrelated records

Security Level: BACKEND (Database-level enforcement via ir.rule)
"""

from odoo import models, fields, api, _

# Domain helper for destination location - internal + allowed
def _domain_location_dest_id(self):
    # Hide view locations only, show all others (internal, customer, supplier, etc.)
    # Sender sees all warehouses' locations; receiver filtering kept by ir.rule
    return [('usage', '!=', 'view')]



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # ============================================
    # Field Definitions
    # ============================================
    
    is_user_accessible = fields.Boolean(
        string='Accessible to Current User',
        compute='_compute_is_user_accessible',
        search='_search_is_user_accessible',
        help="Technical field indicating if this picking is accessible "
             "to the current user based on their warehouse assignment",
    )
    # Helper for readonly logic: single vs multi warehouse user
    user_warehouse_count = fields.Integer(
        compute='_compute_user_warehouse_count',
        string='User Warehouse Count',
    )
    is_single_warehouse_user = fields.Boolean(
        compute='_compute_user_warehouse_count',
        string='Is Single Warehouse User',
    )
    location_dest_id = fields.Many2one(domain=lambda self: _domain_location_dest_id(self))

    @api.depends_context('uid')
    def _compute_user_warehouse_count(self):
        count = len(self.env.user._get_allowed_warehouse_ids())
        # fallback for admin (has all warehouses) -> treat as multi
        is_single = count == 1
        for rec in self:
            rec.user_warehouse_count = count
            rec.is_single_warehouse_user = is_single

    # ============================================
    # Compute Methods
    # ============================================

    def _compute_is_user_accessible(self):
        """Check if each record is accessible to the current user."""
        user = self.env.user
        
        if user._is_admin():
            self.is_user_accessible = True
            return
        
        allowed_wh_ids = user._get_allowed_warehouse_ids()
        
        for record in self:
            if record.picking_type_id.warehouse_id.id in allowed_wh_ids:
                record.is_user_accessible = True
            else:
                record.is_user_accessible = False

    def _search_is_user_accessible(self, operator, value):
        """
        Custom search method for is_user_accessible field.
        
        This allows using is_user_accessible in search domains.
        """
        user = self.env.user
        
        if user._is_admin():
            return [(1, '=', 1)]  # Always true for admins
        
        allowed_wh_ids = user._get_allowed_warehouse_ids()
        if not allowed_wh_ids:
            return [(1, '=', 0)]  # Never true if no access
        
        # Get picking types for these warehouses
        picking_type_ids = self.env['stock.picking.type'].search([
            ('warehouse_id', 'in', allowed_wh_ids)
        ]).ids
        
        if operator == '=':
            if value:
                return [('picking_type_id', 'in', picking_type_ids)]
            else:
                return [('picking_type_id', 'not in', picking_type_ids)]
        elif operator == '!=':
            if value:
                return [('picking_type_id', 'not in', picking_type_ids)]
            else:
                return [('picking_type_id', 'in', picking_type_ids)]
        
        return [(1, '=', 1)]  # Fallback

    # ============================================
    # Override: Default Picking Type
    # ============================================

    @api.model_create_multi
    def create(self, vals_list):
        """
        Override create to enforce warehouse-based picking type assignment.
        
        When a user creates a new picking, ensure they're creating it
        in one of their assigned warehouses.
        """
        user = self.env.user
        
        if not user._is_admin():
            allowed_wh_ids = user._get_allowed_warehouse_ids()
            
            for vals in vals_list:
                picking_type_id = vals.get('picking_type_id')
                
                if picking_type_id:
                    picking_type = self.env['stock.picking.type'].browse(picking_type_id)
                    if picking_type.exists():
                        wh_id = picking_type.warehouse_id.id
                        if wh_id not in allowed_wh_ids:
                            raise AccessError(_(
                                "You cannot create a transfer in warehouse '%s'. "
                                "You don't have access to this warehouse."
                            ) % picking_type.warehouse_id.name)
        
        return super(StockPicking, self).create(vals_list)



    # ============================================
    # UI Helper Methods
    # ============================================

    @api.onchange('picking_type_id')
    def _onchange_picking_type_warehouse_check(self):
        """
        Warning when user selects a picking type outside their warehouses.
        
        This provides early feedback before save (ir.rule will block at DB level).
        """
        user = self.env.user
        
        if not user._is_admin() and self.picking_type_id:
            allowed_wh_ids = user._get_allowed_warehouse_ids()
            
            if self.picking_type_id.warehouse_id.id not in allowed_wh_ids:
                return {
                    'warning': {
                        'title': _('Warehouse Access Warning'),
                        'message': _(
                            "You are selecting an operation type from warehouse '%s' "
                            "which you don't have access to. You may not be able to "
                            "save this record."
                        ) % self.picking_type_id.warehouse_id.name,
                    }
                }
        
        return {}
