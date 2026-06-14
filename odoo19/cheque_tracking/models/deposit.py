from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChequeDeposit(models.Model):
    _name = "cheque.deposit"
    _description = "Cheque Deposit"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "deposit_date desc, id desc"

    name = fields.Char(default="New", readonly=True, copy=False, required=True)
    deposit_date = fields.Date(required=True, default=fields.Date.context_today, tracking=True)
    bank_journal_id = fields.Many2one(
        "account.journal",
        required=True,
        domain=[("type", "=", "bank")],
        tracking=True,
    )
    cheque_ids = fields.One2many("cheque.cheque", "deposit_id", string="Cheques")
    total_amount = fields.Monetary(compute="_compute_total_amount", store=True, currency_field="currency_id")
    currency_id = fields.Many2one(related="company_id.currency_id", readonly=True)
    journal_entry_id = fields.Many2one("account.move", readonly=True, copy=False)
    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="draft",
        tracking=True,
    )
    notes = fields.Text()
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"].sudo()
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = sequence.next_by_code("cheque.deposit") or "New"
        return super().create(vals_list)

    @api.depends("cheque_ids.amount_company_currency")
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.cheque_ids.mapped("amount_company_currency"))

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                raise UserError(_("Only draft deposits can be confirmed."))
            if not rec.cheque_ids:
                raise UserError(_("Please add at least one cheque."))
            for cheque in rec.cheque_ids:
                cheque.deposit_account_id = rec.bank_journal_id
                cheque.action_deposit()
                rec.journal_entry_id = cheque.journal_entry_id
            rec.state = "confirmed"
            rec.message_post(body=_("Deposit confirmed."))
        return self.action_print_deposit_slip()

    def action_cancel(self):
        for rec in self:
            if rec.state == "confirmed":
                raise UserError(_("Confirmed deposits cannot be cancelled. Return the cheques instead."))
            rec.state = "cancelled"

    def action_print_deposit_slip(self):
        self.ensure_one()
        return self.env.ref("cheque_tracking.action_report_deposit_slip").report_action(self)
