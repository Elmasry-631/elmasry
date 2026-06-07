# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestAdvancedAccounting(TransactionCase):

    def setUp(self):
        super(TestAdvancedAccounting, self).setUp()
        self.company = self.env.ref('base.main_company')
        self.feature = self.env['account.feature'].create({
            'name': 'Test Feature',
            'code': 'TF001',
            'company_id': self.company.id,
        })
        self.cost_center = self.env['account.cost.center'].create({
            'name': 'Test Cost Center',
            'code': 'TCC001',
            'company_id': self.company.id,
        })
        self.patch = self.env['account.patch.number'].create({
            'name': 'PATCH-TEST-001',
            'description': 'Test patch',
            'company_id': self.company.id,
        })
        self.account = self.env['account.account'].create({
            'name': 'Test Account',
            'code': '100001',
            'account_type': 'asset_current',
            'company_id': self.company.id,
        })
        self.journal = self.env['account.journal'].create({
            'name': 'Test Journal',
            'code': 'TJ',
            'type': 'general',
            'company_id': self.company.id,
        })

    def test_feature_creation(self):
        self.assertTrue(self.feature.id)
        self.assertEqual(self.feature.code, 'TF001')

    def test_cost_center_creation(self):
        self.assertTrue(self.cost_center.id)
        self.assertEqual(self.cost_center.code, 'TCC001')

    def test_patch_number_creation(self):
        self.assertTrue(self.patch.id)
        self.assertEqual(self.patch.status, 'draft')

    def test_feature_uniqueness(self):
        with self.assertRaises(ValidationError):
            self.env['account.feature'].create({
                'name': 'Duplicate Feature',
                'code': 'TF001',
                'company_id': self.company.id,
            })

    def test_move_line_dimensions(self):
        move = self.env['account.move'].create({
            'journal_id': self.journal.id,
            'date': '2026-01-01',
            'patch_number_id': self.patch.id,
            'line_ids': [
                (0, 0, {
                    'account_id': self.account.id,
                    'name': 'Test Line',
                    'debit': 100.0,
                    'credit': 0.0,
                    'feature_ids': [(6, 0, [self.feature.id])],
                    'cost_center_ids': [(6, 0, [self.cost_center.id])],
                }),
                (0, 0, {
                    'account_id': self.account.id,
                    'name': 'Test Line 2',
                    'debit': 0.0,
                    'credit': 100.0,
                }),
            ],
        })
        move.action_post()
        line = move.line_ids.filtered(lambda l: l.debit > 0)
        self.assertIn(self.feature, line.feature_ids)
        self.assertIn(self.cost_center, line.cost_center_ids)
        self.assertEqual(move.patch_number_id, self.patch)

    def test_manual_exchange_rate(self):
        currency = self.env['res.currency'].create({
            'name': 'TCC',
            'symbol': 'T',
            'rounding': 0.01,
        })
        move = self.env['account.move'].create({
            'journal_id': self.journal.id,
            'date': '2026-01-01',
            'secondary_currency_id': currency.id,
            'use_manual_rate': True,
            'manual_rate': 2.5,
            'line_ids': [
                (0, 0, {
                    'account_id': self.account.id,
                    'name': 'Test Line',
                    'debit': 100.0,
                    'credit': 0.0,
                }),
                (0, 0, {
                    'account_id': self.account.id,
                    'name': 'Test Line 2',
                    'debit': 0.0,
                    'credit': 100.0,
                }),
            ],
        })
        move.action_post()
        line = move.line_ids.filtered(lambda l: l.debit > 0)
        self.assertEqual(line.secondary_debit, 250.0)
        self.assertEqual(line.secondary_credit, 0.0)
        self.assertEqual(line.secondary_balance, 250.0)

    def test_manual_rate_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['account.move'].create({
                'journal_id': self.journal.id,
                'date': '2026-01-01',
                'use_manual_rate': True,
                'manual_rate': 0.0,
            })

    def test_general_ledger_wizard(self):
        wizard = self.env['general.ledger.wizard'].create({
            'date_from': '2026-01-01',
            'date_to': '2026-12-31',
            'company_id': self.company.id,
        })
        self.assertTrue(wizard.id)
        action = wizard.action_view_report()
        self.assertIn('domain', action)

    def test_trial_balance_wizard(self):
        wizard = self.env['trial.balance.wizard'].create({
            'date_from': '2026-01-01',
            'date_to': '2026-12-31',
            'company_id': self.company.id,
        })
        self.assertTrue(wizard.id)
        action = wizard.action_view_report()
        self.assertIn('context', action)