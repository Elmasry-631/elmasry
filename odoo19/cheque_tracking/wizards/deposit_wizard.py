from odoo import _, fields, models
from odoo.exceptions import UserError


class ChequeDepositWizard(models.TransientModel):
    _name = "cheque.deposit.wizard"
    _description = "Batch Cheque Deposit Wizard"

    deposit_date = fields.Date(required=True, default=fields.Date.context_today)
    bank_journal_id = fields.Many2one("account.journal", required=True, domain=[("type", "=", "bank")])
    cheque_ids = fields.Many2many(
        "cheque.cheque",
        string="Cheques",
        domain=[("cheque_type", "=", "received"), ("state", "in", ("holding", "returned"))],
    )
    notes = fields.Text()

    def action_create_deposit(self):
        self.ensure_one()
        if not self.cheque_ids:
            raise UserError(_("Please select at least one cheque."))
        today = fields.Date.context_today(self)
        invalid = self.cheque_ids.filtered(lambda chq: chq.due_date and chq.due_date > today)
        if invalid:
            raise UserError(_("Cannot deposit post-dated cheques before their due date: %s") % ", ".join(invalid.mapped("name")))
        attempts_exceeded = self.cheque_ids.filtered(
            lambda chq: chq.state == "returned"
            and chq.return_count >= (chq.company_id.cheque_max_redeposit_attempts or 2)
        )
        if attempts_exceeded:
            raise UserError(_("Maximum re-deposit attempts exceeded for: %s") % ", ".join(attempts_exceeded.mapped("name")))
        deposit = self.env["cheque.deposit"].create({
            "deposit_date": self.deposit_date,
            "bank_journal_id": self.bank_journal_id.id,
            "cheque_ids": [(6, 0, self.cheque_ids.ids)],
            "notes": self.notes,
        })
        return deposit.action_confirm()

