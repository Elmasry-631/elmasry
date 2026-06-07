from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cheque_received_account_id = fields.Many2one(
        related='company_id.cheque_received_account_id',
        readonly=False,
    )
    cheque_under_collection_account_id = fields.Many2one(
        related='company_id.cheque_under_collection_account_id',
        readonly=False,
    )
    cheque_issued_account_id = fields.Many2one(
        related='company_id.cheque_issued_account_id',
        readonly=False,
    )

