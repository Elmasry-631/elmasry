# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrAttendanceSheetBatchWizard(models.TransientModel):
    _name = 'hr.attendance.sheet.batch.wizard'
    _description = 'Create Attendance Sheet Batch Wizard'

    department_id = fields.Many2one(
        'hr.department',
        string='Department',
        required=True,
    )
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    employee_ids = fields.Many2many(
        'hr.employee',
        string='Employees (optional override)',
        help="If left empty, all active employees in the department will "
             "be used. Otherwise, only the selected employees will have "
             "sheets generated.",
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise UserError(_(
                    "End date cannot be before start date."
                ))

    def action_create_batch(self):
        self.ensure_one()
        batch = self.env['hr.attendance.sheet.batch'].create({
            'department_id': self.department_id.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'company_id': self.company_id.id,
        })
        # Generate sheets immediately
        batch.action_generate_sheets()
        # If employee_ids were specified, filter batch lines
        if self.employee_ids:
            batch.line_ids.filtered(
                lambda l: l.employee_id not in self.employee_ids
            ).sheet_id.unlink()
            batch.line_ids.filtered(
                lambda l: l.employee_id not in self.employee_ids
            ).unlink()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Attendance Sheet Batch'),
            'res_model': 'hr.attendance.sheet.batch',
            'res_id': batch.id,
            'view_mode': 'form',
            'target': 'current',
        }
