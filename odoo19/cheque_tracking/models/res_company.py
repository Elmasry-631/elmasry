from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    cheque_received_account_id = fields.Many2one("account.account", string="Cheques Received Account")
    cheque_under_collection_account_id = fields.Many2one("account.account", string="Cheques Under Collection Account")
    cheque_issued_account_id = fields.Many2one("account.account", string="Cheques Issued Account")
    cheque_bank_charges_account_id = fields.Many2one("account.account", string="Cheque Bank Charges Account")
    cheque_penalty_income_account_id = fields.Many2one("account.account", string="Cheque Penalty Income Account")
    cheque_stale_months = fields.Integer(string="Stale Cheque Months", default=6)
    cheque_pdc_reminder_days = fields.Integer(string="PDC Reminder Days", default=7)
    cheque_max_redeposit_attempts = fields.Integer(string="Maximum Re-Deposit Attempts", default=2)
    cheque_approval_threshold = fields.Monetary(
        string="Issued Cheque Approval Threshold",
        currency_field="currency_id",
        default=0.0,
    )
