from odoo import _, fields, models
from odoo.exceptions import UserError


class ChequeReturnWizard(models.TransientModel):
    _name = "cheque.return.wizard"
    _description = "Cheque Return Wizard"

    cheque_id = fields.Many2one("cheque.cheque", required=True)
    return_date = fields.Date(required=True, default=fields.Date.context_today)
    return_reason_id = fields.Many2one("cheque.return.reason", required=True)
    bank_charges = fields.Monetary(default=0.0, currency_field="currency_id")
    penalty_amount = fields.Monetary(default=0.0, currency_field="currency_id")
    create_activity = fields.Boolean(default=True)
    notes = fields.Text()
    currency_id = fields.Many2one(related="cheque_id.currency_id", readonly=True)

    def action_return_cheque(self):
        self.ensure_one()
        cheque = self.cheque_id
        if cheque.state not in ("deposited", "cleared", "handed_over"):
            raise UserError(_("Only deposited, cleared, or handed-over cheques can be returned."))
        return_record = self.env["cheque.return"].create({
            "cheque_id": cheque.id,
            "return_date": self.return_date,
            "return_reason_id": self.return_reason_id.id,
            "bank_charges": self.bank_charges,
            "penalty_amount": self.penalty_amount,
            "notes": self.notes,
            "company_id": cheque.company_id.id,
        })
        if cheque.cheque_type == "received":
            credit_account = (
                cheque._bank_account()
                if cheque.state == "cleared"
                else cheque._company_account("cheque_under_collection_account_id", _("Cheques Under Collection Account"))
            )
            cheque._create_move(
                "return",
                _("Return Cheque"),
                cheque._partner_account("receivable"),
                credit_account,
                date=self.return_date,
                extra_vals={"cheque_return_id": return_record.id},
            )
            if self.penalty_amount:
                cheque._create_move(
                    "penalty",
                    _("Cheque Return Penalty"),
                    cheque._partner_account("receivable"),
                    cheque._company_account("cheque_penalty_income_account_id", _("Cheque Penalty Income Account")),
                    date=self.return_date,
                    amount=self.penalty_amount,
                    extra_vals={"cheque_return_id": return_record.id},
                )
        else:
            cheque._create_move(
                "return",
                _("Issued Cheque Returned"),
                cheque._company_account("cheque_issued_account_id", _("Cheques Issued Account")),
                cheque._partner_account("payable"),
                date=self.return_date,
                extra_vals={"cheque_return_id": return_record.id},
            )
        if self.bank_charges:
            cheque._create_move(
                "charges",
                _("Cheque Return Bank Charges"),
                cheque._company_account("cheque_bank_charges_account_id", _("Cheque Bank Charges Account")),
                cheque._bank_account(),
                date=self.return_date,
                amount=self.bank_charges,
                extra_vals={"cheque_return_id": return_record.id},
            )
        cheque.state = "returned"
        cheque.message_post(
            body=_("Cheque returned. Reason: %s") % self.return_reason_id.display_name
        )
        if self.create_activity:
            cheque.activity_schedule(
                "mail.mail_activity_data_todo",
                summary=_("Follow up returned cheque"),
                note=self.notes or _("Follow up returned cheque with partner."),
                user_id=cheque.responsible_id.id or self.env.user.id,
            )
        return {"type": "ir.actions.act_window_close"}

