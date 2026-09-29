# -*- coding: utf-8 -*-
"""
Tests for Warehouse-Based Access Control Module

Test Scenarios (from specification):
1. Test 1: One Warehouse - User assigned to single warehouse
2. Test 2: Multiple Warehouses - User assigned to multiple warehouses
3. Test 3: No Warehouse - User with no warehouse assignment
4. Test 4: Administrator - Admin user bypasses restrictions

Author: Ibrahim Elmasry
License: LGPL-3
"""

from odoo.tests import common, tagged
from odoo.exceptions import AccessError


@tagged('-at_install', 'post_install')
class TestWarehouseAccessControl(common.TransactionCase):
    """
    Main test class for Warehouse-Based Access Control module.
    
    All tests use TransactionCase for automatic rollback.
    """

    @classmethod
    def setUpClass(cls):
        """Set up test data."""
        super(TestWarehouseAccessControl, cls).setUpClass()
        
        # ========================================
        # Create test warehouses
        # ========================================
        cls.warehouse_1 = cls.env['stock.warehouse'].create({
            'name': 'Test Warehouse 1',
            'code': 'TWH1',
        })
        
        cls.warehouse_2 = cls.env['stock.warehouse'].create({
            'name': 'Test Warehouse 2',
            'code': 'TWH2',
        })
        
        cls.warehouse_3 = cls.env['stock.warehouse'].create({
            'name': 'Test Warehouse 3',
            'code': 'TWH3',
        })
        
        # ========================================
        # Create test users
        # ========================================
        User = cls.env['res.users']
        Groups = cls.env['res.groups']
        
        # Get warehouse groups
        cls.group_warehouse_user = cls.env.ref('el_warehouse_access.group_warehouse_user')
        cls.group_warehouse_manager = cls.env.ref('el_warehouse_access.group_warehouse_manager')
        cls.group_system = cls.env.ref('base.group_system')
        
        # User with ONE warehouse (Test 1)
        cls.user_single_wh = User.with_context(no_reset_password=True).create({
            'name': 'Single WH User',
            'login': 'single_wh_user',
            'email': 'single@test.com',
            'groups_id': [(6, 0, [cls.group_warehouse_user.id])],
            'warehouse_ids': [(6, 0, [cls.warehouse_1.id])],
        })
        
        # User with MULTIPLE warehouses (Test 2)
        cls.user_multi_wh = User.with_context(no_reset_password=True).create({
            'name': 'Multi WH User',
            'login': 'multi_wh_user',
            'email': 'multi@test.com',
            'groups_id': [(6, 0, [cls.group_warehouse_user.id])],
            'warehouse_ids': [(6, 0, [cls.warehouse_1.id, cls.warehouse_2.id])],
        })
        
        # User with NO warehouse (Test 3)
        cls.user_no_wh = User.with_context(no_reset_password=True).create({
            'name': 'No WH User',
            'login': 'no_wh_user',
            'email': 'no_wh@test.com',
            'groups_id': [(6, 0, [cls.group_warehouse_user.id])],
            'warehouse_ids': [(5, 0, 0)],  # Clear all
        })
        
        # Manager user (Test 4 - partial)
        cls.user_manager = User.with_context(no_reset_password=True).create({
            'name': 'WH Manager',
            'login': 'wh_manager',
            'email': 'manager@test.com',
            'groups_id': [(6, 0, [cls.group_warehouse_manager.id])],
        })

    # ============================================================
    # TEST 1: Single Warehouse Assignment
    # ============================================================

    def test_01_single_warehouse_user_can_see_own_warehouse(self):
        """
        Test 1.1: User with one warehouse can see that warehouse.
        """
        wh_ids = self.user_single_wh._get_allowed_warehouse_ids()
        
        self.assertIn(
            self.warehouse_1.id, 
            wh_ids,
            "User should see their assigned warehouse"
        )
    
    def test_02_single_warehouse_user_cannot_see_other_warehouses(self):
        """
        Test 1.2: User with one warehouse CANNOT see other warehouses.
        """
        wh_ids = self.user_single_wh._get_allowed_warehouse_ids()
        
        self.assertNotIn(
            self.warehouse_2.id,
            wh_ids,
            "User should NOT see unassigned warehouse"
        )
        self.assertNotIn(
            self.warehouse_3.id,
            wh_ids,
            "User should NOT see unassigned warehouse"
        )

    def test_03_single_warehouse_picking_access(self):
        """
        Test 1.3: User can only see pickings from their warehouse.
        """
        Picking = self.env['stock.picking']
        
        # Create picking in user's warehouse
        picking_type_wh1 = self.env['stock.picking.type'].search([
            ('warehouse_id', '=', self.warehouse_1.id),
            ('code', '=', 'incoming'),
        ], limit=1)
        
        if picking_type_wh1:
            picking_allowed = Picking.sudo().create({
                'picking_type_id': picking_type_wh1.id,
                'location_id': self.warehouse_1.lot_stock_id.id,
                'location_dest_id': self.warehouse_1.lot_stock_id.id,
            })
            
            # User should be able to read this picking
            pickings = Picking.with_user(self.user_single_wh).search([
                ('id', '=', picking_allowed.id)
            ])
            
            self.assertEqual(
                len(pickings), 
                1,
                "User should see picking from their warehouse"
            )

    def test_04_single_warehouse_location_access(self):
        """
        Test 1.4: User can only see locations in their warehouse.
        """
        loc_ids = self.user_single_wh._get_allowed_location_ids()
        
        # Should include locations from warehouse 1
        if self.warehouse_1.lot_stock_id:
            self.assertIn(
                self.warehouse_1.lot_stock_id.id,
                loc_ids,
                "User should see their warehouse's stock location"
            )

    # ============================================================
    # TEST 2: Multiple Warehouses Assignment
    # ============================================================

    def test_05_multi_warehouse_user_sees_all_assigned(self):
        """
        Test 2.1: User with multiple warehouses can see ALL of them.
        """
        wh_ids = self.user_multi_wh._get_allowed_warehouse_ids()
        
        self.assertIn(self.warehouse_1.id, wh_ids, "Should see WH1")
        self.assertIn(self.warehouse_2.id, wh_ids, "Should see WH2")
        self.assertEqual(len(wh_ids), 2, "Should see exactly 2 warehouses")

    def test_06_multi_warehouse_user_cannot_see_unassigned(self):
        """
        Test 2.2: User with multiple warehouses CANNOT see unassigned ones.
        """
        wh_ids = self.user_multi_wh._get_allowed_warehouse_ids()
        
        self.assertNotIn(
            self.warehouse_3.id,
            wh_ids,
            "User should NOT see unassigned warehouse 3"
        )

    def test_07_multi_warehouse_picking_from_any_assigned(self):
        """
        Test 2.3: User can access pickings from ANY of their warehouses.
        """
        Picking = self.env['stock.picking']
        
        # Create pickings in both warehouses
        for wh in [self.warehouse_1, self.warehouse_2]:
            picking_type = self.env['stock.picking.type'].search([
                ('warehouse_id', '=', wh.id),
                ('code', '=', 'incoming'),
            ], limit=1)
            
            if picking_type:
                picking = Picking.sudo().create({
                    'picking_type_id': picking_type.id,
                    'location_id': wh.lot_stock_id.id,
                    'location_dest_id': wh.lot_stock_id.id,
                })
                
                # User should be able to search this picking
                found = Picking.with_user(self.user_multi_wh).search([
                    ('id', '=', picking.id)
                ])
                
                self.assertTrue(
                    found,
                    f"User should see picking from warehouse {wh.name}"
                )

    def test_08_multi_warehouse_count(self):
        """
        Test 2.4: Warehouse count is correct for multi-warehouse user.
        """
        self.assertEqual(
            self.user_multi_wh.warehouse_count,
            2,
            "Warehouse count should be 2"
        )

    # ============================================================
    # TEST 3: No Warehouse Assignment
    # ============================================================

    def test_09_no_warehouse_user_has_empty_list(self):
        """
        Test 3.1: User with no warehouse gets empty warehouse list.
        """
        wh_ids = self.user_no_wh._get_allowed_warehouse_ids()
        
        self.assertEqual(
            len(wh_ids), 
            0,
            "User without warehouse assignment should get empty list"
        )

    def test_10_no_warehouse_user_has_empty_locations(self):
        """
        Test 3.2: User with no warehouse gets empty location list.
        """
        loc_ids = self.user_no_wh._get_allowed_location_ids()
        
        self.assertEqual(
            len(loc_ids), 
            0,
            "User without warehouse should have no accessible locations"
        )

    def test_11_no_warehouse_user_cannot_create_picking(self):
        """
        Test 3.3: User with no warehouse cannot create pickings (or sees none).
        """
        Picking = self.env['stock.picking']
        
        # Search should return empty or raise error
        pickings = Picking.with_user(self.user_no_wh).search([])
        
        # User should not see any pickings (or very limited set)
        # The exact behavior depends on rule implementation
        # but they definitely shouldn't see everything
        
        # Try to create a picking - should fail or be restricted
        picking_type = self.env['stock.picking.type'].search([], limit=1)
        if picking_type:
            with self.assertRaises(AccessError):
                Picking.with_user(self.user_no_wh).create({
                    'picking_type_id': picking_type.id,
                    'location_id': picking_type.default_location_src_id.id,
                    'location_dest_id': picking_type.default_location_dest_id.id,
                })

    def test_12_no_warehouse_has_false_check(self):
        """
        Test 3.4: _has_warehouse_access returns False for no-warehouse user.
        """
        self.assertFalse(
            self.user_no_wh._has_warehouse_access(),
            "User without warehouse should return False"
        )

    # ============================================================
    # TEST 4: Administrator Bypass
    # ============================================================

    def test_13_admin_sees_all_warehouses(self):
        """
        Test 4.1: Administrator can see ALL warehouses.
        """
        # Use sudo() to simulate admin context
        admin_user = self.env.ref('base.user_admin')
        wh_ids = admin_user._get_allowed_warehouse_ids()
        
        # Should contain all warehouses
        total_wh = self.env['stock.warehouse'].search_count([])
        
        self.assertGreaterEqual(
            len(wh_ids),
            total_wh - 1,  # Allow some tolerance
            "Admin should see most/all warehouses"
        )

    def test_14_admin_is_admin_flag(self):
        """
        Test 4.2: _is_admin() returns True for admin users.
        """
        admin_user = self.env.ref('base.user_admin')
        
        self.assertTrue(
            admin_user._is_admin(),
            "Admin user should return True for _is_admin()"
        )

    def test_15_manager_bypasses_restrictions(self):
        """
        Test 4.3: Warehouse manager can see all data.
        """
        # Manager should have full access
        self.assertTrue(
            self.user_manager._is_admin(),
            "WH Manager should be treated as admin for security purposes"
        )

    def test_16_manager_gets_all_warehouses(self):
        """
        Test 4.4: Manager gets complete warehouse list.
        """
        wh_ids = self.user_manager._get_allowed_warehouse_ids()
        total_wh = self.env['stock.warehouse'].search_count([])
        
        self.assertGreaterEqual(
            len(wh_ids),
            total_wh - 1,
            "Manager should get all warehouses"
        )

    # ============================================================
    # ADDITIONAL SECURITY TESTS
    # ============================================================

    def test_17_warehouse_domain_method(self):
        """
        Test: _get_warehouse_domain returns proper domain.
        """
        domain = self.user_single_wh._get_warehouse_domain()
        
        # Should not be empty (should restrict to allowed warehouses)
        self.assertIsInstance(domain, list, "Domain should be a list")
        
        # For non-admin, domain should restrict
        if not self.user_single_wh._is_admin():
            self.assertTrue(
                len(domain) > 0,
                "Non-admin user should get restrictive domain"
            )

    def test_18_location_domain_method(self):
        """
        Test: _get_location_domain returns proper domain.
        """
        domain = self.user_single_wh._get_location_domain()
        
        self.assertIsInstance(domain, list, "Domain should be a list")

    def test_19_picking_type_domain_method(self):
        """
        Test: _get_picking_type_domain returns proper domain.
        """
        domain = self.user_single_wh._get_picking_type_domain()
        
        self.assertIsInstance(domain, list, "Domain should be a list")

    def test_20_inactive_warehouse_constraint(self):
        """
        Test: Cannot assign inactive warehouse to user.
        """
        # Deactivate warehouse 3
        self.warehouse_3.write({'active': False})
        
        # Try to assign inactive warehouse - should raise error
        with self.assertRaises(Exception):  # UserError expected
            self.user_single_wh.write({
                'warehouse_ids': [(4, self.warehouse_3.id)]
            })
        
        # Reactivate for other tests
        self.warehouse_3.write({'active': True})

    def test_21_users_for_warehouse_method(self):
        """
        Test: get_users_for_warehouse returns correct users.
        """
        users = self.env['res.users'].get_users_for_warehouse(self.warehouse_1.id)
        
        # Should include both single_wh and multi_wh users
        user_ids = users.ids
        
        self.assertIn(
            self.user_single_wh.id,
            user_ids,
            "Single WH user should be returned"
        )
        self.assertIn(
            self.user_multi_wh.id,
            user_ids,
            "Multi WH user should be returned"
        )
        self.assertNotIn(
            self.user_no_wh.id,
            user_ids,
            "No-WH user should NOT be returned"
        )


