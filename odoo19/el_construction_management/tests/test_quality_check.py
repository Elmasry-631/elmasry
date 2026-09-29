from odoo import Command
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestConstructionQualityCheck(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.manager_group = cls.env.ref('el_construction_management.group_construction_manager')
        cls.user_group = cls.env.ref('el_construction_management.group_construction_user')
        cls.project = cls.env['el_construction.project'].create({
            'name': 'QC Test Project',
            'company_id': cls.company.id,
        })
        cls.employee = cls.env['hr.employee'].create({
            'name': 'QC Inspector',
            'company_id': cls.company.id,
        })
        cls.manager = cls.env['res.users'].create({
            'name': 'QC Manager',
            'login': 'qc_manager_test',
            'email': 'qc_manager@example.com',
            'company_id': cls.company.id,
            'company_ids': [Command.link(cls.company.id)],
            'groups_id': [Command.link(cls.manager_group.id)],
        })
        cls.user = cls.env['res.users'].create({
            'name': 'QC User',
            'login': 'qc_user_test',
            'email': 'qc_user@example.com',
            'company_id': cls.company.id,
            'company_ids': [Command.link(cls.company.id)],
            'groups_id': [Command.link(cls.user_group.id)],
        })

    def _make_check(self, **extra):
        vals = {
            'project_id': self.project.id,
            'inspector_id': self.employee.id,
            'check_type': 'workmanship',
            'check_line_ids': [
                Command.create({'name': 'Alignment', 'result': 'na'}),
                Command.create({'name': 'Finish', 'result': 'na'}),
            ],
        }
        vals.update(extra)
        return self.env['el_construction.quality.check'].create(vals)

    def test_workflow_pass_close(self):
        qc = self._make_check()
        qc.action_start()
        qc.check_line_ids.write({'result': 'pass'})
        qc.action_pass()
        self.assertEqual(qc.state, 'pass')
        with self.assertRaises(AccessError):
            qc.with_user(self.user).action_close()
        qc.with_user(self.manager).action_close()
        self.assertEqual(qc.state, 'closed')
        self.assertTrue(qc.closed_date)
        self.assertEqual(qc.closed_by_id, self.manager)

    def test_start_requires_inspector_and_checkpoints(self):
        qc = self.env['el_construction.quality.check'].create({'project_id': self.project.id})
        with self.assertRaises(UserError):
            qc.action_start()
        qc.inspector_id = self.employee
        with self.assertRaises(UserError):
            qc.action_start()

    def test_result_requires_completed_checkpoints(self):
        qc = self._make_check()
        qc.action_start()
        with self.assertRaises(UserError):
            qc.action_pass()
        qc.check_line_ids.write({'result': 'pass'})
        qc.action_pass()
        self.assertEqual(qc.state, 'pass')

    def test_fail_requires_failed_point_action_and_recheck_date(self):
        qc = self._make_check()
        qc.action_start()
        qc.check_line_ids.write({'result': 'pass'})
        qc.result_notes = 'No failure'
        with self.assertRaises(UserError):
            qc.action_fail()
        qc.check_line_ids[0].result = 'fail'
        with self.assertRaises(UserError):
            qc.action_fail()
        qc.corrective_action = 'Repair and retest.'
        with self.assertRaises(UserError):
            qc.action_fail()
        qc.recheck_date = '2026-09-10'
        qc.action_fail()
        self.assertEqual(qc.state, 'fail')
        qc.action_recheck()
        self.assertEqual(qc.state, 'recheck')

    def test_reinspection_can_pass(self):
        qc = self._make()
        qc.action_start()
        qc.check_line_ids[0].result = 'fail'
        qc.check_line_ids[1].result = 'pass'
        qc.corrective_action = 'Repair defect.'
        qc.recheck_date = '2026-09-10'
        qc.action_fail()
        qc.action_recheck()
        qc.check_line_ids[0].result = 'pass'
        qc.action_pass()
        self.assertEqual(qc.state, 'pass')

    def test_direct_state_change_is_blocked(self):
        qc = self._make()
        with self.assertRaises(UserError):
            qc.write({'state': 'in_progress'})

    def test_closed_quality_check_is_read_only(self):
        qc = self._make()
        qc.action_start()
        qc.check_line_ids.write({'result': 'pass'})
        qc.action_pass()
        qc.with_user(self.manager).action_close()
        with self.assertRaises(UserError):
            qc.write({'result_notes': 'changed'})
        with self.assertRaises(ValidationError):
            qc.check_line_ids[0].write({'remarks': 'changed'})

    def test_cancel_and_reset_are_manager_only(self):
        qc = self._make()
        with self.assertRaises(AccessError):
            qc.with_user(self.user).action_cancel()
        qc.with_user(self.manager).action_cancel()
        self.assertEqual(qc.state, 'cancelled')
        with self.assertRaises(AccessError):
            qc.with_user(self.user).action_reset_draft()
        qc.with_user(self.manager).action_reset_draft()
        self.assertEqual(qc.state, 'draft')
