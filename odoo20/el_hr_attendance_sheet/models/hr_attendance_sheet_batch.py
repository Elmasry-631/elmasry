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
    date_to = fields.Date(string='Date To', required=True, tracking=True)
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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'hr.attendance.sheet.batch'
                ) or _('New')
        return super().create(vals_list)

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
    def action_generate_sheets(self):
        """Generate one attendance sheet per employee in the department."""
        Sheet = self.env['hr.attendance.sheet']
        SheetBatchLine = self.env['hr.attendance.sheet.batch.line']
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_(
                    "Batch %s: can only generate sheets from Draft state."
                ) % rec.name)
            # Get all active employees in the department
            employees = self.env['hr.employee'].search([
                ('department_id', '=', rec.department_id.id),
                ('active', '=', True),
                ('company_id', '=', rec.company_id.id),
            ])
            if not employees:
                raise UserError(_(
                    "No active employees found in department %s."
                ) % rec.department_id.name)
            # Clear existing batch lines
            rec.line_ids.unlink()
            for emp in employees:
                sheet = Sheet.create({
                    'employee_id': emp.id,
                    'date_from': rec.date_from,
                    'date_to': rec.date_to,
                    'company_id': rec.company_id.id,
                    'batch_id': rec.id,
                })
                SheetBatchLine.create({
                    'batch_id': rec.id,
                    'employee_id': emp.id,
                    'sheet_id': sheet.id,
                })
                # Auto-compute each sheet
                try:
                    sheet.action_compute()
                except UserError:
                    # Skip employees with errors (no contract / no policy)
                    continue
            rec.write({'state': 'confirmed'})
            rec.message_post(
                body=_("Batch confirmed: %d sheets generated.")
                % len(rec.line_ids)
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
        self.write({'state': 'done'})

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
        self.write({'state': 'cancelled'})

    def action_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_(
                    "Batch %s: only cancelled batches can be reset to draft."
                ) % rec.name)
        self.write({'state': 'draft'})


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
    company_id = fields.Many2one(
        'res.company',
        related='batch_id.company_id',
        store=True,
    )
