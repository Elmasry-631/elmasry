# -*- coding: utf-8 -*-
from odoo.tests import TransactionCase, tagged
from odoo.exceptions import ValidationError, AccessError
from odoo import fields


@tagged('post_install', '-at_install')
class TestDashboardBuilder(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'email': 'test@example.com',
        })
        cls.manager = cls.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'test_manager',
            'email': 'manager@example.com',
            'groups_id': [(6, 0, [cls.env.ref('dashboard_builder.group_dashboard_manager').id])],
        })
        cls.company = cls.env.company

    def test_dashboard_creation(self):
        """Test creating a dashboard."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Test Dashboard',
            'description': '<p>Test Description</p>',
            'user_id': self.user.id,
            'company_id': self.company.id,
        })
        self.assertEqual(dashboard.name, 'Test Dashboard')
        self.assertEqual(dashboard.user_id, self.user)
        self.assertTrue(dashboard.active)
        self.assertFalse(dashboard.is_public)

    def test_dashboard_duplicate(self):
        """Test duplicating a dashboard."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Original Dashboard',
            'user_id': self.user.id,
        })
        # Add an item
        widget = self.env.ref('dashboard_builder.widget_kpi_card')
        self.env['dashboard.builder.item'].create({
            'dashboard_id': dashboard.id,
            'widget_id': widget.id,
            'pos_x': 0,
            'pos_y': 0,
            'width': 6,
            'height': 4,
        })
        
        duplicated = dashboard.copy({
            'name': 'Duplicated Dashboard',
            'user_id': self.user.id,
        })
        self.assertEqual(duplicated.name, 'Duplicated Dashboard')
        self.assertEqual(len(duplicated.item_ids), 1)
        self.assertEqual(duplicated.item_ids[0].widget_id, widget)

    def test_dashboard_item_creation(self):
        """Test creating dashboard items."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Test Dashboard',
            'user_id': self.user.id,
        })
        widget = self.env.ref('dashboard_builder.widget_kpi_card')
        
        item = self.env['dashboard.builder.item'].create({
            'dashboard_id': dashboard.id,
            'widget_id': widget.id,
            'pos_x': 0,
            'pos_y': 0,
            'width': 6,
            'height': 4,
        })
        self.assertEqual(item.dashboard_id, dashboard)
        self.assertEqual(item.widget_id, widget)
        self.assertEqual(item.pos_x, 0)
        self.assertEqual(item.pos_y, 0)
        self.assertEqual(item.width, 6)
        self.assertEqual(item.height, 4)

    def test_dashboard_item_position_validation(self):
        """Test position validation for dashboard items."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Test Dashboard',
            'user_id': self.user.id,
        })
        widget = self.env.ref('dashboard_builder.widget_kpi_card')
        
        # Test negative X position
        with self.assertRaises(ValidationError):
            self.env['dashboard.builder.item'].create({
                'dashboard_id': dashboard.id,
                'widget_id': widget.id,
                'pos_x': -1,
                'pos_y': 0,
                'width': 6,
                'height': 4,
            })
        
        # Test width exceeding grid
        with self.assertRaises(ValidationError):
            self.env['dashboard.builder.item'].create({
                'dashboard_id': dashboard.id,
                'widget_id': widget.id,
                'pos_x': 8,
                'pos_y': 0,
                'width': 6,  # 8 + 6 = 14 > 12
                'height': 4,
            })

    def test_dashboard_item_onchange_widget(self):
        """Test onchange when widget is selected."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Test Dashboard',
            'user_id': self.user.id,
        })
        widget = self.env.ref('dashboard_builder.widget_kpi_card')
        
        item = self.env['dashboard.builder.item'].new({
            'dashboard_id': dashboard.id,
            'widget_id': widget.id,
        })
        item._onchange_widget_id()
        
        self.assertEqual(item.width, widget.default_width)
        self.assertEqual(item.height, widget.default_height)
        self.assertEqual(item.config, widget.default_config)

    def test_widget_creation(self):
        """Test creating a custom widget."""
        widget = self.env['dashboard.builder.widget'].create({
            'name': 'Custom Widget',
            'xml_id': 'custom_widget',
            'category': 'kpi',
            'icon': 'fa fa-star',
            'color': '#ff0000',
            'component_name': 'CustomWidget',
            'default_width': 4,
            'default_height': 3,
        })
        self.assertEqual(widget.name, 'Custom Widget')
        self.assertEqual(widget.xml_id, 'custom_widget')
        self.assertEqual(widget.category, 'kpi')
        self.assertTrue(widget.is_active)

    def test_widget_xml_id_unique(self):
        """Test XML ID uniqueness constraint."""
        widget1 = self.env['dashboard.builder.widget'].create({
            'name': 'Widget 1',
            'xml_id': 'unique_widget',
            'category': 'kpi',
            'component_name': 'Widget1',
        })
        with self.assertRaises(Exception):  # IntegrityError
            self.env['dashboard.builder.widget'].create({
                'name': 'Widget 2',
                'xml_id': 'unique_widget',
                'category': 'chart',
                'component_name': 'Widget2',
            })

    def test_dashboard_share_creation(self):
        """Test creating a dashboard share."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Shared Dashboard',
            'user_id': self.user.id,
            'is_public': False,
        })
        share = self.env['dashboard.builder.share'].create({
            'dashboard_id': dashboard.id,
            'name': 'Public Link',
            'share_type': 'link',
        })
        self.assertEqual(share.dashboard_id, dashboard)
        self.assertEqual(share.share_type, 'link')
        self.assertTrue(share.access_token)
        self.assertTrue(share.is_active)

    def test_dashboard_share_url(self):
        """Test getting share URL."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Shared Dashboard',
            'user_id': self.user.id,
        })
        share = self.env['dashboard.builder.share'].create({
            'dashboard_id': dashboard.id,
            'name': 'Public Link',
            'share_type': 'link',
        })
        url = share.get_share_url()
        self.assertIn(share.access_token, url)
        self.assertIn('/dashboard/builder/shared/', url)

    def test_dashboard_tag(self):
        """Test dashboard tag creation."""
        tag = self.env['dashboard.builder.tag'].create({
            'name': 'Test Tag',
            'color': 5,
        })
        self.assertEqual(tag.name, 'Test Tag')
        self.assertEqual(tag.color, 5)

    def test_dashboard_favorite(self):
        """Test favorite functionality."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Test Dashboard',
            'user_id': self.user.id,
        })
        self.assertFalse(dashboard.is_favorite)
        
        # Add to favorites
        dashboard.action_toggle_favorite()
        self.assertTrue(dashboard.is_favorite)
        self.assertIn(self.user, dashboard.favorite_user_ids)
        
        # Remove from favorites
        dashboard.action_toggle_favorite()
        self.assertFalse(dashboard.is_favorite)
        self.assertNotIn(self.user, dashboard.favorite_user_ids)

    def test_dashboard_access_rights(self):
        """Test access rights for dashboards."""
        # User dashboard
        user_dashboard = self.env['dashboard.builder'].create({
            'name': 'User Dashboard',
            'user_id': self.user.id,
            'is_public': False,
        })
        
        # Public dashboard
        public_dashboard = self.env['dashboard.builder'].create({
            'name': 'Public Dashboard',
            'user_id': self.manager.id,
            'is_public': True,
        })
        
        # Private dashboard of another user
        private_dashboard = self.env['dashboard.builder'].create({
            'name': 'Private Dashboard',
            'user_id': self.manager.id,
            'is_public': False,
        })
        
        # Test as regular user
        with self.env.user(self.user):
            # Can read own dashboard
            user_dashboard.check_access('read')
            
            # Can read public dashboard
            public_dashboard.check_access('read')
            
            # Cannot read private dashboard of another user
            with self.assertRaises(AccessError):
                private_dashboard.check_access('read')

    def test_dashboard_manager_access(self):
        """Test manager access to all dashboards."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Manager Dashboard',
            'user_id': self.manager.id,
            'is_public': False,
        })
        
        with self.env.user(self.user):
            # Regular user cannot access
            with self.assertRaises(AccessError):
                dashboard.check_access('read')
        
        with self.env.user(self.manager):
            # Manager can access
            dashboard.check_access('read')

    def test_dashboard_export_import(self):
        """Test exporting and importing dashboard configuration."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Export Test Dashboard',
            'user_id': self.user.id,
            'background_color': '#ffffff',
            'refresh_interval': 60,
        })
        widget = self.env.ref('dashboard_builder.widget_kpi_card')
        item = self.env['dashboard.builder.item'].create({
            'dashboard_id': dashboard.id,
            'widget_id': widget.id,
            'pos_x': 0,
            'pos_y': 0,
            'width': 6,
            'height': 4,
            'config': {'model': 'sale.order', 'field': 'amount_total'},
        })
        
        # Export
        config = dashboard.action_export_config()
        self.assertEqual(config['type'], 'ir.actions.act_url')
        
        # Import
        imported = self.env['dashboard.builder'].import_dashboard_config({
            'name': 'Imported Dashboard',
            'layout_config': {},
            'items': [{
                'widget_id': widget.xml_id,
                'position': {'x': 0, 'y': 0, 'w': 6, 'h': 4},
                'config': {'model': 'sale.order', 'field': 'amount_total'},
            }]
        })
        self.assertEqual(imported.name, 'Imported Dashboard')
        self.assertEqual(len(imported.item_ids), 1)
        self.assertEqual(imported.item_ids[0].widget_id, widget)

    def test_dashboard_view_count(self):
        """Test view count increment."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'View Count Test',
            'user_id': self.user.id,
        })
        initial_count = dashboard.view_count
        
        # Simulate view action
        dashboard.write({
            'last_viewed': fields.Datetime.now(),
            'view_count': dashboard.view_count + 1,
        })
        
        self.assertEqual(dashboard.view_count, initial_count + 1)
        self.assertIsNotNone(dashboard.last_viewed)

    def test_layout_config_validation(self):
        """Test layout configuration validation."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Layout Test',
            'user_id': self.user.id,
        })
        
        # Valid layout
        dashboard.write({
            'layout_config': {
                'columns': 12,
                'rowHeight': 100,
                'margin': [10, 10],
                'cols': {'lg': 12, 'md': 10, 'sm': 6, 'xs': 4, 'xxs': 2},
            }
        })
        self.assertEqual(dashboard.layout_config['columns'], 12)
        
        # Invalid layout - missing required keys
        with self.assertRaises(ValidationError):
            dashboard.write({'layout_config': {'columns': 12}})

    def test_dashboard_item_config(self):
        """Test item configuration saving."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'Config Test',
            'user_id': self.user.id,
        })
        widget = self.env.ref('dashboard_builder.widget_kpi_card')
        item = self.env['dashboard.builder.item'].create({
            'dashboard_id': dashboard.id,
            'widget_id': widget.id,
            'pos_x': 0,
            'pos_y': 0,
            'width': 6,
            'height': 4,
        })
        
        # Update config via API
        new_config = {
            'model': 'sale.order',
            'field': 'amount_total',
            'aggregation': 'sum',
            'label': 'Total Revenue',
        }
        item.write({'config': new_config})
        
        self.assertEqual(item.config, new_config)


@tagged('post_install', '-at_install')
class TestDashboardBuilderUI(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user_ui',
            'email': 'test_ui@example.com',
        })

    def test_dashboard_view_action(self):
        """Test dashboard view action."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'UI Test Dashboard',
            'user_id': self.user.id,
        })
        action = dashboard.action_open_dashboard()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertIn(f'/dashboard/builder/{dashboard.id}', action['url'])

    def test_dashboard_edit_action(self):
        """Test dashboard edit action."""
        dashboard = self.env['dashboard.builder'].create({
            'name': 'UI Edit Test',
            'user_id': self.user.id,
        })
        action = dashboard.action_edit_dashboard()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertIn(f'/dashboard/builder/{dashboard.id}/edit', action['url'])

    def test_widget_test_action(self):
        """Test widget test action."""
        widget = self.env.ref('dashboard_builder.widget_kpi_card')
        action = widget.action_test_widget()
        self.assertEqual(action['type'], 'ir.actions.act_url')
        self.assertIn(f'/dashboard/builder/widget/test/{widget.id}', action['url'])

    def test_dashboard_search_filters(self):
        """Test dashboard search filters."""
        dashboard1 = self.env['dashboard.builder'].create({
            'name': 'User Dashboard 1',
            'user_id': self.user.id,
            'is_public': False,
        })
        dashboard2 = self.env['dashboard.builder'].create({
            'name': 'Public Dashboard',
            'user_id': self.env.ref('base.user_root').id,
            'is_public': True,
        })
        
        # Search my dashboards
        my_dashboards = self.env['dashboard.builder'].search([
            ('user_id', '=', self.user.id)
        ])
        self.assertIn(dashboard1, my_dashboards)
        self.assertNotIn(dashboard2, my_dashboards)
        
        # Search public dashboards
        public_dashboards = self.env['dashboard.builder'].search([
            ('is_public', '=', True)
        ])
        self.assertIn(dashboard2, public_dashboards)
        self.assertNotIn(dashboard1, public_dashboards)