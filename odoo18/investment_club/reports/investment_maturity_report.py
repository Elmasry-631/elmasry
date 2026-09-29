# investment_club/reports/investment_maturity_report.py
from odoo import models, api, fields


class InvestmentMaturityReport(models.AbstractModel):
    _name = 'report.investment_club.investment_maturity'
    _description = 'Investment Maturity Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('state', 'in', ('paid', 'active'))]
        if docids:
            domain.append(('id', 'in', docids))

        subscriptions = self.env['investment.subscription'].search(domain)

        report_data = []
        total_invested = 0
        total_capital_due = 0

        for sub in subscriptions:
            # Maturity Principal = Investment amount minus total paid returns
            total_returns_paid = sub.total_actual_returns or 0.0
            capital_due = sub.amount - total_returns_paid
            if capital_due < 0:
                capital_due = 0.0

            last_return_date = sub.last_return_date or ''

            report_data.append({
                'investor': sub.partner_id.name or '',
                'project': sub.project_id.name or '',
                'investment_amount': sub.amount,
                'investment_date': sub.investment_date,
                'contract_end_date': sub.contract_end_date or '',
                'capital_due': capital_due,
                'last_return_date': last_return_date,
            })
            total_invested += sub.amount
            total_capital_due += capital_due

        return {
            'date': fields.Date.today(),
            'data': report_data,
            'total_invested': total_invested,
            'total_capital_due': total_capital_due,
            'count': len(subscriptions),
        }
