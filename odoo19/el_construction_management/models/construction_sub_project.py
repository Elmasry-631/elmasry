from .workflow_mixin import ConstructionWorkflowMixin
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class ConstructionSubProject(ConstructionWorkflowMixin, models.Model):
    _name = 'el_construction.sub.project'
    _description = 'Construction Sub Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Sub Project Name', required=True, tracking=True)
    reference = fields.Char(string='Reference', readonly=True, default='New', copy=False)
    project_id = fields.Many2one('el_construction.project', string='Project', required=True, tracking=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse',
                                   related='project_id.warehouse_id', store=True, readonly=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    # Duration
    date_start = fields.Date(string='Start Date', tracking=True)
    date_end = fields.Date(string='End Date', tracking=True)

    # Status
    state = fields.Selection([
        ('planning', 'Planning'),
        ('procurement', 'Procurement'),
        ('construction', 'Construction'),
        ('handover', 'Handover'),
    ], string='Status', default='planning', tracking=True)

    # Customer
    partner_id = fields.Many2one('res.partner', string='Customer')

    # BOQ
    boq_ids = fields.One2many('el_construction.boq', 'sub_project_id', string='Bill of Quantities')

    # Engineers
    engineer_ids = fields.Many2many('hr.employee', string='Engineers')

    # Documents
    document_ids = fields.One2many('el_construction.sub.project.document', 'sub_project_id', string='Documents')
    handover_checklist_complete = fields.Boolean(string='Handover Checklist Complete', tracking=True)
    client_acceptance = fields.Boolean(string='Client Acceptance Received', tracking=True)
    handover_notes = fields.Text(string='Handover Notes')
    handover_date = fields.Date(string='Handover Date', readonly=True)
    handover_by = fields.Many2one('res.users', string='Handover By', readonly=True)

    # Insurance
    insurance_company = fields.Char(string='Insurance Company')
    insurance_policy_no = fields.Char(string='Policy Number')
    insurance_start_date = fields.Date(string='Insurance Start Date')
    insurance_end_date = fields.Date(string='Insurance End Date')
    insurance_amount = fields.Float(string='Insurance Amount')
    insurance_document = fields.Binary(string='Insurance Document', attachment=True)
    insurance_document_name = fields.Char(string='Insurance File Name')

    # Extra Expenses
    extra_expense_ids = fields.One2many('el_construction.extra.expense', 'sub_project_id', string='Extra Expenses')

    # Tasks
    task_ids = fields.One2many('el_construction.task', 'sub_project_id', string='Tasks')

    # Phases
    phase_ids = fields.One2many('el_construction.phase', 'sub_project_id', string='Project Phases (WBS)')

    # Work Orders
    work_order_ids = fields.One2many('el_construction.work.order', 'sub_project_id', string='Work Orders')

    # Material Requisitions
    material_requisition_ids = fields.One2many('el_construction.material.requisition', 'sub_project_id',
                                                string='Material Requisitions')

    # Budget Lines
    budget_line_ids = fields.One2many('el_construction.budget.line', 'sub_project_id', string='Budget Lines')

    # Progress Billing
    progress_billing_ids = fields.One2many('el_construction.progress.billing', 'sub_project_id',
                                            string='Progress Billings')

    # Computed counts
    task_count = fields.Integer(compute='_compute_counts', string='Tasks')
    phase_count = fields.Integer(compute='_compute_counts', string='Phases')
    work_order_count = fields.Integer(compute='_compute_counts', string='Work Orders')
    mreq_count = fields.Integer(compute='_compute_counts', string='Material Requisitions')
    boq_count = fields.Integer(compute='_compute_counts', string='BOQ')
    billing_count = fields.Integer(compute='_compute_counts', string='Progress Billings')
    expense_count = fields.Integer(compute='_compute_counts', string='Extra Expenses')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', 'New') == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('el_construction.sub.project') or 'New'
        return super().create(vals_list)

    @api.depends('task_ids', 'phase_ids', 'work_order_ids', 'material_requisition_ids', 'boq_ids', 'progress_billing_ids', 'extra_expense_ids')
    def _compute_counts(self):
        for rec in self:
            rec.task_count = len(rec.task_ids)
            rec.phase_count = len(rec.phase_ids)
            rec.work_order_count = len(rec.work_order_ids)
            rec.mreq_count = len(rec.material_requisition_ids)
            rec.boq_count = len(rec.boq_ids)
            rec.billing_count = len(rec.progress_billing_ids)
            rec.expense_count = len(rec.extra_expense_ids)

    def write(self, vals):
        if 'state' in vals and not self._workflow_write_allowed():
            for record in self:
                if vals['state'] != record.state:
                    raise UserError(_('Use the workflow buttons to change the Status.'))
        return super().write(vals)

    def action_planning(self):
        return self._transition('planning', {'planning': {'planning'}}, manager=True)

    def action_procurement(self):
        return self._transition('procurement', {'planning': {'procurement'}}, manager=True)

    def action_construction(self):
        return self._transition('construction', {'procurement': {'construction'}}, manager=True)

    def action_handover(self):
        for rec in self:
            rec._lock_records()
            rec.invalidate_recordset()
            open_orders = rec.work_order_ids.filtered(lambda wo: wo.state not in ('done', 'cancelled'))
            if open_orders:
                raise UserError(_('Handover requires all Work Orders to be Done or Cancelled.'))
            open_checks = self.env['el_construction.quality.check'].search_count([
                ('sub_project_id', '=', rec.id),
                ('state', 'not in', ('closed', 'cancelled')),
            ])
            if open_checks:
                raise UserError(_('Handover requires all Quality Checks to be Closed or Cancelled.'))
            open_ncrs = self.env['el_construction.ncr'].search_count([
                ('sub_project_id', '=', rec.id),
                ('state', 'not in', ('closed', 'cancelled')),
            ])
            if open_ncrs:
                raise UserError(_('Handover requires all NCRs to be Closed or Cancelled.'))
            if not rec.document_ids:
                raise UserError(_('Handover requires at least one supporting document.'))
            if not rec.handover_checklist_complete:
                raise UserError(_('Complete the Handover Checklist before handover.'))
            if not rec.client_acceptance:
                raise UserError(_('Client Acceptance is required before handover.'))
        result = self._transition('handover', {'construction': {'handover'}}, manager=True)
        self.write({'handover_date': fields.Date.context_today(self), 'handover_by': self.env.user.id})
        return result

    def action_view_tasks(self):
        return {
            'name': _('Tasks'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.task',
            'view_mode': 'list,form',
            'domain': [('sub_project_id', '=', self.id)],
            'context': {'default_sub_project_id': self.id, 'default_project_id': self.project_id.id},
        }

    def action_view_phases(self):
        return {
            'name': _('Phases (WBS)'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.phase',
            'view_mode': 'list,form',
            'domain': [('sub_project_id', '=', self.id)],
            'context': {'default_sub_project_id': self.id, 'default_project_id': self.project_id.id},
        }

    def action_view_work_orders(self):
        return {
            'name': _('Work Orders'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.work.order',
            'view_mode': 'list,form',
            'domain': [('sub_project_id', '=', self.id)],
            'context': {'default_sub_project_id': self.id, 'default_project_id': self.project_id.id},
        }

    def action_view_mreq(self):
        return {
            'name': _('Material Requisitions'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.material.requisition',
            'view_mode': 'list,form',
            'domain': [('sub_project_id', '=', self.id)],
            'context': {'default_sub_project_id': self.id, 'default_project_id': self.project_id.id},
        }

    def action_view_boq(self):
        return {
            'name': _('Bill of Quantities'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.boq',
            'view_mode': 'list,form',
            'domain': [('sub_project_id', '=', self.id)],
            'context': {'default_sub_project_id': self.id, 'default_project_id': self.project_id.id},
        }

    def action_view_billings(self):
        return {
            'name': _('Progress Billings'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.progress.billing',
            'view_mode': 'list,form',
            'domain': [('sub_project_id', '=', self.id)],
            'context': {'default_sub_project_id': self.id, 'default_project_id': self.project_id.id},
        }

    def action_view_expenses(self):
        return {
            'name': _('Extra Expenses'),
            'type': 'ir.actions.act_window',
            'res_model': 'el_construction.extra.expense',
            'view_mode': 'list,form',
            'domain': [('sub_project_id', '=', self.id)],
            'context': {'default_sub_project_id': self.id, 'default_project_id': self.project_id.id},
        }

    @api.constrains('project_id', 'company_id')
    def _check_project_company(self):
        for rec in self:
            if rec.project_id.company_id != rec.company_id:
                raise ValidationError(_('Sub Project company must match the Project company.'))

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for rec in self:
            if rec.date_start and rec.date_end and rec.date_start > rec.date_end:
                raise ValidationError(_('End Date must be after Start Date.'))
