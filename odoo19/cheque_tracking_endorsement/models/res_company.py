from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    cheque_allow_post_dated_endorsement = fields.Boolean(string="Allow Endorsement Before Due Date")
    cheque_endorsement_reminder_days = fields.Integer(string="Endorsement Reminder Days", default=3)
    cheque_endorsement_payable_account_id = fields.Many2one("account.account", string="Cheque Endorsement Payable Account")
    cheque_endorsement_bill_account_id = fields.Many2one("account.account", string="Cheque Endorsement Bill Account")
