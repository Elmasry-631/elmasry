from odoo import models



class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_paid(self):
        res = super(HrPayslip, self).action_payslip_paid()
        for payslip in self:
            installment_line = self.env['vehicle.installment.line'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('installment_state', '=', 'approved') if not payslip.is_refund_payslip else ('installment_state', 'in', ['paid', 'approved']),
                ('state', '=', 'unpaid') if not payslip.is_refund_payslip else ('state', '=', 'paid'),
                ('payment_date', '>=', payslip.date_from),
                ('payment_date', '<=', payslip.date_to),
            ])
            installment_line.state = 'paid' if not payslip.is_refund_payslip else 'unpaid'

            unpaid_installments = installment_line.installment_id.installment_lines.filtered_domain([('state', '=', 'unpaid')])
            if not unpaid_installments:
                installment_line.installment_id.state = 'paid'
            else:
                installment_line.installment_id.state = 'approved'
        return res

    def action_payslip_unpaid(self):
        res = super(HrPayslip, self).action_payslip_unpaid()
        for payslip in self:
            installment_line = self.env['vehicle.installment.line'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('installment_state', 'in', ['approved', 'paid']),
                ('state', '=', 'paid') if not payslip.is_refund_payslip else ('state', '=', 'unpaid'),
                ('payment_date', '>=', payslip.date_from),
                ('payment_date', '<=', payslip.date_to),
            ])
            installment_line.state = 'unpaid' if not payslip.is_refund_payslip else 'paid'
            installment_line.installment_id.state = 'approved' if not payslip.is_refund_payslip else 'paid'
        return res

    def action_payslip_cancel(self):
        res = super(HrPayslip, self).action_payslip_cancel()
        for payslip in self:
            installment_line = self.env['vehicle.installment.line'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('installment_state', 'in', ['approved', 'paid']),
                ('state', '=', 'paid') if not payslip.is_refund_payslip else ('state', '=', 'unpaid'),
                ('payment_date', '>=', payslip.date_from),
                ('payment_date', '<=', payslip.date_to),
            ])
            installment_line.state = 'unpaid' if not payslip.is_refund_payslip else 'paid'
            installment_line.installment_id.state = 'approved' if not payslip.is_refund_payslip else 'paid'
        return res


