# -*- coding: utf-8 -*-
"""Return reason configuration.

Each return reason has a code, a name and an optional default penalty
amount that the return wizard will prefill when the user selects it.
"""
from odoo import fields, models


class ChequeReturnReason(models.Model):
    _name = "cheque.return.reason"
    _description = "Cheque Return Reason"
    _order = "sequence, id"
    _rec_name = "name"

    name = fields.Char(string="Reason", required=True, translate=True)
    code = fields.Char(string="Code", required=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    default_penalty = fields.Monetary(
        string="Default Penalty",
        currency_field="currency_id",
        default=0.0,
        help="Default penalty amount prefilled in the return wizard when "
             "this reason is selected.",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        default=lambda self: self.env.company.currency_id,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    _code_uniq = models.Constraint(
        "unique(code, company_id)",
        "Return reason code must be unique per company.",
    )
