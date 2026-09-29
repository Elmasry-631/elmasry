# investment_club/reports/renewal_due_report.py
from odoo import models, api, fields


class RenewalDueReport(models.AbstractModel):
    _name = 'report.investment_club.renewal_due'
    _description = 'Renewal Due Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        today = fields.Date.today()
        
        due_memberships = self.env['investment.membership'].search([
            ('state', '=', 'active'),
            ('next_renewal_date', '<=', today),
        ])
        
        report_data = []
        total_due = 0
        total_overdue = 0
        
        for mem in due_memberships:
            days_overdue = (today - mem.expiry_date).days if mem.expiry_date < today else 0
            status = 'Overdue' if days_overdue > 0 else 'Due Today'
            
            report_data.append({
                'membership_number': mem.membership_number,
                'investor_code': mem.investor_code or '',
                'partner': mem.partner_id.name,
                'phone': mem.partner_id.phone or '',
                'club': mem.club_id.display_name or mem.club_id.name or '',
                'expiry_date': mem.expiry_date,
                'days_overdue': days_overdue,
                'due_amount': mem.annual_subscription_fee,
                'status': status,
            })
            
            if days_overdue > 0:
                total_overdue += mem.annual_subscription_fee
            else:
                total_due += mem.annual_subscription_fee
        
        return {
            'date': today,
            'memberships': report_data,
            'total_due': total_due,
            'total_overdue': total_overdue,
            'grand_total': total_due + total_overdue,
            'count': len(due_memberships),
        }
