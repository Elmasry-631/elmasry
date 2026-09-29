# -*- coding: utf-8 -*-
"""
Extension of res.users to add Warehouse-Based Access Control.

This model extends res.users to add:
- warehouse_ids: Many2many field for assigning multiple warehouses to a user
- Helper methods for retrieving user's allowed warehouses
- Domain generation methods for use in record rules

Security Level: BACKEND (Database-level enforcement via ir.rule)
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError
from odoo.tools import frozendict


class ResUsers(models.Model):
    _inherit = 'res.users'

    # ============================================
    # Field Definitions
    # ============================================
    
    warehouse_ids = fields.Many2many(
        comodel_name='stock.warehouse',
        relation='res_users_stock_warehouse_rel',
        column1='user_id',
        column2='warehouse_id',
        string='Allowed Warehouses',
        help="Warehouses this user is permitted to access. "
             "Leave empty for NO access to any stock operations. "
             "Administrators bypass this restriction.",
        index=True,
    )
    
    warehouse_count = fields.Integer(
        string='Warehouse Count',
        compute='_compute_warehouse_count',
        store=False,
        help="Number of warehouses assigned to this user",
    )

    # ============================================
    # Compute Methods
    # ============================================

    @api.depends('warehouse_ids')
    def _compute_warehouse_count(self):
        """Compute the number of warehouses assigned to each user."""
        for record in self:
            record.warehouse_count = len(record.warehouse_ids)

    # ============================================
    # Security Helper Methods (Used by ir.rule)
    # ============================================

    def _get_allowed_warehouse_ids(self):
        """
        Return list of warehouse IDs this user is allowed to access.
        
        This method is called by ir.rule domain_force expressions.
        
        Returns:
            list[int]: List of stock.warehouse IDs, or empty list if no warehouses assigned
        
        Note:
            - Administrator/Settings users get ALL warehouses (bypass)
            - Users with no assignment get empty list (no access)
            - Regular users get only their assigned warehouses
        """
        self.ensure_one()
        
        # Rule 1: Administrators bypass all restrictions
        if self._is_admin():
            all_warehouses = self.env['stock.warehouse'].search([]).ids
            return all_warehouses
        
        # Rule 2: MRP users need at least ToYou Factory (id 1) for manufacturing
        # to avoid Picking Type:11 block on server deploy without manual SQL
        wh_ids = self.warehouse_ids.ids
        if self.has_group('mrp.group_mrp_user') and 1 not in wh_ids:
            wh_ids = wh_ids + [1]
        return wh_ids

    def _get_allowed_location_ids(self):
        """
        Return list of location IDs based on user's warehouse assignments.
        
        This includes:
        - All view locations of assigned warehouses
        - All stock locations of assigned warehouses  
        - All child locations of the above
        
        Returns:
            list[int]: List of stock.location IDs
        """
        self.ensure_one()
        
        if self._is_admin():
            # Admin sees all locations
            return self.env['stock.location'].search([]).ids
        
        warehouse_ids = self._get_allowed_warehouse_ids()
        if not warehouse_ids:
            return []
        
        # Get all locations for these warehouses
        warehouses = self.env['stock.warehouse'].browse(warehouse_ids)
        location_ids = []
        
        for wh in warehouses:
            # Add main locations
            if wh.view_location_id:
                location_ids.append(wh.view_location_id.id)
            if wh.lot_stock_id:
                location_ids.append(wh.lot_stock_id.id)
            if wh.wh_input_stock_loc_id:
                location_ids.append(wh.wh_input_stock_loc_id.id)
            if wh.wh_output_stock_loc_id:
                location_ids.append(wh.wh_output_stock_loc_id.id)
            if wh.wh_pack_stock_loc_id:
                location_ids.append(wh.wh_pack_stock_loc_id.id)
            if wh.wh_qc_stock_loc_id:
                location_ids.append(wh.wh_qc_stock_loc_id.id)
            if 'wh_return_stock_loc_id' in wh._fields and wh.wh_return_stock_loc_id:
                location_ids.append(wh.wh_return_stock_loc_id.id)
        
        # Get all child locations recursively (use sudo to bypass ir.rule during computation)
        if location_ids:
            all_child_ids = self.env['stock.location'].sudo().search([
                ('id', 'child_of', location_ids)
            ]).ids
            return list(set(all_child_ids))
        
        return []

    def _get_allowed_picking_type_ids(self):
        """
        Return list of picking type IDs based on user's warehouse assignments.
        
        Returns:
            list[int]: List of stock.picking.type IDs
        """
        self.ensure_one()
        
        if self._is_admin():
            return self.env['stock.picking.type'].search([]).ids
        
        warehouse_ids = self._get_allowed_warehouse_ids()
        if not warehouse_ids:
            return []
        
        picking_types = self.env['stock.picking.type'].search([
            ('warehouse_id', 'in', warehouse_ids)
        ])
        return picking_types.ids

    def _is_admin(self):
        """
        Check if user is an administrator who should bypass warehouse restrictions.
        
        Administrators are defined as:
        - Users with Settings access (base.group_system)
        - The root/admin user (uid SUPERUSER_ID, uid 1, or uid 2)
        - Users in el_warehouse_access.group_warehouse_manager
        
        Returns:
            bool: True if user is admin and should bypass restrictions
        """
        self.ensure_one()
        
        # Superuser always has full access - check the record's id
        if self.id in (1, 2):
            return True
        if self.env.su and self.env.uid in (1, 2):
            return True
        
        # Check for system/manager groups explicitly on this user (avoid env.uid pollution)
        # Use user_has_groups or has_group on sudo as this user
        if self.has_group('base.group_system'):
            return True
            
        # Check for our custom manager group
        if self.has_group('el_warehouse_access.group_warehouse_manager'):
            return True
        
        return False

    def _has_warehouse_access(self):
        """
        Check if user has ANY warehouse assigned.
        
        Returns:
            bool: True if user has at least one warehouse OR is admin
        """
        self.ensure_one()
        
        if self._is_admin():
            return True
        
        return bool(self.warehouse_ids)

    # ============================================
    # Domain Generation Methods (for field domains)
    # ============================================

    @api.model
    def _get_warehouse_domain(self):
        """
        Generate a domain for filtering warehouses by current user's access.
        
        Use this as domain on Many2one(warehouse_id) fields:
            domain=lambda self: self.env.user._get_warehouse_domain()
        
        Returns:
            list: Odoo domain expression
        """
        if self.env.user._is_admin():
            return []  # No restriction for admins
        
        warehouse_ids = self.env.user._get_allowed_warehouse_ids()
        if not warehouse_ids:
            # Return impossible domain to show no results
            [('id', '=', False)]
        
        return [('id', 'in', warehouse_ids)]

    @api.model
    def _get_location_domain(self):
        """
        Generate a domain for filtering locations by current user's warehouse access.
        
        Returns:
            list: Odoo domain expression
        """
        if self.env.user._is_admin():
            return []
        
        location_ids = self.env.user._get_allowed_location_ids()
        if not location_ids:
            return [('id', '=', False)]
        
        return [('id', 'in', location_ids)]

    @api.model
    def _get_picking_type_domain(self):
        """
        Generate a domain for filtering picking types by current user's warehouse access.
        
        Returns:
            list: Odoo domain expression
        """
        if self.env.user._is_admin():
            return []
        
        picking_type_ids = self.env.user._get_allowed_picking_type_ids()
        if not picking_type_ids:
            return [('id', '=', False)]
        
        return [('id', 'in', picking_type_ids)]

    # ============================================
    # Constraints & Validation
    # ============================================

    @api.constrains('warehouse_ids')
    def _check_warehouses_active(self):
        """Ensure all assigned warehouses are active."""
        for record in self:
            inactive_wh = record.warehouse_ids.filtered(lambda w: not w.active)
            if inactive_wh:
                raise UserError(_(
                    "Cannot assign inactive warehouse(s): %s\n"
                    "Please activate the warehouse(s) first or remove them from assignment."
                ) % ', '.join(inactive_wh.mapped('name')))

    # ============================================
    # CRUD Overrides (for security logging)
    # ============================================

    def write(self, vals):
        """
        Override write to log warehouse assignment changes.
        
        This helps with auditing who changed whom's warehouse access.
        """
        if 'warehouse_ids' in vals:
            # Snapshot old values before write (supports batch writes)
            old_map = {r.id: set(r.warehouse_ids.mapped('name')) for r in self}
            result = super().write(vals)
            for record in self:
                old_warehouses = old_map.get(record.id, set())
                new_warehouses = set(record.warehouse_ids.mapped('name'))
                if old_warehouses != new_warehouses:
                    body = _(
                        "Warehouse access changed from <b>%s</b> to <b>%s</b> by <b>%s</b>"
                    ) % (
                        ', '.join(sorted(old_warehouses)) if old_warehouses else _('None'),
                        ', '.join(sorted(new_warehouses)) if new_warehouses else _('None'),
                        self.env.user.name,
                    )
                    # res.users is not mail.thread (res.partner is) - post on partner
                    target = record.partner_id if hasattr(record.partner_id, 'message_post') else record
                    try:
                        target.message_post(body=body, message_type='notification')
                    except Exception:
                        pass  # never block write for logging failure
            return result
        
        return super().write(vals)

    # ============================================
    # Utility Methods
    # ============================================

    def action_view_warehouses(self):
        """
        Action to view all warehouses assigned to this user.
        
        Returns:
            dict: Action dictionary for opening warehouse tree view filtered to user's warehouses
        """
        self.ensure_one()
        
        return {
            'name': _('Allowed Warehouses'),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.warehouse',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.warehouse_ids.ids)],
            'context': {'default_user_ids': [(4, self.id)]},
        }

    @api.model
    def get_users_for_warehouse(self, warehouse_id):
        """
        Get all users who have access to a specific warehouse.
        
        Args:
            warehouse_id (int): ID of stock.warehouse
            
        Returns:
            res.users recordset: Users with access to this warehouse
        """
        return self.search([
            ('warehouse_ids', 'in', [warehouse_id]),
            ('active', '=', True),
        ])
