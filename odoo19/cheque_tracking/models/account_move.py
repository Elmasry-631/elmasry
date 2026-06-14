from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    cheque_id = fields.Many2one("cheque.cheque", string="Cheque", copy=False, index=True)
    cheque_deposit_id = fields.Many2one("cheque.deposit", string="Cheque Deposit", copy=False, index=True)
    cheque_return_id = fields.Many2one("cheque.return", string="Cheque Return", copy=False, index=True)
    cheque_stage = fields.Selection(
        [
            ("receive", "Receive Cheque"),
            ("deposit", "Deposit Cheque"),
            ("clear", "Clear Cheque"),
            ("return", "Return Cheque"),
            ("charges", "Bank Charges"),
            ("penalty", "Penalty"),
            ("issue", "Issue Cheque"),
            ("cash", "Cash Cheque"),
        ],
        string="Cheque Stage",
        copy=False,
    )
