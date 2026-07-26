# -*- coding: utf-8 -*-
"""Batch deposit model.

A ``cheque.deposit`` groups multiple holding received cheques into a
single deposit batch posted to one bank journal. On confirmation the
deposit triggers ``cheque.cheque.action_deposit()`` for each linked
cheque, which posts the deposit accounting entry (Dr Under Collection /
Cr Cheques Received).
"""
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChequeDeposit(models.Model):
    _name = "cheque.deposit"
    _description = "Cheque Deposit"
    _inherit = ["mail.thread"]
    _order = "deposit_date desc, id desc"
    _rec_name = "name"

    name = fields.Char(
        string="Reference",
        default="New",
        readonly=True,
        copy=False,
        required=True,
        tracking=True,
    )
    deposit_date = fields.Date(
        string="Deposit Date",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    bank_journal_id = fields.Many2one(
        string="Bank Journal",
        comodel_name="account.journal",
        domain="[('type', '=', 'bank')]",
        required=True,
        tracking=True,
    )
    cheque_ids = fields.Many2many(
        string="Cheques",
        comodel_name="cheque.cheque",
        relation="cheque_deposit_cheque_rel",
        column1="deposit_id",
        column2="cheque_id",
        domain="[('cheque_type', '=', 'received'), ('state', 'in', ('holding', 'returned'))]",
    )
    total_amount = fields.Monetary(
        string="Total Amount",
        compute="_compute_total_amount",
        currency_field="currency_id",
        store=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    state = fields.Selection(
        string="Status",
        selection=[("draft", "Draft"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        required=True,
        default="draft",
        tracking=True,
        copy=False,
    )
    notes = fields.Text(string="Notes")
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    @api.depends("cheque_ids", "cheque_ids.amount", "currency_id")
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.cheque_ids.mapped("amount"))

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"].sudo()
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = sequence.next_by_code("cheque.deposit") or "New"
        return super().create(vals_list)

    def action_confirm(self):
        """Confirm the deposit: trigger action_deposit on each cheque."""
        for rec in self:
            if rec.state != "draft":
                raise UserError(_("Only draft deposits can be confirmed."))
            if not rec.cheque_ids:
                raise UserError(_("Please add at least one cheque."))
            for cheque in rec.cheque_ids:
                # Temporarily set the deposit journal on each cheque so its
                # accounting entries hit the right bank journal.
                cheque.deposit_account_id = rec.bank_journal_id
                cheque.deposit_id = rec.id
                cheque.action_deposit()
            rec.state = "confirmed"
            rec.message_post(body=_("Deposit confirmed."))

    def action_cancel(self):
        """Cancel only draft deposits (confirmed ones need cheque returns)."""
        for rec in self:
            if rec.state == "confirmed":
                raise UserError(
                    _("Confirmed deposits cannot be cancelled. Return the cheques first.")
                )
            rec.state = "cancelled"
            rec.message_post(body=_("Deposit cancelled."))

    def action_print_slip(self):
        self.ensure_one()
        return self.env.ref(
            "el_cheque_tracking.action_report_deposit_slip"
        ).report_action(self)
