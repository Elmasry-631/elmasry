# -*- coding: utf-8 -*-
"""Batch deposit wizard: pick multiple holding cheques + a bank journal.

Creates a ``cheque.deposit`` record and triggers ``action_deposit()``
on each selected cheque, which posts the deposit accounting entry
(Dr Under Collection / Cr Cheques Received) for each.
"""
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChequeDepositWizard(models.TransientModel):
    _name = "cheque.deposit.wizard"
    _description = "Cheque Deposit Wizard"

    deposit_date = fields.Date(
        string="Deposit Date",
        required=True,
        default=fields.Date.context_today,
    )
    bank_journal_id = fields.Many2one(
        string="Bank Journal",
        comodel_name="account.journal",
        domain="[('type', '=', 'bank')]",
        required=True,
    )
    cheque_ids = fields.Many2many(
        string="Cheques",
        comodel_name="cheque.cheque",
        relation="cheque_deposit_wiz_cheque_rel",
        column1="wizard_id",
        column2="cheque_id",
        domain="[('cheque_type', '=', 'received'), ('state', 'in', ('holding', 'returned'))]",
    )
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company,
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Pre-fill cheques from active_ids in context (called from list view)
        active_ids = self.env.context.get("active_ids", [])
        if active_ids and self.env.context.get("active_model") == "cheque.cheque":
            cheques = self.env["cheque.cheque"].browse(active_ids)
            res["cheque_ids"] = [(6, 0, cheques.ids)]
        return res

    def action_create_deposit(self):
        self.ensure_one()
        if not self.cheque_ids:
            raise UserError(_("Please select at least one cheque."))
        today = fields.Date.context_today(self)
        for cheque in self.cheque_ids:
            if cheque.is_post_dated and cheque.due_date and cheque.due_date > today:
                raise UserError(
                    _("Cannot deposit post-dated cheques before their due date: %s")
                    % cheque.display_name
                )
            if cheque.state == "returned":
                max_attempts = self.company_id.cheque_max_redeposits or 0
                if max_attempts and cheque.return_count >= max_attempts:
                    raise UserError(
                        _("Maximum re-deposit attempts exceeded for: %s")
                        % cheque.display_name
                    )
        deposit = self.env["cheque.deposit"].sudo().create({
            "deposit_date": self.deposit_date,
            "bank_journal_id": self.bank_journal_id.id,
            "cheque_ids": [(6, 0, self.cheque_ids.ids)],
            "company_id": self.company_id.id,
        })
        deposit.action_confirm()
        return {
            "name": _("Deposit"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.deposit",
            "view_mode": "form",
            "res_id": deposit.id,
        }
