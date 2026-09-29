from odoo.tests.common import TransactionCase


class TestBudgetCosting(TransactionCase):
    def test_same_product_lines_do_not_overwrite(self):
        Project = self.env['el_construction.project']
        Boq = self.env['el_construction.boq']
        product = self.env['product.product'].create({'name': 'Test Material', 'list_price': 10})
        project = Project.create({'name': 'Costing Test'})
        boq = Boq.create({'project_id': project.id, 'company_id': project.company_id.id})
        self.env['el_construction.boq.line'].create([
            {'boq_id': boq.id, 'product_id': product.id, 'quantity': 2, 'unit_price': 10, 'uom_id': product.uom_id.id},
            {'boq_id': boq.id, 'product_id': product.id, 'quantity': 3, 'unit_price': 10, 'uom_id': product.uom_id.id},
        ])
        boq.action_create_budget()
        budget = self.env['el_construction.budget'].search([
            ('project_id', '=', project.id), ('company_id', '=', project.company_id.id)
        ], limit=1)
        self.assertEqual(len(budget.line_ids), 2)
