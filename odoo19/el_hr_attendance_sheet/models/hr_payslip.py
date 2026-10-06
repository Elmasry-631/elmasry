# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    attendance_sheet_id = fields.Many2one(
        'hr.attendance.sheet',
        string='Attendance Sheet',
        readonly=True,
        copy=False,
        help="Linked attendance sheet that provided overtime, lateness, "
             "absence and difference time inputs.",
    )
    no_attendance_sheet = fields.Boolean(
        string='No Attendance Sheet',
        compute='_compute_no_attendance_sheet',
        help="Technical field: this payslip is not linked to any attendance "
             "sheet, so all attendance amounts are zero.",
    )
    overtime_hours = fields.Float(
        string='Overtime Hours',
        compute='_compute_attendance_data',
        store=True,
        help="Total overtime hours from the linked attendance sheet.",
    )
    late_in_hours = fields.Float(
        string='Late In Hours',
        compute='_compute_attendance_data',
        store=True,
        help="Total late-in hours (computed from late-in minutes).",
    )
    absence_days = fields.Float(
        string='Absence Days',
        compute='_compute_attendance_data',
        store=True,
        help="Total absence days from the linked attendance sheet.",
    )
    difference_hours = fields.Float(
        string='Difference Hours',
        compute='_compute_attendance_data',
        store=True,
        help="Total difference hours (worked - planned - overtime).",
    )
    late_penalty_hours = fields.Float(
        string='Late Penalty Hours',
        compute='_compute_attendance_data',
        store=True,
        help="Total late penalty hours after applying the lateness "
             "escalation steps (repetitions).",
    )
    absence_penalty_days = fields.Float(
        string='Absence Penalty Days',
        compute='_compute_attendance_data',
        store=True,
        help="Total absence deduction days after applying the absence "
             "escalation steps (repetitions).",
    )

    number_late_occurrences = fields.Integer(
        string='Late Occurrences',
        compute='_compute_attendance_data',
        store=True,
        help="Number of days with lateness in the sheet period.",
    )
    number_absence_occurrences = fields.Integer(
        string='Absence Occurrences',
        compute='_compute_attendance_data',
        store=True,
        help="Number of absence days in the sheet period.",
    )

    @api.depends('attendance_sheet_id', 'attendance_sheet_id.total_overtime')
    def _compute_attendance_data(self):
        for rec in self:
            sheet = rec.attendance_sheet_id
            if sheet:
                rec.overtime_hours = sheet.total_overtime
                rec.late_in_hours = sheet.total_late_in / 60.0
                rec.absence_days = sheet.total_absence
                rec.difference_hours = sheet.total_difference
                rec.late_penalty_hours = sheet.total_late_penalty_hours
                rec.absence_penalty_days = sheet.total_absence_penalty_days
                rec.number_late_occurrences = len(
                    sheet.line_ids.filtered(
                        lambda l: l.late_in_minutes > 0))
                rec.number_absence_occurrences = len(
                    sheet.line_ids.filtered(lambda l: l.is_absent))
            else:
                rec.overtime_hours = 0.0
                rec.late_in_hours = 0.0
                rec.absence_days = 0.0
                rec.difference_hours = 0.0
                rec.late_penalty_hours = 0.0
                rec.absence_penalty_days = 0.0
                rec.number_late_occurrences = 0
                rec.number_absence_occurrences = 0

    @api.depends('attendance_sheet_id')
    def _compute_no_attendance_sheet(self):
        for rec in self:
            rec.no_attendance_sheet = not rec.attendance_sheet_id

    # ------------------------------------------------------------------
    # LINKING
    # ------------------------------------------------------------------
    def _find_matching_attendance_sheet(self):
        """Return the computed sheet covering this payslip period.

        A payslip created straight from the payroll menu has no sheet link, so
        its overtime / lateness / absence amounts all compute to zero. Matching
        on employee and period lets such a payslip pick up the data.
        """
        self.ensure_one()
        return self.env['hr.attendance.sheet'].search([
            ('employee_id', '=', self.employee_id.id),
            ('state', 'not in', ('draft', 'cancelled')),
            ('date_from', '<=', self.date_to),
            ('date_to', '>=', self.date_from),
            ('payslip_id', '=', False),
        ], limit=1, order='date_from desc')

    def action_link_attendance_sheet(self):
        """Link this payslip to the attendance sheet of the same period."""
        self.ensure_one()
        if self.attendance_sheet_id:
            raise UserError(_(
                "Payslip %s is already linked to attendance sheet %s."
            ) % (self.name, self.attendance_sheet_id.name))
        sheet = self._find_matching_attendance_sheet()
        if not sheet:
            raise UserError(_(
                "No computed attendance sheet found for %s covering %s to %s.\n"
                "Compute the attendance sheet first, then link it here."
            ) % (self.employee_id.name, self.date_from, self.date_to))
        self.write({'attendance_sheet_id': sheet.id})
        sheet.write({'payslip_id': self.id})
        self.compute_sheet()
        return True

    def action_open_attendance_sheet(self):
        """Open the linked attendance sheet."""
        self.ensure_one()
        if not self.attendance_sheet_id:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('Attendance Sheet'),
            'res_model': 'hr.attendance.sheet',
            'res_id': self.attendance_sheet_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Auto-link the matching attendance sheet when none was given."""
        payslips = super().create(vals_list)
        for payslip in payslips:
            if payslip.attendance_sheet_id:
                continue
            sheet = payslip._find_matching_attendance_sheet()
            if sheet and not sheet.payslip_id:
                sheet.write({'payslip_id': payslip.id})
                payslip.write({'attendance_sheet_id': sheet.id})
        return payslips
