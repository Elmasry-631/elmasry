from odoo import models, fields, api, _


class LoanLine(models.Model):
    _name = 'loan.line'
    _description = 'Loan Line'

    loan_id = fields.Many2one('loan')
    employee_id = fields.Many2one('hr.employee', 'Employee', related='loan_id.employee_id', store=True)
    payment_date = fields.Date('Payment Date')
    amount = fields.Monetary('Amount', currency_field='currency_id')
    state = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ], default='unpaid')
    loan_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ], related='loan_id.state', store=True, string="Loan State")
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='loan_id.company_id',
        index=True,
        store=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=False,
        related='loan_id.currency_id',
        store=True
    )
    note = fields.Html('Note')

    def write(self, vals_list):
        res = super(LoanLine, self).write(vals_list)
        if 'amount' in vals_list:
            for line in self:
                all_lines = line.loan_id.loan_lines

                later_installments = all_lines.filtered(
                    lambda l: l.payment_date and l.payment_date > line.payment_date and l.state == 'unpaid'
                )

                if later_installments:
                    earlier_installments = all_lines.filtered(
                        lambda l: l.payment_date and l.payment_date < line.payment_date
                    )

                    earlier_installments_amount = sum(earlier_installments.mapped('amount'))

                    loan_amount = line.loan_id.amount
                    total_amount_due = loan_amount - earlier_installments_amount - line.amount
                    amount_due_per_month = total_amount_due / len(later_installments)

                    later_installments.write({'amount': amount_due_per_month})

        return res