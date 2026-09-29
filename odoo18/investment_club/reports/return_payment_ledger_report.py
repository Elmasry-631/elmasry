# investment_club/reports/return_payment_ledger_report.py
from odoo import models, api, fields


class ReturnPaymentLedgerReport(models.AbstractModel):
    _name = 'report.investment_club.return_payment_ledger'
    _description = 'Return Payment Ledger Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        # Get all paid return payments
        domain = [('state', '=', 'paid')]
        if docids:
            domain.append(('id', 'in', docids))

        returns = self.env['investment.actual.return'].search(domain, order='date_from desc')

        report_data = []
        total_expected = 0
        total_actual = 0

        for ret in returns:
            report_data.append({
                'investor': ret.partner_id.name or '',
                'membership_number': ret.membership_id.membership_number or '',
                'project': ret.project_id.name or '',
                'return_type': dict(ret._fields['return_type'].selection).get(ret.return_type, ret.return_type),
                'period': ret.period_name or '',
                'expected_amount': ret.expected_amount,
                'actual_amount': ret.actual_amount,
                'difference': ret.difference,
                'state': dict(ret._fields['state'].selection).get(ret.state, ret.state),
                'payment_date': ret.payment_id.date if ret.payment_id else '',
            })
            total_expected += ret.expected_amount
            total_actual += ret.actual_amount

        return {
            'date': fields.Date.today(),
            'data': report_data,
            'total_expected': total_expected,
            'total_actual': total_actual,
            'total_difference': total_actual - total_expected,
            'count': len(returns),
        }
