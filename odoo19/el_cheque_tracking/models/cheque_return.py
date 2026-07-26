# -*- coding: utf-8 -*-
"""Cheque return record.

A ``cheque.return`` records a single return event: when it happened,
why, and what bank charges + penalty (if any) were applied. The actual
accounting entries are posted by ``cheque.cheque._apply_return`` so that
they appear on the cheque's audit trail; this model exists for historical
queryability.
"""
from odoo import fields, models


class ChequeReturn(models.Model):
    _name = "cheque.return"
    _description = "Cheque Return"
    _order = "return_date desc, id desc"
    _rec_name = "name"

    name = fields.Char(
        string="Reference",
        default="New",
        readonly=True,
        copy=False,
        required=True,
    )
    cheque_id = fields.Many2one(
        string="Cheque",
        comodel_name="cheque.cheque",
        required=True,
        ondelete="restrict",
        index=True,
    )
    return_date = fields.Date(string="Return Date", required=True, default=fields.Date.context_today)
    return_reason_id = fields.Many2one(
        string="Return Reason",
        comodel_name="cheque.return.reason",
        required=True,
    )
    bank_charges = fields.Monetary(
        string="Bank Charges",
        currency_field="currency_id",
        default=0.0,
    )
    penalty_amount = fields.Monetary(
        string="Penalty Amount",
        currency_field="currency_id",
        default=0.0,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        related="cheque_id.currency_id",
        readonly=True,
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        related="cheque_id.company_id",
        readonly=True,
        store=True,
    )
    notes = fields.Text(string="Notes")
    move_ids = fields.One2many(
        string="Related Journal Entries",
        comodel_name="account.move",
        inverse_name="cheque_return_id",
        readonly=True,
    )
