# -*- coding: utf-8 -*-
"""
Extension of stock.location for Warehouse-Based Access Control.

This model extends stock.location to enforce warehouse-based filtering.
Users can only see locations that belong to their assigned warehouses.

Security Level: BACKEND (Database-level enforcement via ir.rule)
"""

from odoo import models, fields, api, _


class StockLocation(models.Model):
    _inherit = 'stock.location'

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
        search='_search_warehouse_id',
        store=False,
        help="The main warehouse this location belongs to",
    )

    # ============================================
    # Compute Methods
    # ============================================

    def _compute_is_user_accessible(self):
        """Check if location is accessible based on user's warehouses."""
        user = self.env.user
        
        if user._is_admin():
            self.is_user_accessible = True
            return
        
        allowed_loc_ids = user._get_allowed_location_ids()
        
        for record in self:
            record.is_user_accessible = record.id in allowed_loc_ids

    def _compute_warehouse_id(self):
        """
        Compute the warehouse for each location.
        
        A location belongs to a warehouse if it's a child of any of the 
        warehouse's main locations.
        """
        warehouses = self.env['stock.warehouse'].search([])
        wh_location_map = {}
        
        for wh in warehouses:
            # Collect all locations belonging to this warehouse
            wh_locations = self.env['stock.location']
            for loc_field in ['view_location_id', 'lot_stock_id', 
                             'wh_input_stock_loc_id', 'wh_output_stock_loc_id',
                             'wh_pack_stock_loc_id', 'wh_qc_stock_loc_id']:
                if loc_field not in wh._fields:
                    continue
                loc = wh[loc_field]
                if loc:
                    wh_locations |= loc
            
            # Get all child locations
            if wh_locations:
                wh_children = self.search([('id', 'child_of', wh_locations.ids)])
                for child in wh_children:
                    wh_location_map[child.id] = wh.id
        
        for record in self:
            record.warehouse_id = wh_location_map.get(record.id, False)

    def _search_warehouse_id(self, operator, value):
        """Custom search for computed warehouse_id field."""
        # Find locations by warehouse
        warehouses = self.env['stock.warehouse'].search([('id', operator, value)])
        
        location_ids = []
        for wh in warehouses:
            for loc_field in ['view_location_id', 'lot_stock_id', 
                             'wh_input_stock_loc_id', 'wh_output_stock_loc_id',
                             'wh_pack_stock_loc_id', 'wh_qc_stock_loc_id']:
                if loc_field not in wh._fields:
                    continue
                loc = wh[loc_field]
                if loc:
                    location_ids.append(loc.id)
        
        if location_ids:
            children = self.search([('id', 'child_of', location_ids)]).ids
            return [('id', 'in', children)]
        
        return [('id', '=', False)]

    # ============================================
    # Location Hierarchy Helpers
    # ============================================

    @api.model
    def get_allowed_location_tree(self):
        """
        Get the complete location tree for user's allowed warehouses.
        
        Returns:
            list: List of dicts with location info and children
        """
        user = self.env.user
        
        if user._is_admin():
            locations = self.search([('usage', '=', 'internal')])
        else:
            allowed_ids = user._get_allowed_location_ids()
            locations = self.browse(allowed_ids).filtered(lambda l: l.usage == 'internal')
        
        return self._build_location_tree(locations)

    def _build_location_tree(self, locations, parent_id=None):
        """Recursively build location tree structure."""
        tree = []
        
        children = locations.filtered(lambda l: l.location_id.id == parent_id)
        
        for location in children.sorted('name'):
            node = {
                'id': location.id,
                'name': location.complete_name or location.name,
                'barcode': location.barcode or '',
                'children': self._build_location_tree(locations, location.id),
            }
            tree.append(node)
        
        return tree

    # ============================================
    # Domain Generation
    # ============================================

    @api.model
    def _get_parent_location_domain(self):
        """Domain for location_id (parent) field."""
        return self.env.user._get_location_domain()

    @api.model
    def _get_child_of_domain(self):
        """Domain for finding children of accessible locations."""
        domain = self.env.user._get_location_domain()
        if not domain:
            return [('id', '=', False)]
        return [('location_id', 'child_of', [l['id'] for l in self.search_read(domain, ['id'])])]