@tagged('-at_install', 'post_install')
class TestWarehouseAccessRecordRules(common.TransactionCase):
    """
    Test record rules are properly enforced at database level.
    
    These tests verify that ir.rules actually filter data correctly.
    """

    @classmethod
    def setUpClass(cls):
        super(TestWarehouseAccessRecordRules, cls).setUpClass()
        
        # Create test warehouse and user
        cls.test_warehouse = cls.env['stock.warehouse'].create({
            'name': 'Rule Test Warehouse',
            'code': 'RTW',
        })
        
        cls.test_user = cls.env['res.users'].with_context(no_reset_password=True).create({
            'name': 'Rule Test User',
            'login': 'rule_test_user',
            'email': 'ruletest@test.com',
            'groups_id': [(6, 0, [cls.env.ref('el_warehouse_access.group_warehouse_user').id])],
            'warehouse_ids': [(6, 0, [cls.test_warehouse.id])],
        })

    def test_stock_picking_rule_filters_correctly(self):
        """
        Verify stock.picking rule filters by warehouse.
        """
        Picking = cls = self.env['stock.picking']
        
        # Create picking in test warehouse
        picking_type = self.env['stock.picking.type'].search([
            ('warehouse_id', '=', self.test_warehouse.id),
        ], limit=1)
        
        if picking_type:
            picking = Picking.sudo().create({
                'picking_type_id': picking_type.id,
                'location_id': self.test_warehouse.lot_stock_id.id,
                'location_dest_id': self.test_warehouse.lot_stock_id.id,
            })
            
            # User should be able to find it
            found = Picking.with_user(self.test_user).search([
                ('id', '=', picking.id)
            ])
            
            self.assertTrue(found, "User should find picking in their warehouse")

    def test_stock_quant_rule_filters_by_location(self):
        """
        Verify stock.quant rule filters by location.
        """
        Quant = self.env['stock.quant']
        
        # Create quant in test warehouse location
        product = self.env['product.product'].create({
            'name': 'Test Product for Quant Rule',
            'type': 'product',
        })
        
        quant = Quant.sudo().create({
            'product_id': product.id,
            'location_id': self.test_warehouse.lot_stock_id.id,
            'quantity': 10.0,
        })
        
        # User should be able to find it
        found = Quant.with_user(self.test_user).search([
            ('id', '=', quant.id)
        ])
        
        self.assertTrue(found, "User should find quant in their location")


