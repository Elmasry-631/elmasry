from odoo.exceptions import AccessError, UserError
from odoo.tests.common import TransactionCase


class TestConstructionWorkflow(TransactionCase):
    def test_budget_direct_state_write_is_blocked(self):
        Project = self.env['el_construction.project']
        project = Project.create({'name': 'Workflow Test'})
        budget = self.env['el_construction.budget'].create({'project_id': project.id, 'company_id': project.company_id.id})
        with self.assertRaises(UserError):
            budget.write({'state': 'approved'})
        budget.action_confirm()
        with self.assertRaises(AccessError):
            budget.action_approve()
