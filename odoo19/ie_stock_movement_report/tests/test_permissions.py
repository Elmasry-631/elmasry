"""Permission tests for Stock Movement Report.

Covers (4 methods — STEP 6 requirement):
    1. Manager group can create wizard
    2. Manager group can write wizard
    3. Manager group can delete wizard
    4. User group cannot delete wizard (only managers)
"""

from datetime import date

from odoo.exceptions import AccessError
from odoo.tests import TransactionCase, tagged


@tagged('standard')
class TestStockMovementReportPermissions(TransactionCase):
    """Permission tests — verify group-based access control."""

    def setUp(self):
        """Set up test fixtures with manager and user groups."""
        super().setUp()
        self.Wizard = self.env['stock.movement.report.wizard']
        self.manager_group = self.env.ref(
            'ie_stock_movement_report.group_stock_movement_report_manager'
        )
        self.user_group = self.env.ref(
            'ie_stock_movement_report.group_stock_movement_report_user'
        )
        # Create a test user in the manager group
        self.manager_user = self.env['res.users'].create({
            'name': 'Test Manager',
            'login': 'test_manager_smr',
            'groups_id': [(4, self.manager_group.id)],
        })
        # Create a test user in the user group (not manager)
        self.normal_user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user_smr',
            'groups_id': [(4, self.user_group.id)],
        })

    def test_01_manager_can_create(self):
        """Manager group can create wizard records."""
        wiz = self.Wizard.with_user(self.manager_user).create({
            'date_from': date(2026, 1, 1),
            'date_to': date(2026, 1, 31),
        })
        self.assertTrue(wiz.exists())

    def test_02_manager_can_write(self):
        """Manager group can write wizard records."""
        wiz = self.Wizard.create({
            'date_from': date(2026, 1, 1),
            'date_to': date(2026, 1, 31),
        })
        wiz.with_user(self.manager_user).write({'date_from': date(2026, 2, 1)})
        self.assertEqual(wiz.date_from, date(2026, 2, 1))

    def test_03_manager_can_unlink(self):
        """Manager group can delete wizard records."""
        wiz = self.Wizard.create({
            'date_from': date(2026, 1, 1),
            'date_to': date(2026, 1, 31),
        })
        wiz.with_user(self.manager_user).unlink()
        self.assertFalse(wiz.exists())

    def test_04_user_cannot_unlink(self):
        """User group cannot delete wizard records (only managers)."""
        wiz = self.Wizard.create({
            'date_from': date(2026, 1, 1),
            'date_to': date(2026, 1, 31),
        })
        with self.assertRaises(AccessError):
            wiz.with_user(self.normal_user).unlink()
