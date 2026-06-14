from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChequeCheque(models.Model):
    _inherit = "cheque.cheque"

    is_endorsable = fields.Boolean(default=True, tracking=True)
    is_crossed = fields.Boolean(tracking=True)
    original_beneficiary_id = fields.Many2one("res.partner", tracking=True)
    current_endorsee_id = fields.Many2one("res.partner", string="Current Endorsee", related="partner_id", store=True, readonly=True)
    endorsement_ids = fields.One2many("cheque.endorsement", "cheque_id", string="Endorsements", readonly=True)
    endorsement_count = fields.Integer(compute="_compute_endorsement_count", store=True)
    state = fields.Selection(selection_add=[("endorsed", "Endorsed")], ondelete={"endorsed": "set default"})

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records.filtered(lambda c: c.cheque_type == "received" and not c.original_beneficiary_id):
            record.original_beneficiary_id = record.partner_id
        return records

    def init(self):
        self.env.cr.execute("""
            UPDATE cheque_cheque
               SET is_endorsable = TRUE
             WHERE is_endorsable IS NULL
        """)
        self.env.cr.execute("""
            UPDATE cheque_cheque
               SET original_beneficiary_id = partner_id
             WHERE original_beneficiary_id IS NULL
               AND cheque_type = 'received'
               AND partner_id IS NOT NULL
        """)

    def write(self, vals):
        if "is_endorsable" in vals:
            for rec in self:
                if rec.endorsement_count or rec.state in ("endorsed", "deposited", "cleared", "cashed", "returned", "cancelled", "void"):
                    raise UserError(_("You cannot change the endorsable flag after endorsement or lifecycle progression."))
        return super().write(vals)

    @api.depends("endorsement_ids")
    def _compute_endorsement_count(self):
        for rec in self:
            rec.endorsement_count = len(rec.endorsement_ids)

    @api.depends("due_date", "cheque_date", "company_id.cheque_stale_months", "state")
    def _compute_date_flags(self):
        super()._compute_date_flags()
        today = fields.Date.context_today(self)
        for rec in self:
            stale_months = rec.company_id.cheque_stale_months or 6
            if rec.cheque_date and rec.state == "endorsed":
                rec.is_stale = rec.cheque_date < today - relativedelta(months=stale_months)

    def _check_endorsement_allowed(self):
        for rec in self:
            if rec.cheque_type != "received":
                raise UserError(_("Only received cheques can be endorsed."))
            if rec.state not in ("holding", "endorsed"):
                raise UserError(_("This cheque cannot be endorsed in its current state."))
            if not rec.is_endorsable:
                raise UserError(_("This cheque is not endorsable and can only be cashed by the first beneficiary."))
            if rec.due_date and rec.due_date > fields.Date.context_today(rec) and not rec.company_id.cheque_allow_post_dated_endorsement:
                raise UserError(_("Post-dated cheques cannot be endorsed before their due date."))
            if not (
                self.env.user.has_group("cheque_tracking_endorsement.group_cheque_endorse")
                or self.env.user.has_group("cheque_tracking.group_cheque_manager")
                or self.env.user.has_group("cheque_tracking.group_cheque_admin")
            ):
                raise UserError(_("You do not have permission to endorse cheques."))

    def _endorsement_payable_account(self):
        self.ensure_one()
        account = self.company_id.cheque_endorsement_payable_account_id
        if not account:
            raise UserError(_("Please configure the cheque endorsement payable account."))
        return account

    def _endorsement_bill_account(self):
        self.ensure_one()
        account = self.company_id.cheque_endorsement_bill_account_id
        if not account:
            raise UserError(_("Please configure the cheque endorsement bill account."))
        return account

    def _partner_account_for(self, partner, account_type):
        self.ensure_one()
        account = partner.property_account_receivable_id if account_type == "receivable" else partner.property_account_payable_id
        if not account:
            raise UserError(_("Please configure the accounting account for partner %s.") % partner.display_name)
        return account

    def _create_endorsement_move(self, endorser, endorsee, endorsement_date):
        self.ensure_one()
        journal = self.deposit_account_id
        if not journal:
            raise UserError(_("Please select the cheque bank journal."))
        amount = self._to_company_currency(self.amount, date=endorsement_date)
        checks_receivable = self._company_account("cheque_received_account_id", _("Cheques Received Account"))
        checks_payable = self._endorsement_payable_account()
        endorsee_payable = self._partner_account_for(endorsee, "payable")
        line_ids = []

        if checks_payable == checks_receivable:
            raise UserError(_("Cheque endorsement payable account must be different from cheques received account."))

        # If the intermediary account collapses with the supplier payable account,
        # post the effective transfer only to avoid a redundant zero-net pair.
        if checks_payable == endorsee_payable:
            line_ids = [
                (0, 0, {
                    "name": _("Cheque Endorsement"),
                    "partner_id": endorsee.id,
                    "account_id": endorsee_payable.id,
                    "debit": amount,
                    "credit": 0.0,
                }),
                (0, 0, {
                    "name": _("Cheque Endorsement"),
                    "partner_id": endorser.id,
                    "account_id": checks_receivable.id,
                    "debit": 0.0,
                    "credit": amount,
                }),
            ]
        else:
            line_ids = [
                (0, 0, {
                    "name": _("Cheque Endorsement"),
                    "account_id": checks_payable.id,
                    "debit": amount,
                    "credit": 0.0,
                }),
                (0, 0, {
                    "name": _("Cheque Endorsement"),
                    "partner_id": endorser.id,
                    "account_id": checks_receivable.id,
                    "debit": 0.0,
                    "credit": amount,
                }),
                (0, 0, {
                    "name": _("Cheque Endorsement"),
                    "partner_id": endorsee.id,
                    "account_id": endorsee_payable.id,
                    "debit": amount,
                    "credit": 0.0,
                }),
                (0, 0, {
                    "name": _("Cheque Endorsement"),
                    "account_id": checks_payable.id,
                    "debit": 0.0,
                    "credit": amount,
                }),
            ]
        move = self.env["account.move"].create({
            "move_type": "entry",
            "date": endorsement_date,
            "journal_id": journal.id,
            "ref": "%s - %s" % (self.name, _("Cheque Endorsement")),
            "cheque_id": self.id,
            "cheque_stage": "endorse",
            "line_ids": line_ids,
        })
        move.action_post()
        self.journal_entry_id = move
        return move

    def _create_vendor_bill_for_endorsement(self, endorsee, endorsement_date, endorsement):
        self.ensure_one()
        bill = self.env["account.move"].create({
            "move_type": "in_invoice",
            "partner_id": endorsee.id,
            "invoice_date": endorsement_date,
            "ref": "%s - %s" % (self.name, _("Cheque Endorsement")),
            "cheque_endorsement_id": endorsement.id,
            "invoice_line_ids": [
                (0, 0, {
                    "name": _("Cheque Endorsement %s") % self.cheque_number,
                    "quantity": 1.0,
                    "price_unit": self.amount,
                    "account_id": self._endorsement_bill_account().id,
                }),
            ],
        })
        return bill

    def action_open_endorse_wizard(self):
        self.ensure_one()
        self._check_endorsement_allowed()
        return {
            "name": _("Endorse Cheque"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.endorse.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_cheque_id": self.id,
                "default_current_beneficiary_id": self.partner_id.id,
            },
        }

    def action_endorse(self, endorsee_partner, endorsement_date=False, reason=False, create_vendor_bill=True):
        self.ensure_one()
        self._check_endorsement_allowed()
        endorsee_partner = endorsee_partner if isinstance(endorsee_partner, models.BaseModel) else self.env["res.partner"].browse(endorsee_partner)
        if not endorsee_partner.exists() or not endorsee_partner.active:
            raise UserError(_("The new beneficiary must be an active partner."))
        if endorsee_partner == self.partner_id:
            raise UserError(_("The new beneficiary must be different from the current beneficiary."))
        endorsement_date = endorsement_date or fields.Date.context_today(self)
        endorser = self.partner_id
        move = self._create_endorsement_move(endorser, endorsee_partner, endorsement_date)
        endorsement = self.env["cheque.endorsement"].create({
            "cheque_id": self.id,
            "endorser_id": endorser.id,
            "endorsee_id": endorsee_partner.id,
            "endorsement_date": endorsement_date,
            "reason": reason,
            "move_id": move.id,
            "state": "confirmed",
        })
        move.cheque_endorsement_id = endorsement
        bill = self.env["account.move"]
        if create_vendor_bill:
            bill = self._create_vendor_bill_for_endorsement(endorsee_partner, endorsement_date, endorsement)
            endorsement.vendor_bill_id = bill
        self.write({
            "partner_id": endorsee_partner.id,
            "state": "endorsed",
            "original_beneficiary_id": self.original_beneficiary_id.id or endorser.id,
        })
        self.message_post(
            body=_("Cheque endorsed from %s to %s.")
            % (endorser.display_name, endorsee_partner.display_name)
        )
        return endorsement

    def action_deposit(self):
        self._check_state(["holding", "endorsed", "returned"])
        for rec in self:
            if rec.state == "endorsed":
                if rec.cheque_type != "received":
                    raise UserError(_("Only received cheques can be deposited."))
                if rec.due_date and rec.due_date > fields.Date.context_today(rec):
                    raise UserError(_("Cannot deposit a post-dated cheque before its due date."))
                if rec.state == "returned" and rec.return_count >= rec.company_id.cheque_max_redeposit_attempts:
                    raise UserError(_("Cannot re-deposit cheque. Maximum re-deposit attempts (%s) exceeded.") % rec.company_id.cheque_max_redeposit_attempts)
                rec._create_move(
                    "deposit",
                    _("Deposit Cheque"),
                    rec._company_account("cheque_under_collection_account_id", _("Cheques Under Collection Account")),
                    rec._company_account("cheque_received_account_id", _("Cheques Received Account")),
                )
                rec.state = "deposited"
                rec.message_post(body=_("Endorsed cheque deposited under collection."))
            else:
                super(ChequeCheque, rec).action_deposit()

    def action_cancel(self):
        for rec in self:
            if rec.state == "endorsed":
                for endorsement in rec.endorsement_ids.filtered(lambda e: e.state == "confirmed"):
                    if endorsement.move_id and endorsement.move_id.state == "posted":
                        endorsement.move_id._reverse_moves(cancel=True)
                    elif endorsement.move_id and endorsement.move_id.state == "draft":
                        endorsement.move_id.button_cancel()
                    bill = endorsement.vendor_bill_id
                    if bill:
                        if bill.state == "posted":
                            bill._reverse_moves(cancel=True)
                        elif bill.state == "draft":
                            bill.button_cancel()
                    endorsement.state = "cancelled"
                rec.write({"state": "cancelled"})
                rec.message_post(body=_("Cheque cancelled and endorsement entries reversed."))
            else:
                super(ChequeCheque, rec).action_cancel()

    def action_view_endorsements(self):
        self.ensure_one()
        return {
            "name": _("Cheque Endorsements"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.endorsement",
            "view_mode": "list,form",
            "domain": [("cheque_id", "=", self.id)],
            "context": {"default_cheque_id": self.id},
        }

    @api.model
    def _cron_pdc_maturity_reminder(self):
        super()._cron_pdc_maturity_reminder()
        today = fields.Date.context_today(self)
        for company in self.env["res.company"].search([]):
            date_to = today + relativedelta(days=company.cheque_endorsement_reminder_days or 3)
            endorsed_cheques = self.search([
                ("company_id", "=", company.id),
                ("cheque_type", "=", "received"),
                ("state", "=", "endorsed"),
                ("due_date", ">=", today),
                ("due_date", "<=", date_to),
            ])
            for cheque in endorsed_cheques:
                cheque.activity_schedule(
                    "mail.mail_activity_data_todo",
                    summary=_("Endorsed cheque nearing maturity"),
                    note=_("Endorsed cheque %s matures on %s.") % (cheque.display_name, cheque.due_date),
                    user_id=cheque.responsible_id.id or self.env.user.id,
                )

    @api.model
    def _cron_stale_cheque_detection(self):
        super()._cron_stale_cheque_detection()
        stale_cheques = self.search([("state", "=", "endorsed")]).filtered("is_stale")
        for cheque in stale_cheques:
            cheque.message_post(body=_("Endorsed cheque is stale based on company configuration."))
            cheque.activity_schedule(
                "mail.mail_activity_data_todo",
                summary=_("Stale endorsed cheque follow-up"),
                note=_("Review stale endorsed cheque %s.") % cheque.display_name,
                user_id=cheque.responsible_id.id or self.env.user.id,
            )
