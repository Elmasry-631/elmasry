from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestMaterialRequisition(TransactionCase):
    def test_purchase_order_requires_approval(self):
        project = self.env['el_construction.project'].create({'name': 'MREQ Test'})
        mreq = self.env['el_construction.material.requisition'].create({'project_id': project.id, 'company_id': project.company_id.id})
        with self.assertRaises(UserError):
            mreq.action_create_purchase_order()
