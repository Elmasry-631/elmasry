# -*- coding: utf-8 -*-
import datetime
import math
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class VehicleInstallment(models.Model):
    _name = 'vehicle.installment'
    _inherit = ['mail.thread']
    _description = 'Vehicle Installment'
    _rec_name = 'vehicle_id'

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True, tracking=True, ondelete='restrict')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, tracking=True, ondelete='restrict')
    date = fields.Date(string='Date', required=True, tracking=True, default=datetime.date.today())
    vehicle_price = fields.Monetary(string='Vehicle Price', currency_field='currency_id', required=True, tracking=True)
    rate_percentage = fields.Float(string='Rate Percentage (%)', required=True, tracking=True, default=0.0)
    monthly_payment = fields.Monetary(string='Monthly Payment', currency_field='currency_id', required=True, tracking=True)
    
    # Computed fields
    total_amount = fields.Monetary(string='Total Amount', currency_field='currency_id', compute='_compute_total_amount', store=True, tracking=True)
    calculated_months = fields.Float(string='Calculated Months', compute='_compute_calculated_months', store=True)
    full_months = fields.Integer(string='Full Payment Months', compute='_compute_calculated_months', store=True)
    last_payment_amount = fields.Monetary(string='Last Payment Amount', currency_field='currency_id', compute='_compute_calculated_months', store=True)
    
    installment_lines = fields.One2many('vehicle.installment.line', 'installment_id', string='Installment Lines')
    reason = fields.Text(string='Reason', tracking=True)
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='employee_id.company_id',
        index=True,
        required=False,
        store=True
    )

    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ], default='draft', tracking=True)

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=False,
        related='company_id.currency_id',
        store=True
    )

    @api.depends('vehicle_price', 'rate_percentage')
    def _compute_total_amount(self):
        """
        حساب المبلغ الإجمالي = سعر السيارة + (سعر السيارة × نسبة الفائدة)
        """
        for rec in self:
            if rec.vehicle_price and rec.rate_percentage:
                rate_amount = rec.vehicle_price * (rec.rate_percentage / 100)
                rec.total_amount = rec.vehicle_price + rate_amount
            else:
                rec.total_amount = rec.vehicle_price

    @api.depends('total_amount', 'monthly_payment')
    def _compute_calculated_months(self):
        """
        حساب عدد الأشهر والقسط الأخير
        مثال: لو المبلغ الكلي 24000 والقسط الشهري 1800
        عدد الأشهر = 24000 / 1800 = 13.333333
        الأشهر الكاملة = 13 شهر
        القسط الأخير = 0.333333 × 1800 = 599.9994
        """
        for rec in self:
            if rec.total_amount and rec.monthly_payment and rec.monthly_payment > 0:
                # حساب عدد الأشهر الإجمالي
                total_months = rec.total_amount / rec.monthly_payment
                rec.calculated_months = total_months
                
                # فصل الجزء الصحيح عن الكسور
                full_months = math.floor(total_months)
                rec.full_months = full_months
                
                # حساب الكسور
                fractional_part = total_months - full_months
                
                # حساب القسط الأخير
                if fractional_part > 0:
                    rec.last_payment_amount = fractional_part * rec.monthly_payment
                else:
                    rec.last_payment_amount = rec.monthly_payment
            else:
                rec.calculated_months = 0.0
                rec.full_months = 0
                rec.last_payment_amount = 0.0

    def compute_installments(self):
        """
        حساب الأقساط الشهرية
        """
        for rec in self:
            if rec.monthly_payment > 0 and rec.total_amount > 0:
                # حذف الأقساط السابقة إن وجدت
                if len(rec.installment_lines) > 0:
                    rec.write({
                        'installment_lines': [(5, 0, 0)]
                    })
                
                today = fields.Date.today()
                period_start = rec.date
                
                # تحديد تاريخ بداية الدفع (يوم 25 من كل شهر)
                if rec.date.day <= 25:
                    period_start = rec.date.replace(day=25)
                elif rec.date.month != 12 and rec.date.day >= 26:
                    period_start = rec.date.replace(month=rec.date.month + 1, day=25)
                elif rec.date.month == 12:
                    period_start = rec.date.replace(year=today.year + 1, month=1, day=25)

                # إنشاء الأقساط الكاملة
                for installment in range(rec.full_months):
                    self.installment_lines.create({
                        'installment_id': rec.id,
                        'payment_date': period_start,
                        'amount': rec.monthly_payment,
                    })
                    # الانتقال للشهر التالي
                    if period_start.month == 12:
                        period_start = period_start.replace(year=period_start.year + 1, month=1, day=25)
                    else:
                        period_start = period_start.replace(month=period_start.month + 1, day=25)
                
                # إضافة القسط الأخير إذا كان هناك كسور
                if rec.last_payment_amount > 0 and rec.last_payment_amount != rec.monthly_payment:
                    self.installment_lines.create({
                        'installment_id': rec.id,
                        'payment_date': period_start,
                        'amount': rec.last_payment_amount,
                    })
                    
            rec.state = 'waiting'

    def button_approve(self):
        self.state = 'approved'

    def button_reject(self):
        self.state = 'rejected'

    def button_draft(self):
        self.state = 'draft'

    def get_admins(self):
        return self.env.ref('vehicle_installment.group_vehicle_installment_manager').user_ids.ids

    def write(self, vals_list):
        res = super(VehicleInstallment, self).write(vals_list)
        for rec in self:
            current_user_id = rec.env.user.id
            admins = rec.get_admins()
            if rec.state == 'approved' and current_user_id not in admins:
                raise ValidationError(
                    _("You cannot edit current record as its status is 'approved', contact your administrator instead."))
        return res

    def unlink(self):
        for rec in self:
            if rec.state == 'approved':
                raise ValidationError(_("You can only delete records in (Draft, Rejected) status."))
        return super(VehicleInstallment, self).unlink()
