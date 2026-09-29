from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestBudgetMethods(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['el_construction.project'].create({'name': 'Budget Methods Test'})
        cls.product = cls.env['product.product'].create({
            'name': 'Budget Test Product',
            'list_price': 100,
        })

    def _budget(self, **vals):
        values = {'project_id': self.project.id}
        values.update(vals)
        return self.env['el_construction.budget'].create(values)

    def test_project_total_budget(self):
        budget = self._budget(budget_method='project', project_budget_amount=100000)
        self.assertEqual(budget.total_planned, 100000)
        self.assertEqual(budget.allocated_amount, 0)
        self.assertEqual(budget.unallocated_amount, 100000)
        self.assertEqual(budget.allocation_percentage, 0)
        with self.assertRaises(UserError):
            self.env['el_construction.budget.line'].create({
                'budget_id': budget.id,
                'description': 'Should not be allowed',
                'planned_amount': 1000,
            })
        budget.action_confirm()

    def test_lines_budget(self):
        budget = self._budget(budget_method='lines')
        self.env['el_construction.budget.line'].create({
            'budget_id': budget.id,
            'product_id': self.product.id,
            'uom_id': self.product.uom_id.id,
            'quantity': 10,
            'unit_price': 100,
            'planned_amount': 1000,
        })
        self.assertEqual(budget.total_planned, 1000)
        self.assertEqual(budget.allocated_amount, 1000)
        self.assertEqual(budget.unallocated_amount, 0)
        self.assertEqual(budget.allocation_percentage, 100)
        budget.action_confirm()

    def test_hybrid_budget_tracks_unallocated_balance(self):
        budget = self._budget(budget_method='hybrid', project_budget_amount=10000)
        self.env['el_construction.budget.line'].create({
            'budget_id': budget.id,
            'description': 'Concrete',
            'planned_amount': 6000,
        })
        self.assertEqual(budget.total_planned, 10000)
        self.assertEqual(budget.allocated_amount, 6000)
        self.assertEqual(budget.unallocated_amount, 4000)
        self.assertEqual(budget.allocation_percentage, 60)
        budget.action_confirm()

    def test_hybrid_cannot_over_allocate(self):
        budget = self._budget(budget_method='hybrid', project_budget_amount=10000)
        with self.assertRaises(ValidationError):
            self.env['el_construction.budget.line'].create({
                'budget_id': budget.id,
                'description': 'Over allocation',
                'planned_amount': 10001,
            })

    def test_lines_method_rejects_project_amount(self):
        with self.assertRaises(ValidationError):
            self._budget(budget_method='lines', project_budget_amount=1)

    def test_project_and_hybrid_require_project_amount(self):
        with self.assertRaises(ValidationError):
            self._budget(budget_method='project')
        with self.assertRaises(ValidationError):
            self._budget(budget_method='hybrid')
