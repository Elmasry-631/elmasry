# investment_club/reports/investor_statement_report.py
from odoo import models, api, fields


class InvestorStatementReport(models.AbstractModel):
    _name = 'report.investment_club.investor_statement'
    _description = 'Investor Investment Statement Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        domain = [('state', '=', 'active')]
        if docids:
            domain.append(('id', 'in', docids))

        memberships = self.env['investment.membership'].search(domain)

        report_data = []
        grand_total_invested = 0
        grand_total_returns_due = 0
        grand_total_returns_paid = 0
        grand_total_remaining = 0
        grand_total_admin_fees = 0
        grand_total_net_due = 0

        for mem in memberships:
            investments = mem.investment_ids.filtered(lambda i: i.state in ('paid', 'active'))

            total_invested = sum(inv.amount for inv in investments)

            # Expected Returns
            total_returns_due = 0.0
            for inv in investments:
                returns = inv.actual_return_ids.filtered(lambda r: r.state != 'cancelled')
                total_returns_due += sum(r.expected_amount for r in returns)

            # Actual Paid Returns
            total_returns_paid = sum(inv.total_actual_returns or 0.0 for inv in investments)

            # Remaining
            remaining = total_returns_due - total_returns_paid

            # Administrative Fees
            admin_fees = mem.club_id.administrative_fees or 0.0

            # Net Due
            net_due = remaining - admin_fees

            report_data.append({
                'investor': mem.partner_id.name or '',
                'membership_number': mem.membership_number or '',
                'investor_code': mem.investor_code or '',
                'club': mem.club_id.display_name or '',
                'total_invested': total_invested,
                'total_returns_due': total_returns_due,
                'total_returns_paid': total_returns_paid,
                'remaining': remaining,
                'admin_fees': admin_fees,
                'net_due': net_due,
            })

            grand_total_invested += total_invested
            grand_total_returns_due += total_returns_due
            grand_total_returns_paid += total_returns_paid
            grand_total_remaining += remaining
            grand_total_admin_fees += admin_fees
            grand_total_net_due += net_due

        return {
            'date': fields.Date.today(),
            'data': report_data,
            'grand_total_invested': grand_total_invested,
            'grand_total_returns_due': grand_total_returns_due,
            'grand_total_returns_paid': grand_total_returns_paid,
            'grand_total_remaining': grand_total_remaining,
            'grand_total_admin_fees': grand_total_admin_fees,
            'grand_total_net_due': grand_total_net_due,
            'count': len(memberships),
        }
