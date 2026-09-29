# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class VehicleInstallmentLine(models.Model):
    _name = 'vehicle.installment.line'
    _description = 'Vehicle Installment Line'

    installment_id = fields.Many2one('vehicle.installment', string='Installment', ondelete='cascade')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', related='installment_id.vehicle_id', store=True)
    employee_id = fields.Many2one('hr.employee', string='Employee', related='installment_id.employee_id', store=True)
    payment_date = fields.Date(string='Payment Date', required=True)
    amount = fields.Monetary(string='Amount', currency_field='currency_id', required=True)
    state = fields.Selection([
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid')
    ], default='unpaid', string='Payment Status')
    
    installment_state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ], related='installment_id.state', store=True, string='Installment Status')
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='installment_id.company_id',
        index=True,
        store=True
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        required=False,
        related='installment_id.currency_id',
        store=True
    )
    
    note = fields.Html(string='Note')

    def write(self, vals_list):
        res = super(VehicleInstallmentLine, self).write(vals_list)
        if 'amount' in vals_list:
            for line in self:
                all_lines = line.installment_id.installment_lines

                later_installments = all_lines.filtered(
                    lambda l: l.payment_date and l.payment_date > line.payment_date and l.state == 'unpaid'
                )

                if later_installments:
                    earlier_installments = all_lines.filtered(
                        lambda l: l.payment_date and l.payment_date < line.payment_date
                    )

                    earlier_installments_amount = sum(earlier_installments.mapped('amount'))

                    loan_amount = line.installment_id.total_amount
                    total_amount_due = loan_amount - earlier_installments_amount - line.amount
                    amount_due_per_month = total_amount_due / len(later_installments)

                    later_installments.write({'amount': amount_due_per_month})

        return res