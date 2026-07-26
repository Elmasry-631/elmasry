# -*- coding: utf-8 -*-
"""Return wizard: select reason + optional bank charges + penalty.

Delegates the accounting work to ``cheque.cheque._apply_return()``,
which reverses the latest move and posts optional charges + penalty
entries on the cheque's audit trail.
"""
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChequeReturnWizard(models.TransientModel):
    _name = "cheque.return.wizard"
    _description = "Cheque Return Wizard"

    cheque_id = fields.Many2one(
        string="Cheque",
        comodel_name="cheque.cheque",
        required=True,
        ondelete="restrict",
    )
    return_date = fields.Date(
        string="Return Date",
        required=True,
        default=fields.Date.context_today,
    )
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
    notes = fields.Text(string="Notes")

    @api.onchange("return_reason_id")
    def _onchange_return_reason_id(self):
        if self.return_reason_id and self.return_reason_id.default_penalty:
            self.penalty_amount = self.return_reason_id.default_penalty

    def action_submit_return(self):
        self.ensure_one()
        cheque = self.cheque_id
        if cheque.state not in ("deposited", "cleared", "handed_over"):
            raise UserError(
                _("Only deposited, cleared, or handed-over cheques can be returned.")
            )
        return_record = cheque._apply_return(
            return_date=self.return_date,
            reason_id=self.return_reason_id.id,
            bank_charges=self.bank_charges,
            penalty_amount=self.penalty_amount,
        )
        if self.notes:
            return_record.notes = self.notes
        return {
            "name": _("Cheque Return"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.return",
            "view_mode": "form",
            "res_id": return_record.id,
        }
