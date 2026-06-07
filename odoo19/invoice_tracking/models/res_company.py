from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    cheque_received_account_id = fields.Many2one('account.account', string='Cheques Received Account')
    cheque_under_collection_account_id = fields.Many2one('account.account', string='Cheques Under Collection Account')
    cheque_issued_account_id = fields.Many2one('account.account', string='Cheques Issued Account')

