from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestConstructionTask(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Project = cls.env['el_construction.project']
        cls.Task = cls.env['el_construction.task']
        cls.Timesheet = cls.env['el_construction.timesheet']
        cls.Employee = cls.env['hr.employee']
        cls.project = cls.Project.create({
            'name': 'Task Test Project',
            'company_id': cls.env.company.id,
        })

    def _employee(self, name='Task Employee'):
        return self.Employee.create({'name': name, 'company_id': self.env.company.id})

    def test_workflow_transitions_and_guards(self):
        task = self.Task.create({'name': 'Workflow Task', 'project_id': self.project.id})
        self.assertEqual(task.state, 'draft')
        task.action_start()
        self.assertEqual(task.state, 'in_progress')
        self.assertTrue(task.date_start)
        with self.assertRaises(UserError):
            task.action_done()
        task.write({'progress': 100.0})
        task.action_done()
        self.assertEqual(task.state, 'done')
        self.assertEqual(task.progress, 100.0)
        with self.assertRaises(UserError):
            task.write({'state': 'draft'})

    def test_cancel_and_reset_workflow(self):
        task = self.Task.create({'name': 'Cancel Reset', 'project_id': self.project.id})
        task.action_cancel()
        self.assertEqual(task.state, 'cancelled')
        with self.assertRaises(UserError):
            task.write({'name': 'Must Stay Locked'})
        task.action_reset_draft()
        self.assertEqual(task.state, 'draft')
        task.write({'name': 'Editable Again'})

    def test_direct_state_write_is_blocked(self):
        task = self.Task.create({'name': 'Direct State Task', 'project_id': self.project.id})
        with self.assertRaises(UserError):
            task.write({'state': 'in_progress'})

    def test_invalid_subproject_is_blocked(self):
        other = self.Project.create({'name': 'Other Project', 'company_id': self.env.company.id})
        sub = self.env['el_construction.sub.project'].create({
            'name': 'Other Sub Project',
            'project_id': other.id,
            'company_id': self.env.company.id,
        })
        with self.assertRaises(ValidationError):
            self.Task.create({
                'name': 'Invalid Task',
                'project_id': self.project.id,
                'sub_project_id': sub.id,
            })

    def test_progress_and_remaining_hours(self):
        task = self.Task.create({
            'name': 'Hours Task',
            'project_id': self.project.id,
            'planned_hours': 10,
        })
        self.Timesheet.create({
            'task_id': task.id,
            'employee_id': self._employee().id,
            'date': fields.Date.today(),
            'hours': 4,
            'state': 'done',
        })
        task.invalidate_recordset()
        self.assertEqual(task.total_hours, 4)
        self.assertEqual(task.progress, 40)
        self.assertEqual(task.remaining_hours, 6)

    def test_planned_hours_completion_uses_actual_logged_hours(self):
        task = self.Task.create({
            'name': 'Planned Completion',
            'project_id': self.project.id,
            'planned_hours': 2,
        })
        task.action_start()
        task.write({'progress': 100})
        with self.assertRaises(UserError):
            task.action_done()
        self.Timesheet.create({
            'task_id': task.id,
            'employee_id': self._employee('Planned Employee').id,
            'hours': 2,
            'state': 'done',
        })
        task.invalidate_recordset()
        self.assertEqual(task.progress, 100)
        task.action_done()
        self.assertEqual(task.state, 'done')
        self.assertEqual(task.remaining_hours, 0)

    def test_timer_only_in_progress(self):
        task = self.Task.create({'name': 'Timer Guard', 'project_id': self.project.id})
        with self.assertRaises(UserError):
            task.action_timer_start()

    def test_timer_lifecycle(self):
        task = self.Task.create({'name': 'Timer Lifecycle', 'project_id': self.project.id})
        task.action_start()
        task.action_timer_start()
        self.assertTrue(task.is_timer_running)
        self.assertEqual(task.current_timesheet_id.state, 'running')
        task.action_timer_stop()
        self.assertFalse(task.is_timer_running)
        self.assertFalse(task.current_timesheet_id)
        self.assertEqual(task.timesheet_ids[-1].state, 'done')
        self.assertGreater(task.timesheet_ids[-1].hours, 0)

    def test_running_timesheet_cannot_be_created_directly(self):
        task = self.Task.create({'name': 'Running Guard', 'project_id': self.project.id})
        with self.assertRaises(UserError):
            self.Timesheet.create({
                'task_id': task.id,
                'employee_id': self._employee('Running Employee').id,
                'hours': 0,
                'state': 'running',
            })

    def test_timesheet_cannot_be_added_to_closed_task(self):
        task = self.Task.create({'name': 'Closed Task', 'project_id': self.project.id})
        task.action_start()
        task.write({'progress': 100})
        task.action_done()
        with self.assertRaises(UserError):
            self.Timesheet.create({
                'task_id': task.id,
                'employee_id': self._employee('Closed Employee').id,
                'hours': 1,
                'state': 'done',
            })

    def test_completed_task_cannot_be_deleted(self):
        task = self.Task.create({'name': 'Delete Guard', 'project_id': self.project.id})
        task.action_start()
        task.write({'progress': 100})
        task.action_done()
        with self.assertRaises(UserError):
            task.unlink()

class TestConstructionTaskGanttDependencies(TransactionCase):
    """Regression tests for Task Gantt dependency integrity."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project = cls.env['el_construction.project'].create({
            'name': 'Gantt Project',
            'company_id': cls.env.company.id,
        })

    def _task(self, name, start, end):
        return self.env['el_construction.task'].create({
            'name': name,
            'project_id': self.project.id,
            'company_id': self.env.company.id,
            'date_start': start,
            'date_end': end,
        })

    def test_finish_to_start_dependency_is_allowed(self):
        predecessor = self._task('Excavation', '2026-09-01', '2026-09-05')
        successor = self._task('Foundation', '2026-09-05', '2026-09-10')
        successor.predecessor_ids = [(4, predecessor.id)]
        self.assertIn(predecessor, successor.predecessor_ids)
        self.assertIn(successor, predecessor.successor_ids)

    def test_dependency_rejects_early_successor(self):
        predecessor = self._task('Excavation', '2026-09-01', '2026-09-05')
        successor = self._task('Foundation', '2026-09-04', '2026-09-10')
        with self.assertRaises(ValidationError):
            successor.predecessor_ids = [(4, predecessor.id)]

    def test_dependency_rejects_cross_project(self):
        other_project = self.env['el_construction.project'].create({
            'name': 'Other Project',
            'company_id': self.env.company.id,
        })
        predecessor = self._task('Excavation', '2026-09-01', '2026-09-05')
        successor = self.env['el_construction.task'].create({
            'name': 'Foundation',
            'project_id': other_project.id,
            'company_id': self.env.company.id,
            'date_start': '2026-09-05',
            'date_end': '2026-09-10',
        })
        with self.assertRaises(ValidationError):
            successor.predecessor_ids = [(4, predecessor.id)]

    def test_dependency_rejects_cycle(self):
        first = self._task('Excavation', '2026-09-01', '2026-09-05')
        second = self._task('Foundation', '2026-09-05', '2026-09-10')
        second.predecessor_ids = [(4, first.id)]
        # A reverse dependency would create a cycle and must be rejected.
        with self.assertRaises(ValidationError):
            first.predecessor_ids = [(4, second.id)]

class TestConstructionTaskAdvancedPlanning(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Project = cls.env['el_construction.project']
        cls.Task = cls.env['el_construction.task']
        cls.project = cls.Project.create({
            'name': 'Advanced Planning Project',
            'company_id': cls.env.company.id,
        })
        cls.manager = cls.env['res.users'].create({
            'name': 'Planning Test Manager',
            'login': 'construction_planning_manager',
            'email': 'construction_planning_manager@example.com',
            'groups_id': [
                (6, 0, [
                    cls.env.ref('base.group_user').id,
                    cls.env.ref('el_construction_management.group_construction_user').id,
                    cls.env.ref('el_construction_management.group_construction_manager').id,
                ])
            ],
        })

    def _task(self, name, start, end):
        return self.Task.create({
            'name': name,
            'project_id': self.project.id,
            'company_id': self.env.company.id,
            'date_start': start,
            'date_end': end,
            'planned_hours': 8,
        })

    def test_baseline_snapshot(self):
        task = self._task('Baseline Task', '2026-10-01', '2026-10-05')
        task.with_user(self.manager).action_set_baseline()
        self.assertTrue(task.baseline_locked)
        self.assertEqual(task.baseline_start, task.date_start)
        self.assertEqual(task.baseline_end, task.date_end)
        self.assertEqual(task.baseline_hours, 8)

    def test_milestone_requires_single_day(self):
        with self.assertRaises(ValidationError):
            self._task('Invalid Milestone', '2026-10-01', '2026-10-02').write({
                'is_milestone': True,
            })

    def test_critical_path_and_slack(self):
        first = self._task('Critical A', '2026-10-01', '2026-10-03')
        second = self._task('Critical B', '2026-10-03', '2026-10-05')
        parallel = self._task('Parallel', '2026-10-01', '2026-10-02')
        second.predecessor_ids = [(4, first.id)]
        first.invalidate_recordset()
        second.invalidate_recordset()
        parallel.invalidate_recordset()
        first._compute_schedule_metrics()
        second._compute_schedule_metrics()
        parallel._compute_schedule_metrics()
        self.assertTrue(first.critical_path)
        self.assertTrue(second.critical_path)
        self.assertGreaterEqual(parallel.schedule_slack_days, 0)

    def test_project_schedule_action(self):
        action = self.project.action_view_task_planning()
        self.assertEqual(action['res_model'], 'el_construction.task')
        self.assertEqual(action['view_mode'], 'gantt')
        self.assertEqual(action['domain'], [('project_id', '=', self.project.id)])

    def test_baseline_and_actual_fields_are_server_protected(self):
        task = self._task('Protected Planning', '2026-10-01', '2026-10-05')
        with self.assertRaises(UserError):
            task.write({'baseline_start': '2026-09-30'})
        with self.assertRaises(UserError):
            task.write({'actual_start_date': '2026-10-01'})

    def test_non_manager_cannot_set_actual_finish_through_done(self):
        user = self.env['res.users'].create({
            'name': 'Planning Regular User',
            'login': 'construction_planning_user',
            'email': 'construction_planning_user@example.com',
            'groups_id': [
                (6, 0, [
                    self.env.ref('base.group_user').id,
                    self.env.ref('el_construction_management.group_construction_user').id,
                ])
            ],
        })
        task = self._task('Protected Actual Finish', '2026-10-01', '2026-10-05')
        task.with_user(user).action_start()
        task.with_user(user).write({'progress': 100})
        with self.assertRaises(Exception):
            task.with_user(user).action_done()
        self.assertFalse(task.actual_end_date)
