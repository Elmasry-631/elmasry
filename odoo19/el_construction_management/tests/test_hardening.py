from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestConstructionHardening(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['el_construction.project'].create({'name': 'Hardening Test'})
        cls.product = cls.env['product.product'].create({'name': 'Construction Product', 'list_price': 100})

    def test_forged_workflow_context_cannot_change_state(self):
        budget = self.env['el_construction.budget'].create({'project_id': self.project.id})
        with self.assertRaises(UserError):
            budget.with_context(_construction_workflow_token='forged').write({'state': 'confirmed'})

    def test_subcontract_line_amount_is_contract_amount(self):
        subcontract = self.env['el_construction.subcontract'].create({
            'project_id': self.project.id,
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        line = self.env['el_construction.subcontract.line'].create({
            'subcontract_id': subcontract.id,
            'work_description': 'Concrete works',
            'quantity': 10,
            'rate': 25,
        })
        self.assertEqual(line.amount, 250)
        self.assertEqual(subcontract.contract_amount, 250)

    def test_subcontract_lines_locked_after_confirmation(self):
        subcontract = self.env['el_construction.subcontract'].create({
            'project_id': self.project.id,
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        self.env['el_construction.subcontract.line'].create({
            'subcontract_id': subcontract.id,
            'work_description': 'Concrete works',
            'quantity': 1,
            'rate': 10,
        })
        subcontract.action_confirm()
        with self.assertRaises(UserError):
            subcontract.line_ids.write({'rate': 20})

    def test_ra_completion_percentage_affects_amount(self):
        subcontract = self.env['el_construction.subcontract'].create({
            'project_id': self.project.id,
            'partner_id': self.env.ref('base.res_partner_1').id,
        })
        self.env['el_construction.subcontract.line'].create({
            'subcontract_id': subcontract.id,
            'work_description': 'Concrete works',
            'quantity': 10,
            'rate': 100,
        })
        ra = self.env['el_construction.ra.billing'].create({'subcontract_id': subcontract.id})
        line = self.env['el_construction.ra.billing.line'].create({
            'ra_billing_id': ra.id,
            'description': 'Concrete works',
            'quantity': 10,
            'rate': 100,
            'completion_percentage': 50,
        })
        self.assertEqual(line.amount, 500)
        self.assertEqual(ra.total_amount, 500)

    def test_invalid_company_reference_is_rejected(self):
        company = self.env['res.company'].create({'name': 'Construction Test Company'})
        other_project = self.env['el_construction.project'].create({'name': 'Other', 'company_id': company.id})
        with self.assertRaises(ValidationError):
            self.env['el_construction.budget'].create({
                'project_id': other_project.id,
                'company_id': self.env.company.id,
            })
