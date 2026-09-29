import datetime
from calendar import month
from email.policy import default

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Loan(models.Model):
    _name = 'loan'
    _inherit = ['mail.thread']
    _description = 'Loan'
    _rec_name='employee_id'

    employee_id = fields.Many2one('hr.employee', required=True, tracking=True, domain=lambda l: l.employee_id_domain(), ondelete='restrict')
    date = fields.Date(required=True, tracking=True, default=datetime.date.today())
    amount = fields.Monetary(string='Amount', currency_field='currency_id', tracking=True)
    reason = fields.Text(string='Reason', tracking=True)
    loan_lines = fields.One2many('loan.line', 'loan_id')
    installments_count = fields.Char('Installments No.', required=True)
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

    def compute_installments(self):
        for rec in self:
            if int(rec.installments_count) > 0 and rec.amount > 0:
                if len(rec.loan_lines) > 1:
                    rec.write({
                        'loan_lines': [(5, 0, 0)]
                    })
                today = fields.Date.today()
                amount_per_month = rec.amount / int(rec.installments_count)
                period_start = rec.date
                if rec.date.day <= 25:
                    period_start = rec.date.replace(day=25)
                elif rec.date.month != 12 and rec.date.day >= 26:
                    period_start = rec.date.replace(month=rec.date.month + 1, day=25)
                elif rec.date.month == 12:
                    period_start = rec.date.replace(year=today.year + 1, month=1, day=25)

                for installment in range(int(rec.installments_count)):
                    self.loan_lines.create({
                        'loan_id': rec.id,
                        'payment_date': period_start,
                        'amount': amount_per_month,
                    })
                    if period_start.month == 12:
                        period_start = period_start.replace(year=period_start.year + 1, month=1, day=25)
                    else:
                        period_start = period_start.replace(month=period_start.month + 1, day=25)
            rec.state = 'waiting'

    def employee_id_domain(self):
        current_user_id = self.env.user.id
        admins = self.get_admins()
        if current_user_id not in admins:
            return ['|', ('parent_id.user_id', '=', current_user_id), ('user_id', '=', current_user_id)]
        else:
            return []

    def button_approve(self):
        self.state = 'approved'

    def button_reject(self):
        self.state = 'rejected'

    def button_draft(self):
        self.state = 'draft'

    def get_admins(self):
        return self.env.ref('loan_management.group_loan_manager').user_ids.ids

    def write(self, vals_list):
        res = super(Loan, self).write(vals_list)
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
        return super(Loan, self).unlink()
