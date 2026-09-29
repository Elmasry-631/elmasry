from odoo import Command
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestRound2Hardening(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['el_construction.project'].create({
            'name': 'Round 2 Test Project',
            'company_id': cls.env.company.id,
        })
        cls.vendor = cls.env['res.partner'].create({
            'name': 'Round 2 Vendor',
            'supplier_rank': 1,
        })
        cls.manager = cls.env['res.users'].create({
            'name': 'Construction Test Manager',
            'login': 'construction_test_manager_round2',
            'email': 'construction_test_manager_round2@example.com',
            'groups_id': [Command.set([
                cls.env.ref('base.group_user').id,
                cls.env.ref('el_construction_management.group_construction_user').id,
                cls.env.ref('el_construction_management.group_construction_manager').id,
            ])],
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Round 2 Product',
            'type': 'consu',
        })

    def test_mreq_rejects_partial_vendor_assignment(self):
        req = self.env['el_construction.material.requisition'].create({
            'project_id': self.project.id,
            'company_id': self.env.company.id,
            'line_ids': [
                Command.create({
                    'product_id': self.product.id, 'quantity': 1,
                    'uom_id': self.product.uom_id.id, 'vendor_id': self.vendor.id,
                }),
                Command.create({
                    'product_id': self.product.id, 'quantity': 1,
                    'uom_id': self.product.uom_id.id,
                }),
            ],
        })
        req.action_submit_approval()
        req = req.with_user(self.manager)
        req.action_approve()
        with self.assertRaises(UserError):
            req.action_create_purchase_order()

    def test_work_order_other_line_is_in_total(self):
        wo = self.env['el_construction.work.order'].create({
            'project_id': self.project.id,
            'company_id': self.env.company.id,
        })
        self.env['el_construction.work.order.line'].create({
            'work_order_id': wo.id, 'line_type': 'other',
            'quantity': 2, 'unit_price': 25,
        })
        self.assertEqual(wo.other_total, 50)
        self.assertEqual(wo.total_amount, 50)

    def test_ra_billing_numbers_increment_per_subcontract(self):
        subcontract = self.env['el_construction.subcontract'].create({
            'name': 'RA Numbering Test',
            'project_id': self.project.id,
            'company_id': self.env.company.id,
            'partner_id': self.vendor.id,
        })
        ra1, ra2 = self.env['el_construction.ra.billing'].create([
            {'subcontract_id': subcontract.id},
            {'subcontract_id': subcontract.id},
        ])
        self.assertEqual(ra2.billing_no, ra1.billing_no + 1)

    def test_ra_billing_line_parent_is_required(self):
        with self.assertRaises(Exception):
            self.env['el_construction.ra.billing.line'].create({
                'description': 'Orphan', 'quantity': 1, 'rate': 1,
            })