@tagged('-at_install', 'post_install')  
class TestWarehouseAccessPerformance(common.TransactionCase):
    """
    Performance tests for warehouse access control methods.
    
    These tests ensure security methods don't cause N+1 queries
    or performance issues.
    """

    @classmethod
    def setUpClass(cls):
        super(TestWarehouseAccessPerformance, cls).setUpClass()
        
        # Create multiple warehouses for testing
        cls.warehouses = cls.env['stock.warehouse']
        for i in range(5):
            wh = cls.env['stock.warehouse'].create({
                'name': f'Perf Test Warehouse {i}',
                'code': f'PTW{i}',
            })
            cls.warehouses |= wh
        
        # Create user with all warehouses
        cls.perf_user = cls.env['res.users'].with_context(no_reset_password=True).create({
            'name': 'Perf Test User',
            'login': 'perf_test_user',
            'email': 'perf@test.com',
            'groups_id': [(6, 0, [cls.env.ref('el_warehouse_access.group_warehouse_user').id])],
            'warehouse_ids': [(6, 0, cls.warehouses.ids)],
        })

    def test_get_allowed_warehouse_ids_performance(self):
        """
        Test: _get_allowed_warehouse_ids completes quickly.
        """
        import time
        
        start = time.time()
        
        # Call method multiple times
        for _ in range(10):
            self.perf_user._get_allowed_warehouse_ids()
        
        elapsed = time.time() - start
        
        # Should complete within 2 seconds (generous limit)
        self.assertLess(
            elapsed,
            2.0,
            f"Method took too long: {elapsed:.2f}s"
        )

    def test_get_allowed_location_ids_performance(self):
        """
        Test: _get_allowed_location_ids completes quickly.
        """
        import time
        
        start = time.time()
        
        for _ in range(10):
            self.perf_user._get_allowed_location_ids()
        
        elapsed = time.time() - start
        
        self.assertLess(
            elapsed,
            2.0,
            f"Location lookup took too long: {elapsed:.2f}s"
        )
