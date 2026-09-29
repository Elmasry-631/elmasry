# -*- coding: utf-8 -*-
from odoo import api, fields, models


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

    @api.depends('attendance_sheet_id', 'attendance_sheet_id.total_overtime')
    def _compute_attendance_data(self):
        for rec in self:
            sheet = rec.attendance_sheet_id
            if sheet:
                rec.overtime_hours = sheet.total_overtime
                rec.late_in_hours = sheet.total_late_in / 60.0
                rec.absence_days = sheet.total_absence
                rec.difference_hours = sheet.total_difference
            else:
                rec.overtime_hours = 0.0
                rec.late_in_hours = 0.0
                rec.absence_days = 0.0
                rec.difference_hours = 0.0
