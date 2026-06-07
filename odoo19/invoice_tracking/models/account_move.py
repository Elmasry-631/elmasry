from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    code_id = fields.Many2one('partner.code')
    check_tracking_id = fields.Many2one('check.tracking', string='Cheque Tracking', copy=False)
    check_stage = fields.Selection([
        ('receive', 'Receive Cheque'),
        ('deposit', 'Deposit Cheque'),
        ('clear', 'Cheque Cleared'),
        ('bounce', 'Cheque Bounced'),
        ('issue', 'Issue Cheque'),
        ('cash', 'Cheque Cashed'),
    ], string='Cheque Stage', copy=False)



    @api.onchange('code_id')
    def change_partner(self):
        if self.code_id:
            self.partner_id = self.env['res.partner'].search([('code_id', '=', self.code_id.id)], limit=1)
