from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cheque_received_account_id = fields.Many2one(related="company_id.cheque_received_account_id", readonly=False)
    cheque_under_collection_account_id = fields.Many2one(
        related="company_id.cheque_under_collection_account_id",
        readonly=False,
    )
    cheque_issued_account_id = fields.Many2one(related="company_id.cheque_issued_account_id", readonly=False)
    cheque_bank_charges_account_id = fields.Many2one(
        related="company_id.cheque_bank_charges_account_id",
        readonly=False,
    )
    cheque_penalty_income_account_id = fields.Many2one(
        related="company_id.cheque_penalty_income_account_id",
        readonly=False,
    )
    cheque_stale_months = fields.Integer(related="company_id.cheque_stale_months", readonly=False)
    cheque_pdc_reminder_days = fields.Integer(related="company_id.cheque_pdc_reminder_days", readonly=False)
    cheque_max_redeposit_attempts = fields.Integer(related="company_id.cheque_max_redeposit_attempts", readonly=False)
    cheque_approval_threshold = fields.Monetary(
        related="company_id.cheque_approval_threshold",
        readonly=False,
        currency_field="currency_id",
    )
