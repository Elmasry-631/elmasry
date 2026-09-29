import secrets
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from .workflow_mixin import ConstructionWorkflowMixin

_TASK_TIMER_TOKEN = secrets.token_urlsafe(32)
_TASK_PLANNING_TOKEN = secrets.token_urlsafe(32)


class ConstructionTask(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.task'
    _description = 'Construction Task'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence, id'

    _TASK_STATES = {
        'draft': {'in_progress', 'cancelled'},
        'in_progress': {'done', 'cancelled'},
        'cancelled': {'draft'},
        'done': set(),
    }

    name = fields.Char(string='Task Name', required=True, tracking=True)
    reference = fields.Char(string='Reference', readonly=True, default='New', copy=False, index=True)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True, index=True, ondelete='restrict')
    sub_project_id = fields.Many2one('el_construction.sub.project', string='Sub Project', index=True, ondelete='restrict')
    phase_id = fields.Many2one('el_construction.phase', string='Phase', index=True, ondelete='restrict')
    work_order_id = fields.Many2one('el_construction.work.order', string='Work Order', index=True, ondelete='restrict')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company, index=True, ondelete='restrict')

    sequence = fields.Integer(string='Sequence', default=10)
    description = fields.Html(string='Description')
    assigned_to = fields.Many2one('hr.employee', string='Assigned To', index=True, ondelete='restrict')
    department_id = fields.Many2one('hr.department', string='Department', ondelete='restrict')
    date_start = fields.Date(string='Start Date')
    date_end = fields.Date(string='End Date')
    date_deadline = fields.Date(string='Deadline', index=True)
    priority = fields.Selection([
        ('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Urgent'),
    ], string='Priority', default='0', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'), ('in_progress', 'In Progress'),
        ('done', 'Done'), ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True, copy=False)
    progress = fields.Float(
        string='Progress (%)', compute='_compute_progress', store=True, readonly=False,
        help='If Planned Hours is set, progress is calculated from timesheet hours. Otherwise it can be entered manually.'
    )
    planned_hours = fields.Float(string='Planned Hours', default=0.0)
    remaining_hours = fields.Float(string='Remaining Hours', compute='_compute_remaining', store=True, readonly=True)

    is_timer_running = fields.Boolean(string='Timer Running', default=False, copy=False, readonly=True)
    timer_start = fields.Datetime(string='Timer Started At', copy=False, readonly=True)
    current_timesheet_id = fields.Many2one(
        'el_construction.timesheet', string='Running Timesheet',
        copy=False, readonly=True, ondelete='set null'
    )
    timesheet_ids = fields.One2many('el_construction.timesheet', 'task_id', string='Timesheets')

    # Gantt / planning dependencies. A dependency is Finish-to-Start:
    # a successor should not start before its predecessor finishes.
    predecessor_ids = fields.Many2many(
        'el_construction.task',
        'el_construction_task_dependency_rel',
        'successor_id',
        'predecessor_id',
        string='Blocked By',
        help='Tasks that must be completed before this Task can start.',
    )
    successor_ids = fields.Many2many(
        'el_construction.task',
        'el_construction_task_dependency_rel',
        'predecessor_id',
        'successor_id',
        string='Blocking Tasks',
        help='Tasks that depend on this Task.',
    )
    dependency_count = fields.Integer(
        string='Blocked By Count', compute='_compute_dependency_counts',
    )
    successor_count = fields.Integer(
        string='Blocking Task Count', compute='_compute_dependency_counts',
    )
    total_hours = fields.Float(string='Total Hours', compute='_compute_total_hours', store=True, readonly=True)

    # Advanced project-planning controls. The baseline is a frozen snapshot of the
    # approved plan; current dates remain editable until the task is closed.
    baseline_start = fields.Date(string='Baseline Start', copy=False, readonly=True)
    baseline_end = fields.Date(string='Baseline End', copy=False, readonly=True)
    baseline_hours = fields.Float(string='Baseline Hours', copy=False, readonly=True)
    baseline_locked = fields.Boolean(string='Baseline Locked', copy=False, readonly=True)
    baseline_set_on = fields.Datetime(string='Baseline Set On', copy=False, readonly=True)
    actual_start_date = fields.Date(string='Actual Start', copy=False, readonly=True)
    actual_end_date = fields.Date(string='Actual Finish', copy=False, readonly=True)
    baseline_variance_days = fields.Integer(
        string='Baseline Finish Variance (Days)', compute='_compute_schedule_metrics',
    )
    baseline_start_variance_days = fields.Integer(
        string='Baseline Start Variance (Days)', compute='_compute_schedule_metrics',
    )
    schedule_slack_days = fields.Integer(
        string='Schedule Slack (Days)', compute='_compute_schedule_metrics',
    )
    schedule_slack_hours = fields.Float(
        string='Schedule Slack (Hours)', compute='_compute_schedule_metrics',
    )
    critical_path = fields.Boolean(
        string='Critical Path', compute='_compute_schedule_metrics', search='_search_critical_path',
    )
    schedule_health = fields.Selection([
        ('no_schedule', 'No Schedule'),
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('delayed', 'Delayed'),
        ('completed', 'Completed'),
    ], string='Schedule Health', compute='_compute_schedule_metrics', search='_search_schedule_health')
    delay_days = fields.Integer(string='Delay (Days)', compute='_compute_schedule_metrics')
    is_milestone = fields.Boolean(string='Milestone', default=False, tracking=True)
    notes = fields.Text(string='Notes')

    _reference_unique = models.Constraint(
        'UNIQUE(reference)',
        'Task Reference must be unique.',
    )
    _sequence_non_negative = models.Constraint(
        'CHECK(sequence >= 0)',
        'Task Sequence cannot be negative.',
    )

    @api.depends('name', 'reference')
    def _compute_display_name(self):
        for rec in self:
            if rec.reference and rec.reference != 'New' and rec.name:
                rec.display_name = f'[{rec.reference}] {rec.name}'
            elif rec.name:
                rec.display_name = rec.name
            elif rec.reference and rec.reference != 'New':
                rec.display_name = rec.reference
            else:
                rec.display_name = _('Task #%s') % rec.id

    @api.constrains('project_id', 'sub_project_id', 'phase_id', 'work_order_id', 'company_id', 'assigned_to', 'department_id')
    def _check_consistency(self):
        for rec in self:
            if rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Task company must match the project company.'))
            if rec.sub_project_id:
                if rec.sub_project_id.project_id != rec.project_id:
                    raise ValidationError(_('Sub Project must belong to the selected Project.'))
                if rec.sub_project_id.company_id != rec.company_id:
                    raise ValidationError(_('Task company must match the sub-project company.'))
            if rec.phase_id:
                if rec.phase_id.project_id != rec.project_id:
                    raise ValidationError(_('Phase must belong to the selected Project.'))
                if rec.sub_project_id and rec.phase_id.sub_project_id and rec.phase_id.sub_project_id != rec.sub_project_id:
                    raise ValidationError(_('Phase must belong to the selected Sub Project.'))
                if rec.phase_id.company_id != rec.company_id:
                    raise ValidationError(_('Task company must match the phase company.'))
            if rec.work_order_id:
                if rec.work_order_id.project_id != rec.project_id:
                    raise ValidationError(_('Work Order must belong to the selected Project.'))
                if rec.sub_project_id and rec.work_order_id.sub_project_id and rec.work_order_id.sub_project_id != rec.sub_project_id:
                    raise ValidationError(_('Work Order must belong to the selected Sub Project.'))
                if rec.phase_id and rec.work_order_id.phase_id and rec.work_order_id.phase_id != rec.phase_id:
                    raise ValidationError(_('Work Order must belong to the selected Phase.'))
                if rec.work_order_id.company_id != rec.company_id:
                    raise ValidationError(_('Task company must match the work order company.'))
            if rec.assigned_to and rec.assigned_to.company_id and rec.assigned_to.company_id != rec.company_id:
                raise ValidationError(_('Assigned Employee must belong to the Task company.'))
            if rec.department_id and rec.department_id.company_id and rec.department_id.company_id != rec.company_id:
                raise ValidationError(_('Department must belong to the Task company.'))

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if not self.project_id:
            self.sub_project_id = self.phase_id = self.work_order_id = False
            return
        if self.sub_project_id and self.sub_project_id.project_id != self.project_id:
            self.sub_project_id = False
        if self.phase_id and self.phase_id.project_id != self.project_id:
            self.phase_id = False
        if self.work_order_id and self.work_order_id.project_id != self.project_id:
            self.work_order_id = False

    @api.onchange('sub_project_id')
    def _onchange_sub_project_id(self):
        if self.sub_project_id and self.sub_project_id.project_id != self.project_id:
            self.sub_project_id = False
        if self.phase_id and self.sub_project_id and self.phase_id.sub_project_id and self.phase_id.sub_project_id != self.sub_project_id:
            self.phase_id = False
        if self.work_order_id and self.sub_project_id and self.work_order_id.sub_project_id and self.work_order_id.sub_project_id != self.sub_project_id:
            self.work_order_id = False

    @api.onchange('phase_id')
    def _onchange_phase_id(self):
        if self.phase_id and self.phase_id.project_id != self.project_id:
            self.phase_id = False
        if self.work_order_id and self.phase_id and self.work_order_id.phase_id and self.work_order_id.phase_id != self.phase_id:
            self.work_order_id = False

    @api.depends('predecessor_ids', 'successor_ids')
    def _compute_dependency_counts(self):
        for rec in self:
            rec.dependency_count = len(rec.predecessor_ids)
            rec.successor_count = len(rec.successor_ids)

    def _search_critical_path(self, operator, value):
        if operator not in ('=', '!='):
            return [('id', '=', 0)]
        tasks = self.search([])
        tasks._compute_schedule_metrics()
        ids = tasks.filtered(lambda r: bool(r.critical_path) == bool(value)).ids
        if operator == '!=':
            ids = tasks.filtered(lambda r: bool(r.critical_path) != bool(value)).ids
        return [('id', 'in', ids)]

    def _search_schedule_health(self, operator, value):
        if operator not in ('=', '!='):
            return [('id', '=', 0)]
        tasks = self.search([])
        tasks._compute_schedule_metrics()
        if operator == '=':
            ids = tasks.filtered(lambda r: r.schedule_health == value).ids
        else:
            ids = tasks.filtered(lambda r: r.schedule_health != value).ids
        return [('id', 'in', ids)]

    def _planning_tasks(self):
        self.ensure_one()
        return self.search([('project_id', '=', self.project_id.id)])

    def _compute_schedule_metrics(self):
        today = fields.Date.context_today(self)
        # Cache the network calculation once per project for the whole recordset.
        project_cache = {}
        for task in self:
            task.baseline_variance_days = 0
            task.baseline_start_variance_days = 0
            task.schedule_slack_days = 0
            task.schedule_slack_hours = 0.0
            task.critical_path = False
            task.delay_days = 0
            if task.state == 'done':
                task.schedule_health = 'completed'
            elif not task.date_start or not task.date_end:
                task.schedule_health = 'no_schedule'
            elif task.state == 'in_progress' and task.date_end < today:
                task.delay_days = (today - task.date_end).days
                task.schedule_health = 'delayed'
            elif task.state == 'in_progress' and task.date_deadline and task.date_deadline < today:
                task.delay_days = (today - task.date_deadline).days
                task.schedule_health = 'delayed'
            elif task.state == 'in_progress' and (
                task.date_end <= today + timedelta(days=2)
                or (task.date_deadline and task.date_deadline <= today + timedelta(days=2) and task.date_deadline >= today)
            ):
                task.schedule_health = 'at_risk'
            else:
                task.schedule_health = 'on_track'

            if task.baseline_start and task.actual_start_date:
                task.baseline_start_variance_days = (task.actual_start_date - task.baseline_start).days
            elif task.baseline_start and task.state == 'in_progress':
                task.baseline_start_variance_days = max((today - task.baseline_start).days, 0)
            if task.baseline_end and task.actual_end_date:
                task.baseline_variance_days = (task.actual_end_date - task.baseline_end).days
            elif task.baseline_end and task.state == 'in_progress':
                task.baseline_variance_days = max((today - task.baseline_end).days, 0)

            if not task.date_start or not task.date_end or task.state == 'cancelled':
                continue

            project_id = task.project_id.id
            if project_id not in project_cache:
                tasks = task._planning_tasks().filtered(
                    lambda r: r.date_start and r.date_end and r.state != 'cancelled'
                )
                by_id = {r.id: r for r in tasks}
                indegree = {
                    r.id: len([p.id for p in r.predecessor_ids if p.id in by_id])
                    for r in tasks
                }
                queue = [rid for rid, degree in indegree.items() if degree == 0]
                order = []
                while queue:
                    rid = queue.pop(0)
                    order.append(rid)
                    for succ in by_id[rid].successor_ids.filtered(lambda r: r.id in by_id):
                        indegree[succ.id] -= 1
                        if indegree[succ.id] == 0:
                            queue.append(succ.id)
                if len(order) != len(by_id):
                    project_cache[project_id] = {}
                    continue

                # CPM using the current planned dates as the schedule baseline.
                # This deliberately does not move user-entered dates; it only
                # measures float against the current project finish.
                project_finish = max(r.date_end for r in tasks)
                latest_start = {}
                for rid in reversed(order):
                    rec = by_id[rid]
                    successors = [latest_start[s.id] for s in rec.successor_ids if s.id in latest_start]
                    latest_finish = min(successors) if successors else project_finish
                    latest_start[rid] = latest_finish - (rec.date_end - rec.date_start)
                metrics = {}
                for rec in tasks:
                    slack = max((latest_start[rec.id] - rec.date_start).days, 0)
                    metrics[rec.id] = (slack, slack == 0)
                project_cache[project_id] = metrics

            metrics = project_cache[project_id]
            if task.id in metrics:
                slack, critical = metrics[task.id]
                task.schedule_slack_days = slack
                task.schedule_slack_hours = slack * 24.0
                task.critical_path = critical

    def action_set_baseline(self):
        self._require_manager()
        for task in self:
            if task.state in ('done', 'cancelled'):
                raise UserError(_('A completed or cancelled Task cannot have its baseline changed.'))
            if not task.date_start or not task.date_end:
                raise UserError(_('A Task must have Start Date and End Date before a baseline can be set.'))
            if task.date_end < task.date_start:
                raise UserError(_('Task End Date cannot be before Start Date.'))
            task.with_context(_construction_task_planning_token=_TASK_PLANNING_TOKEN).write({
                'baseline_start': task.date_start,
                'baseline_end': task.date_end,
                'baseline_hours': task.planned_hours,
                'baseline_locked': True,
                'baseline_set_on': fields.Datetime.now(),
            })
        return True

    def _validate_dependencies(self):
        for task in self:
            if task in task.predecessor_ids or task in task.successor_ids:
                raise ValidationError(_('A Task cannot depend on itself.'))
            if task.predecessor_ids & task.successor_ids:
                raise ValidationError(_('A Task cannot be both a predecessor and successor of the same Task.'))
            for predecessor in task.predecessor_ids:
                if predecessor.company_id != task.company_id:
                    raise ValidationError(_('Task dependencies must stay within the same company.'))
                if predecessor.project_id != task.project_id:
                    raise ValidationError(_('Task dependencies must stay within the same Project.'))
                if predecessor.id == task.id:
                    raise ValidationError(_('A Task cannot depend on itself.'))
                if predecessor.date_end and task.date_start and predecessor.date_end > task.date_start:
                    raise ValidationError(_(
                        'Task %(task)s cannot start before predecessor %(predecessor)s finishes.',
                        task=task.display_name,
                        predecessor=predecessor.display_name,
                    ))

            # Detect cycles by traversing predecessors from the current Task.
            seen = set()
            stack = list(task.predecessor_ids)
            while stack:
                node = stack.pop()
                if node.id in seen:
                    continue
                seen.add(node.id)
                if node.id == task.id:
                    raise ValidationError(_('Circular Task dependencies are not allowed.'))
                stack.extend(node.predecessor_ids)

    @api.constrains('predecessor_ids', 'successor_ids', 'project_id', 'company_id', 'date_start', 'date_end')
    def _check_dependencies(self):
        self._validate_dependencies()
        # Validate affected successors as well because changing a predecessor's
        # dates can invalidate an already stored Finish-to-Start relationship.
        affected = self.mapped('successor_ids')
        if affected:
            affected._validate_dependencies()

    @api.constrains('is_milestone', 'date_start', 'date_end')
    def _check_milestone(self):
        for task in self:
            if task.is_milestone and task.date_start and task.date_end and task.date_start != task.date_end:
                raise ValidationError(_('A milestone must have the same Start Date and End Date.'))

    @api.constrains('date_start', 'date_end', 'date_deadline')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_('End Date must be after Start Date.'))
            if rec.date_deadline and rec.date_start and rec.date_deadline < rec.date_start:
                raise ValidationError(_('Deadline cannot be before Start Date.'))
            if rec.date_deadline and rec.date_end and rec.date_deadline < rec.date_end:
                raise ValidationError(_('Deadline cannot be before End Date.'))

    @api.constrains('planned_hours', 'progress')
    def _check_metrics(self):
        for rec in self:
            if rec.planned_hours < 0:
                raise ValidationError(_('Planned Hours cannot be negative.'))
            if rec.progress < 0 or rec.progress > 100:
                raise ValidationError(_('Progress must be between 0 and 100.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals.setdefault('company_id', self.env.company.id)
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('el_construction.task') or 'New'
        records = super().create(vals_list)
        records._check_consistency()
        records._validate_dependencies()
        return records

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        planning_internal_fields = {
            'baseline_start', 'baseline_end', 'baseline_hours', 'baseline_locked',
            'baseline_set_on', 'actual_start_date', 'actual_end_date',
        }
        if planning_internal_fields.intersection(vals) and self.env.context.get('_construction_task_planning_token') != _TASK_PLANNING_TOKEN:
            raise UserError(_('Baseline and Actual Schedule fields can only be changed by Task planning workflow actions.'))

        timer_fields = {'is_timer_running', 'timer_start', 'current_timesheet_id'}
        for record in self:
            if record.state in ('done', 'cancelled'):
                non_internal_fields = set(vals) - {'state'} - timer_fields
                if non_internal_fields:
                    raise UserError(_('Completed or cancelled Tasks are read-only. Reset the Task to Draft first.'))

        protected_fields = {
            'project_id', 'sub_project_id', 'phase_id', 'work_order_id', 'company_id',
            'assigned_to', 'department_id', 'planned_hours', 'date_start', 'date_end', 'date_deadline',
        }
        if protected_fields.intersection(vals):
            for record in self:
                if record.state in ('done', 'cancelled'):
                    raise UserError(_('Completed or cancelled Tasks cannot have their planning data changed. Reset the Task to Draft first.'))
        timer_fields = {'is_timer_running', 'timer_start', 'current_timesheet_id'}
        if timer_fields.intersection(vals) and not self._timer_write_allowed():
            raise UserError(_('Timer fields can only be changed by the Task timer actions.'))
        res = super().write(vals)
        if protected_fields.intersection(vals):
            self._check_consistency()
        if {'predecessor_ids', 'successor_ids', 'project_id', 'company_id', 'date_start', 'date_end'} & set(vals):
            self._validate_dependencies()
            self.mapped('successor_ids')._validate_dependencies()
        return res

    def unlink(self):
        for record in self:
            if record.state != 'draft':
                raise UserError(_('Only Draft Tasks can be deleted.'))
            if record.is_timer_running or record.timesheet_ids:
                raise UserError(_('A Task with timer activity or timesheets cannot be deleted.'))
        return super().unlink()

    def _timer_write_allowed(self):
        return self.env.context.get('_construction_task_timer_token') == _TASK_TIMER_TOKEN

    @api.depends('timesheet_ids.hours', 'timesheet_ids.state')
    def _compute_total_hours(self):
        for rec in self:
            rec.total_hours = sum(rec.timesheet_ids.filtered(lambda ts: ts.state == 'done').mapped('hours'))

    @api.depends('total_hours', 'planned_hours', 'state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'done':
                rec.progress = 100.0
            elif rec.planned_hours > 0:
                rec.progress = min(100.0, round(rec.total_hours / rec.planned_hours * 100, 2))

    @api.depends('planned_hours', 'total_hours', 'state')
    def _compute_remaining(self):
        for rec in self:
            rec.remaining_hours = 0.0 if rec.state == 'done' else (
                max(0.0, rec.planned_hours - rec.total_hours) if rec.planned_hours else 0.0
            )

    def action_start(self):
        self._transition('in_progress', self._TASK_STATES)
        today = fields.Date.context_today(self)
        for task in self:
            vals = {}
            if not task.date_start:
                vals['date_start'] = today
            if not task.actual_start_date:
                vals['actual_start_date'] = today
            if vals:
                task.with_context(_construction_task_planning_token=_TASK_PLANNING_TOKEN).write(vals)
        return True

    def action_done(self):
        self.ensure_one()
        if self.is_timer_running:
            raise UserError(_('Stop the running timer before completing the Task.'))
        if self.planned_hours > 0:
            if self.total_hours < self.planned_hours:
                raise UserError(_('A Task with Planned Hours can only be completed when logged hours reach the Planned Hours.'))
        elif self.progress < 100.0:
            raise UserError(_('A Task can only be completed when Progress is 100%.'))
        self._require_manager()
        self.with_context(_construction_task_planning_token=_TASK_PLANNING_TOKEN).write({
            'actual_end_date': fields.Date.context_today(self),
        })
        self._transition('done', self._TASK_STATES, manager=True)
        return True

    def action_cancel(self):
        self._transition('cancelled', self._TASK_STATES, manager=True)
        self.filtered(lambda r: r.is_timer_running).action_timer_stop()
        return True

    def action_reset_draft(self):
        self.ensure_one()
        if self.is_timer_running:
            raise UserError(_('Stop the running timer before resetting the Task to Draft.'))
        self._transition('draft', self._TASK_STATES, manager=True)
        return True

    def action_timer_start(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('The Task timer can only be started while the Task is In Progress.'))
        self._lock_records()
        self.invalidate_recordset(['is_timer_running', 'timer_start', 'current_timesheet_id'])
        if self.is_timer_running:
            raise UserError(_('Timer is already running.'))
        employee = self.env['hr.employee'].search([
            ('user_id', '=', self.env.uid), ('company_id', '=', self.company_id.id)
        ], limit=1)
        if not employee:
            raise UserError(_('No Employee linked to your user in the Task company.'))
        ts = self.env['el_construction.timesheet'].with_context(
            _construction_task_timer_token=_TASK_TIMER_TOKEN
        ).create({
            'task_id': self.id,
            'employee_id': employee.id,
            'date': fields.Date.context_today(self),
            'hours': 0.0,
            'description': _('Timer running: %s') % self.name,
            'state': 'running',
        })
        self.with_context(_construction_task_timer_token=_TASK_TIMER_TOKEN).write({
            'is_timer_running': True,
            'timer_start': fields.Datetime.now(),
            'current_timesheet_id': ts.id,
        })
        return True

    def action_timer_stop(self):
        self.ensure_one()
        if not self.is_timer_running:
            raise UserError(_('No timer is running.'))
        if self.state not in ('in_progress', 'cancelled'):
            raise UserError(_('A timer can only be stopped for an In Progress or Cancelled Task.'))
        if not self.timer_start:
            raise UserError(_('Timer start time is missing.'))
        elapsed = max(round((fields.Datetime.now() - self.timer_start).total_seconds() / 3600.0, 2), 0.01)
        if self.current_timesheet_id:
            self.current_timesheet_id.with_context(_construction_timesheet_timer=True).write({
                'hours': elapsed, 'state': 'done',
            })
        self.with_context(_construction_task_timer_token=_TASK_TIMER_TOKEN).write({
            'is_timer_running': False, 'timer_start': False, 'current_timesheet_id': False,
        })
        return True


class ConstructionTimesheet(models.Model):
    _name = 'el_construction.timesheet'
    _description = 'Construction Timesheet'
    _order = 'date desc, id desc'

    task_id = fields.Many2one('el_construction.task', string='Task', required=True, ondelete='cascade', index=True)
    project_id = fields.Many2one('el_construction.project', string='Project', related='task_id.project_id', store=True, index=True)
    company_id = fields.Many2one('res.company', string='Company', related='task_id.company_id', store=True, index=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, ondelete='restrict')
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    hours = fields.Float(string='Hours', required=True, default=0.0)
    description = fields.Char(string='Description')
    is_internal = fields.Boolean(string='Internal Timesheet', default=False)
    state = fields.Selection([
        ('running', 'Running'), ('done', 'Done'), ('cancelled', 'Cancelled')
    ], required=True, default='done', copy=False)

    @api.constrains('task_id', 'employee_id', 'company_id')
    def _check_consistency(self):
        for rec in self:
            if rec.task_id.company_id != rec.company_id:
                raise ValidationError(_('Timesheet company must match the Task company.'))
            if rec.employee_id.company_id and rec.employee_id.company_id != rec.company_id:
                raise ValidationError(_('Employee must belong to the Task company.'))

    @api.constrains('hours')
    def _check_hours(self):
        for rec in self:
            if rec.hours < 0:
                raise ValidationError(_('Timesheet hours cannot be negative.'))
            if rec.state == 'done' and rec.hours <= 0:
                raise ValidationError(_('Completed Timesheet hours must be greater than zero.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('state') == 'running' and self.env.context.get('_construction_task_timer_token') != _TASK_TIMER_TOKEN:
                raise UserError(_('Running Timesheets can only be created by the Task timer.'))
            task_id = vals.get('task_id')
            if task_id:
                task = self.env['el_construction.task'].browse(task_id)
                if task.state in ('done', 'cancelled'):
                    raise UserError(_('Timesheets cannot be created for completed or cancelled Tasks.'))
        records = super().create(vals_list)
        records._check_consistency()
        return records

    def write(self, vals):
        timer_write = self.env.context.get('_construction_timesheet_timer')
        if 'state' in vals and vals['state'] == 'running' and self.env.context.get('_construction_task_timer_token') != _TASK_TIMER_TOKEN:
            raise UserError(_('A Timesheet can only enter the Running state through the Task timer.'))
        for rec in self:
            if rec.state == 'done' and not timer_write:
                if any(field in vals for field in ('task_id', 'employee_id', 'date', 'hours', 'description', 'is_internal', 'state')):
                    raise UserError(_('Completed Timesheets are read-only.'))
            if rec.task_id.state in ('done', 'cancelled') and not timer_write:
                raise UserError(_('Timesheets cannot be changed for completed or cancelled Tasks.'))
        res = super().write(vals)
        self._check_consistency()
        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'running':
                raise UserError(_('Running Timesheets must be stopped before deletion.'))
            if rec.state == 'done' or rec.task_id.state not in ('draft', 'in_progress'):
                raise UserError(_('Completed Timesheets or Timesheets on closed Tasks cannot be deleted.'))
        return super().unlink()
