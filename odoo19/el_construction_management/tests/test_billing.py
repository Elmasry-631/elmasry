from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestBilling(TransactionCase):
    def test_progress_billing_requires_in_progress_for_invoice(self):
        project = self.env['el_construction.project'].create({'name': 'Billing Test'})
        billing = self.env['el_construction.progress.billing'].create({'name': 'Test Billing', 'project_id': project.id, 'company_id': project.company_id.id})
        with self.assertRaises(UserError):
            billing.action_create_invoice()
