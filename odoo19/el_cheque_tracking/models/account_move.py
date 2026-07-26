# -*- coding: utf-8 -*-
"""Account.move extension: link moves to cheques + track lifecycle stage."""
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    cheque_id = fields.Many2one(
        string="Cheque",
        comodel_name="cheque.cheque",
        ondelete="restrict",
        index=True,
        copy=False,
    )
    cheque_return_id = fields.Many2one(
        string="Cheque Return",
        comodel_name="cheque.return",
        ondelete="restrict",
        index=True,
        copy=False,
    )
    cheque_stage = fields.Selection(
        string="Cheque Stage",
        selection=[
            ("receipt", "Receipt"),
            ("deposit", "Deposit"),
            ("clearance", "Clearance"),
            ("return", "Return"),
            ("issue", "Issue"),
            ("cash", "Cash"),
            ("void", "Void"),
        ],
        copy=False,
        index=True,
    )
