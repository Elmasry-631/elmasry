# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrAttendancePolicy(models.Model):
    _name = 'hr.attendance.policy'
    _description = 'HR Attendance Policy'
    _inherit = ['mail.thread']
    _order = 'name'

    name = fields.Char(string='Name', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        tracking=True,
    )

    overtime_working_id = fields.Many2one(
        'hr.attendance.rule.overtime',
        string='Overtime Rule (Working Days)',
        domain="[('type', '=', 'working_day'), ('company_id', '=', company_id)]",
        tracking=True,
    )
    overtime_weekend_id = fields.Many2one(
        'hr.attendance.rule.overtime',
        string='Overtime Rule (Weekends)',
        domain="[('type', '=', 'weekend'), ('company_id', '=', company_id)]",
        tracking=True,
    )
    overtime_holiday_id = fields.Many2one(
        'hr.attendance.rule.overtime',
        string='Overtime Rule (Public Holidays)',
        domain="[('type', '=', 'public_holiday'), ('company_id', '=', company_id)]",
        tracking=True,
    )
    lateness_id = fields.Many2one(
        'hr.attendance.rule.lateness',
        string='Lateness Rule',
        domain="[('company_id', '=', company_id)]",
        tracking=True,
    )
    absence_id = fields.Many2one(
        'hr.attendance.rule.absence',
        string='Absence Rule',
        domain="[('company_id', '=', company_id)]",
        tracking=True,
    )

    contract_ids = fields.One2many(
        'hr.version',
        'attendance_policy_id',
        string='Contracts Using This Policy',
    )

    def get_overtime_rule(self, day_type):
        """Return the overtime rule for the given day type."""
        self.ensure_one()
        if day_type == 'public_holiday':
            return self.overtime_holiday_id
        if day_type == 'weekend':
            return self.overtime_weekend_id
        return self.overtime_working_id
