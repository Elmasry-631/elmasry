from odoo import models, fields



class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    loan_total = fields.Float(string='Total Loan', readonly=True)
    loan_before = fields.Float(string='Loan Before', readonly=True)
    loan_after = fields.Float(string='Loan After', readonly=True)

    def action_payslip_paid(self):
        res = super(HrPayslip, self).action_payslip_paid()
        for payslip in self:
            loan_line = self.env['loan.line'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('loan_state', '=', 'approved'),
                ('state', '=', 'unpaid'),
                ('payment_date', '>=', payslip.date_from),
                ('payment_date', '<=', payslip.date_to),
            ])

            loan_id = loan_line.loan_id
            paid_loans = loan_id.loan_lines.filtered_domain([('state', '=', 'paid')])

            loan_line.state = 'paid'

            unpaid_loans = loan_line.loan_id.loan_lines.filtered_domain([('state', '=', 'unpaid')])
            payslip.loan_total = loan_line.loan_id.amount if loan_line.loan_id else 0
            total_paid_loans = sum(paid_loans.mapped('amount')) if paid_loans else 0
            total_unpaid_loans = sum(unpaid_loans.mapped('amount')) if unpaid_loans else 0

            payslip.loan_before = loan_id.amount - total_paid_loans
            payslip.loan_after = total_unpaid_loans

            if not unpaid_loans:
                loan_id.state = 'paid'
        return res

    def action_payslip_unpaid(self):
        res = super(HrPayslip, self).action_payslip_unpaid()
        for payslip in self:
            loan_line = self.env['loan.line'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('loan_state', 'in', ['approved', 'paid']),
                ('state', '=', 'paid'),
                ('payment_date', '>=', payslip.date_from),
                ('payment_date', '<=', payslip.date_to),
            ])
            loan_id = loan_line.loan_id
            loan_line.state = 'unpaid'
            paid_loans = loan_id.loan_lines.filtered_domain([('state', '=', 'paid')])
            unpaid_loans = loan_line.loan_id.loan_lines.filtered_domain([('state', '=', 'unpaid')])
            payslip.loan_total = loan_line.loan_id.amount if loan_line.loan_id else 0
            total_paid_loans = sum(paid_loans.mapped('amount')) if paid_loans else 0
            total_unpaid_loans = sum(unpaid_loans.mapped('amount')) if unpaid_loans else 0

            payslip.loan_before = loan_id.amount - total_paid_loans
            payslip.loan_after = total_unpaid_loans

            loan_id.state = 'approved'
        return res

    def action_payslip_cancel(self):
        res = super(HrPayslip, self).action_payslip_cancel()
        for payslip in self:
            loan_line = self.env['loan.line'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('loan_state', 'in', ['approved', 'paid']),
                ('state', '=', 'paid'),
                ('payment_date', '>=', payslip.date_from),
                ('payment_date', '<=', payslip.date_to),
            ])
            loan_id = loan_line.loan_id
            loan_line.state = 'unpaid'
            paid_loans = loan_id.loan_lines.filtered_domain([('state', '=', 'paid')])
            unpaid_loans = loan_line.loan_id.loan_lines.filtered_domain([('state', '=', 'unpaid')])
            payslip.loan_total = loan_line.loan_id.amount if loan_line.loan_id else 0
            total_paid_loans = sum(paid_loans.mapped('amount')) if paid_loans else 0
            total_unpaid_loans = sum(unpaid_loans.mapped('amount')) if unpaid_loans else 0

            payslip.loan_before = loan_id.amount - total_paid_loans
            payslip.loan_after = total_unpaid_loans

            loan_id.state = 'approved'
        return res


