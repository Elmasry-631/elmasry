# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrAttendanceSheetBatch(models.Model):
    _name = 'hr.attendance.sheet.batch'
    _description = 'HR Attendance Sheet Batch'
    _inherit = ['mail.thread']
    _order = 'date_from desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
        tracking=True,
    )
    date_from = fields.Date(string='Date From', required=True, tracking=True)
    date_to = fields.Date(
        string='Date To',
        compute='_compute_date_to',
        store=True,
        readonly=False,
        tracking=True,
        help="Last day of the month of 'Date From'. Filled automatically.",
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False, index=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )
    line_ids = fields.One2many(
        'hr.attendance.sheet.batch.line',
        'batch_id',
        string='Batch Lines',
    )

    @api.depends('date_from')
    def _compute_date_to(self):
        for rec in self:
            rec.date_to = fields.Date.end_of(rec.date_from, 'month') if rec.date_from else False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hr.attendance.sheet.batch'
                ) or _('New')
        return super().create(vals_list)

    def write(self, vals):
        if 'state' in vals:
            if not self.env.context.get('_attendance_batch_state_transition'):
                raise UserError(_(
                    "Use the batch workflow actions to change status."
                ))
            allowed = {
                'draft': {'confirmed', 'cancelled'},
                'confirmed': {'done', 'cancelled'},
                'done': set(),
                'cancelled': {'draft'},
            }
            target = vals['state']
            for rec in self:
                if target != rec.state and target not in allowed.get(rec.state, set()):
                    raise UserError(_(
                        "Batch %s: transition from %s to %s is not allowed."
                    ) % (rec.name, rec.state, target))
        return super().write(vals)

    @api.constrains('date_from', 'date_to')
    def _check_period(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise UserError(_(
                    "End date (%s) cannot be before start date (%s)."
                ) % (rec.date_to, rec.date_from))

    # ------------------------------------------------------------
    # STATE MACHINE
    # ------------------------------------------------------------
    def action_generate_sheets(self, employee_ids=None):
        """Generate sheets for selected employees or the whole department."""
        Sheet = self.env['hr.attendance.sheet']
        SheetBatchLine = self.env['hr.attendance.sheet.batch.line']
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_(
                    "Batch %s: can only generate sheets from Draft state."
                ) % rec.name)
            # Generate only requested employees when a selection is supplied.
            domain = [
                ('department_id', '=', rec.department_id.id),
                ('active', '=', True),
                ('company_id', '=', rec.company_id.id),
            ]
            if employee_ids is not None:
                domain.append(('id', 'in', employee_ids))
            employees = self.env['hr.employee'].search(domain)
            if not employees:
                raise UserError(_(
                    "No active employees found in department %s."
                ) % rec.department_id.name)
            # Clear existing batch lines
            rec.line_ids.unlink()
            for emp in employees:
                try:
                    with self.env.cr.savepoint():
                        sheet = Sheet.create({
                            'employee_id': emp.id,
                            'date_from': rec.date_from,
                            'date_to': rec.date_to,
                            'company_id': rec.company_id.id,
                            'batch_id': rec.id,
                        })
                except UserError as error:
                    SheetBatchLine.create({
                        'batch_id': rec.id,
                        'employee_id': emp.id,
                        'error_message': str(error),
                    })
                    continue
                line = SheetBatchLine.create({
                    'batch_id': rec.id,
                    'employee_id': emp.id,
                    'sheet_id': sheet.id,
                })
                # Preserve failed rows and their reason for transparent follow-up.
                try:
                    with self.env.cr.savepoint():
                        sheet.action_compute()
                except UserError as error:
                    line.error_message = str(error)
            rec.with_context(_attendance_batch_state_transition=True).write({'state': 'confirmed'})
            failed = rec.line_ids.filtered('error_message')
            rec.message_post(
                body=_("Batch confirmed: %d sheets generated; %d require attention.")
                % (len(rec.line_ids), len(failed))
            )

    def action_confirm(self):
        """Alias for action_generate_sheets."""
        self.action_generate_sheets()

    def action_done(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError(_(
                    "Batch %s: only confirmed batches can be set to Done."
                ) % rec.name)
            for line in rec.line_ids:
                if line.sheet_id.state not in ('approved', 'done'):
                    raise UserError(_(
                        "Cannot mark batch Done: sheet %s for employee %s "
                        "is not yet approved."
                    ) % (line.sheet_id.name, line.employee_id.name))
        self.with_context(_attendance_batch_state_transition=True).write({'state': 'done'})

    def action_cancel(self):
        for rec in self:
            if rec.state not in ('draft', 'confirmed'):
                raise UserError(_(
                    "Batch %s: cannot cancel in %s state."
                ) % (rec.name, rec.state))
        # Cascade cancel to child sheets (only those still cancellable)
        for rec in self:
            for line in rec.line_ids:
                if line.sheet_id.state in ('draft', 'computed', 'approved'):
                    line.sheet_id.action_cancel()
        self.with_context(_attendance_batch_state_transition=True).write({'state': 'cancelled'})

    def action_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_(
                    "Batch %s: only cancelled batches can be reset to draft."
                ) % rec.name)
        self.with_context(_attendance_batch_state_transition=True).write({'state': 'draft'})


class HrAttendanceSheetBatchLine(models.Model):
    _name = 'hr.attendance.sheet.batch.line'
    _description = 'HR Attendance Sheet Batch Line'
    _order = 'batch_id, employee_id'

    batch_id = fields.Many2one(
        'hr.attendance.sheet.batch',
        string='Batch',
        required=True,
        ondelete='cascade',
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
    )
    sheet_id = fields.Many2one(
        'hr.attendance.sheet',
        string='Attendance Sheet',
        readonly=True,
    )
    error_message = fields.Text(string='Generation Error', readonly=True)
    company_id = fields.Many2one(
        'res.company',
        related='batch_id.company_id',
        store=True,
    )
