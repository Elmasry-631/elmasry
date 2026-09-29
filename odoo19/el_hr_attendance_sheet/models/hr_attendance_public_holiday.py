# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrAttendancePublicHoliday(models.Model):
    _name = 'hr.attendance.public.holiday'
    _description = 'HR Attendance Public Holiday'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_from desc'

    name = fields.Char(string='Name', required=True, tracking=True)
    date_from = fields.Date(string='Date From', required=True, tracking=True)
    date_to = fields.Date(string='Date To', required=True, tracking=True)
    active = fields.Boolean(string='Active', default=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, copy=False)
    line_ids = fields.One2many(
        'hr.attendance.public.holiday.line',
        'holiday_id',
        string='Holiday Lines',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        tracking=True,
    )

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise UserError(_(
                    "End date (%s) cannot be before start date (%s)."
                ) % (rec.date_to, rec.date_from))

    def action_activate(self):
        for rec in self:
            if rec.state != 'draft':
                raise UserError(_(
                    "Only draft public holidays can be activated."
                ))
            if not rec.line_ids:
                raise UserError(_(
                    "Cannot activate a public holiday without any employee/"
                    "department/tag lines."
                ))
        self.write({'state': 'active', 'active': True})

    def action_cancel(self):
        for rec in self:
            if rec.state not in ('draft', 'active'):
                raise UserError(_(
                    "Only draft or active public holidays can be cancelled."
                ))
        self.write({'state': 'cancelled', 'active': False})

    def action_draft(self):
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError(_(
                    "Only cancelled public holidays can be reset to draft."
                ))
        self.write({'state': 'draft', 'active': True})

    def is_employee_on_holiday(self, employee, date):
        """Check if employee is on public holiday on the given date."""
        self.ensure_one()
        if not (self.date_from <= date <= self.date_to):
            return False
        for line in self.line_ids:
            if line.matches_employee(employee):
                return True
        return False


class HrAttendancePublicHolidayLine(models.Model):
    _name = 'hr.attendance.public.holiday.line'
    _description = 'HR Attendance Public Holiday Line'
    _order = 'holiday_id, id'

    holiday_id = fields.Many2one(
        'hr.attendance.public.holiday',
        string='Public Holiday',
        required=True,
        ondelete='cascade',
    )
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department',
    )
    employee_tag_ids = fields.Many2many(
        'hr.employee.category',
        string='Employee Tags',
    )
    company_id = fields.Many2one(
        'res.company',
        related='holiday_id.company_id',
        store=True,
    )

    @api.model
    def matches_employee(self, employee):
        """Return True if this line matches the given employee."""
        self.ensure_one()
        if self.employee_id and self.employee_id != employee:
            return False
        if self.department_id and self.department_id != employee.department_id:
            return False
        if self.employee_tag_ids:
            emp_tags = employee.category_ids
            if not (self.employee_tag_ids & emp_tags):
                return False
        # If all three are empty, line matches everyone
        return True
