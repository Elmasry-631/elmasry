# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrAttendanceCreatePayslipWizard(models.TransientModel):
    _name = 'hr.attendance.create.payslip.wizard'
    _description = 'Create Payslip From Attendance Sheet Wizard'

    sheet_id = fields.Many2one(
        'hr.attendance.sheet',
        string='Attendance Sheet',
        required=True,
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
    )
    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    struct_id = fields.Many2one(
        'hr.payroll.structure',
        string='Salary Structure',
        required=True,
        default=lambda self: self.env.ref(
            'el_hr_attendance_sheet.structure_attendance',
            raise_if_not_found=False,
        ),
    )
    contract_id = fields.Many2one(
        'hr.version',
        string='Contract',
        related='sheet_id.contract_id',
        readonly=True,
    )

    def action_create_payslip(self):
        self.ensure_one()
        sheet = self.sheet_id
        if sheet.state != 'approved':
            raise UserError(_(
                "Sheet %s must be Approved before creating a payslip."
            ) % sheet.name)
        if sheet.payslip_id:
            raise UserError(_(
                "Sheet %s already has a payslip (%s)."
            ) % (sheet.name, sheet.payslip_id.name))
        vals = {
            'employee_id': self.employee_id.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'struct_id': self.struct_id.id,
            'version_id': sheet.contract_id.id,
            'attendance_sheet_id': sheet.id,
        }
        # 'name' is required on hr.payslip but is not precomputed, so the ORM
        # fills it after the INSERT -- which the NOT NULL constraint on the
        # column rejects. Build it up-front with the model's own logic so the
        # name matches what the standard payroll flow produces.
        draft = self.env['hr.payslip'].new(vals)
        draft._compute_name()
        payslip = self.env['hr.payslip'].create(dict(vals, name=draft.name))
        # Compute payslip inputs from sheet
        sheet.write({'payslip_id': payslip.id, 'state': 'done'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Payslip'),
            'res_model': 'hr.payslip',
            'res_id': payslip.id,
            'view_mode': 'form',
            'target': 'current',
        }
