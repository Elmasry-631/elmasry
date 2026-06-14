from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cheque_allow_post_dated_endorsement = fields.Boolean(
        related="company_id.cheque_allow_post_dated_endorsement",
        readonly=False,
    )
    cheque_endorsement_reminder_days = fields.Integer(
        related="company_id.cheque_endorsement_reminder_days",
        readonly=False,
    )
    cheque_endorsement_payable_account_id = fields.Many2one(
        related="company_id.cheque_endorsement_payable_account_id",
        readonly=False,
    )
    cheque_endorsement_bill_account_id = fields.Many2one(
        related="company_id.cheque_endorsement_bill_account_id",
        readonly=False,
    )
