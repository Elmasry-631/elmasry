from odoo import models



class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_paid(self):
        res = super(HrPayslip, self).action_payslip_paid()
        for payslip in self:
            deduction = self.env['deduction.deduction'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('state', '=', 'approved') if not payslip.is_refund_payslip else ('state', 'in', ['done', 'approved']),
                ('date', '>=', payslip.date_from),
                ('date', '<=', payslip.date_to),
            ])
            deduction.state = 'done' if not payslip.is_refund_payslip else 'approved'
        return res

    def action_payslip_unpaid(self):
        res = super(HrPayslip, self).action_payslip_unpaid()
        for payslip in self:
            deduction = self.env['deduction.deduction'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('state', '=', 'done') if not payslip.is_refund_payslip else ('state', '=', 'approved'),
                ('date', '>=', payslip.date_from),
                ('date', '<=', payslip.date_to),
            ])
            deduction.state = 'approved' if not payslip.is_refund_payslip else 'done'
        return res

    def action_payslip_cancel(self):
        res = super(HrPayslip, self).action_payslip_cancel()
        for payslip in self:
            deduction = self.env['deduction.deduction'].search([
                ('employee_id', '=', payslip.employee_id.id),
                ('state', '=', 'done') if not payslip.is_refund_payslip else ('state', '=', 'approved'),
                ('date', '>=', payslip.date_from),
                ('date', '<=', payslip.date_to),
            ])
            deduction.state = 'approved' if not payslip.is_refund_payslip else 'done'
        return res


