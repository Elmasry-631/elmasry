from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ChequeCheque(models.Model):
    _name = "cheque.cheque"
    _description = "Cheque"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "cheque_date desc, id desc"

    name = fields.Char(default="New", readonly=True, copy=False, required=True, tracking=True)
    cheque_type = fields.Selection(
        [("received", "Received"), ("issued", "Issued")],
        required=True,
        default="received",
        tracking=True,
    )
    cheque_number = fields.Char(required=True, tracking=True)
    cheque_date = fields.Date(required=True, default=fields.Date.context_today, tracking=True)
    due_date = fields.Date(tracking=True)
    amount = fields.Monetary(required=True, currency_field="currency_id", tracking=True)
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
        tracking=True,
    )
    company_currency_id = fields.Many2one(related="company_id.currency_id", string="Company Currency", readonly=True)
    amount_company_currency = fields.Monetary(
        compute="_compute_amount_company_currency",
        store=True,
        currency_field="company_currency_id",
    )
    exchange_rate = fields.Float(digits=(12, 6), help="Manual conversion rate to company currency.")
    partner_id = fields.Many2one("res.partner", required=True, tracking=True)
    payee_name = fields.Char(tracking=True)
    bank_id = fields.Many2one("res.bank", string="Bank", required=True, tracking=True)
    bank_branch_id = fields.Many2one("res.partner", string="Bank Branch")
    bank_account_id = fields.Many2one("res.partner.bank", string="Cheque Bank Account")
    deposit_account_id = fields.Many2one(
        "account.journal",
        string="Deposit / Drawee Bank Journal",
        domain=[("type", "=", "bank")],
        required=True,
        tracking=True,
    )
    invoice_ids = fields.Many2many(
        "account.move",
        "cheque_invoice_rel",
        "cheque_id",
        "move_id",
        string="Linked Invoices / Bills",
        domain=[("move_type", "in", ("out_invoice", "in_invoice", "out_refund", "in_refund"))],
    )
    deposit_id = fields.Many2one("cheque.deposit", readonly=True, copy=False)
    journal_entry_id = fields.Many2one("account.move", string="Latest Journal Entry", readonly=True, copy=False)
    move_ids = fields.One2many("account.move", "cheque_id", string="Journal Entries", readonly=True)
    move_count = fields.Integer(compute="_compute_move_count")
    return_ids = fields.One2many("cheque.return", "cheque_id", string="Return History", readonly=True)
    return_count = fields.Integer(compute="_compute_return_info", store=True)
    last_return_date = fields.Date(compute="_compute_return_info", store=True)
    responsible_id = fields.Many2one("res.users", default=lambda self: self.env.user, tracking=True)
    handover_date = fields.Date(tracking=True)
    handover_recipient = fields.Char(tracking=True)
    expected_clearing_date = fields.Date(tracking=True)
    state_changed_date = fields.Datetime(default=fields.Datetime.now, readonly=True, copy=False)
    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("holding", "Holding"),
            ("deposited", "Deposited"),
            ("cleared", "Cleared"),
            ("approved", "Approved"),
            ("handed_over", "Handed Over"),
            ("cashed", "Cashed"),
            ("returned", "Returned"),
            ("cancelled", "Cancelled"),
            ("void", "Void"),
        ],
        required=True,
        default="draft",
        tracking=True,
        index=True,
    )
    is_post_dated = fields.Boolean(compute="_compute_date_flags", store=True)
    is_stale = fields.Boolean(compute="_compute_date_flags", store=True)
    days_until_due = fields.Integer(compute="_compute_days")
    days_in_state = fields.Integer(compute="_compute_days")
    notes = fields.Text()
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True, index=True)

    _cheque_number_bank_date_uniq = models.Constraint(
        "unique(cheque_number, bank_id, cheque_date, company_id)",
        "Cheque number, bank, and date must be unique per company.",
    )
    _amount_positive = models.Constraint("check(amount > 0)", "Cheque amount must be positive.")

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"].sudo()
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = sequence.next_by_code("cheque.cheque") or "New"
        records = super().create(vals_list)
        for record in records:
            record.message_post(body=_("Cheque created."))
            if record.cheque_type == "issued":
                record._create_high_value_activity()
        return records

    def write(self, vals):
        track_state = "state" in vals
        result = super().write(vals)
        if track_state:
            self.write({"state_changed_date": fields.Datetime.now()})
        return result

    @api.depends("amount", "currency_id", "company_id", "cheque_date", "exchange_rate")
    def _compute_amount_company_currency(self):
        for rec in self:
            if not rec.amount or not rec.currency_id or not rec.company_id:
                rec.amount_company_currency = 0.0
            elif rec.exchange_rate:
                rec.amount_company_currency = rec.amount * rec.exchange_rate
            else:
                rec.amount_company_currency = rec.currency_id._convert(
                    rec.amount,
                    rec.company_id.currency_id,
                    rec.company_id,
                    rec.cheque_date or fields.Date.context_today(rec),
                )

    @api.depends("due_date", "cheque_date", "company_id.cheque_stale_months")
    def _compute_date_flags(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_post_dated = bool(rec.due_date and rec.cheque_date and rec.due_date > rec.cheque_date)
            stale_months = rec.company_id.cheque_stale_months or 6
            rec.is_stale = bool(
                rec.cheque_date
                and rec.state in ("holding", "deposited")
                and rec.cheque_date < today - relativedelta(months=stale_months)
            )

    @api.depends("move_ids")
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(rec.move_ids)

    @api.depends("due_date", "state_changed_date")
    def _compute_days(self):
        today = fields.Date.context_today(self)
        now = fields.Datetime.now()
        for rec in self:
            rec.days_until_due = (rec.due_date - today).days if rec.due_date else 0
            rec.days_in_state = (now - rec.state_changed_date).days if rec.state_changed_date else 0

    @api.depends("return_ids.return_date")
    def _compute_return_info(self):
        for rec in self:
            rec.return_count = len(rec.return_ids)
            rec.last_return_date = rec.return_ids[:1].return_date if rec.return_ids else False

    @api.constrains("due_date", "cheque_date")
    def _check_dates(self):
        for rec in self:
            if rec.due_date and rec.cheque_date and rec.due_date < rec.cheque_date:
                raise ValidationError(_("Due date cannot be earlier than cheque date."))

    def _check_state(self, allowed):
        for rec in self:
            if rec.state not in allowed:
                raise UserError(_("Invalid state transition for cheque %s.") % rec.display_name)

    def _company_account(self, field_name, label):
        self.ensure_one()
        account = self.company_id[field_name]
        if not account:
            raise UserError(_("Please configure %s in Cheque Tracking settings.") % label)
        return account

    def _bank_account(self):
        self.ensure_one()
        if not self.deposit_account_id or not self.deposit_account_id.default_account_id:
            raise UserError(_("Please select a bank journal with a default account."))
        return self.deposit_account_id.default_account_id

    def _partner_account(self, account_type):
        self.ensure_one()
        account = (
            self.partner_id.property_account_receivable_id
            if account_type == "receivable"
            else self.partner_id.property_account_payable_id
        )
        if not account:
            raise UserError(_("Please configure the partner accounting account."))
        return account

    def _to_company_currency(self, amount, date=None):
        self.ensure_one()
        if self.exchange_rate and self.currency_id != self.company_id.currency_id:
            return amount * self.exchange_rate
        return self.currency_id._convert(
            amount,
            self.company_id.currency_id,
            self.company_id,
            date or self.cheque_date or fields.Date.context_today(self),
        )

    def _create_move(
        self,
        stage,
        label,
        debit_account,
        credit_account,
        date=None,
        amount=None,
        extra_vals=None,
    ):
        self.ensure_one()
        journal = self.deposit_account_id
        if not journal:
            raise UserError(_("Please select the cheque bank journal."))
        move_amount = self._to_company_currency(amount if amount is not None else self.amount, date=date)
        if move_amount <= 0:
            return self.env["account.move"]
        vals = {
            "move_type": "entry",
            "date": date or fields.Date.context_today(self),
            "journal_id": journal.id,
            "ref": "%s - %s" % (self.name, label),
            "cheque_id": self.id,
            "cheque_stage": stage,
            "line_ids": [
                (0, 0, {
                    "name": label,
                    "partner_id": self.partner_id.id,
                    "account_id": debit_account.id,
                    "debit": move_amount,
                    "credit": 0.0,
                }),
                (0, 0, {
                    "name": label,
                    "partner_id": self.partner_id.id,
                    "account_id": credit_account.id,
                    "debit": 0.0,
                    "credit": move_amount,
                }),
            ],
        }
        if extra_vals:
            vals.update(extra_vals)
        move = self.env["account.move"].create(vals)
        move.action_post()
        self.journal_entry_id = move
        return move

    def action_submit(self):
        self._check_state(["draft"])
        for rec in self:
            if rec.cheque_type == "received":
                rec._create_move(
                    "receive",
                    _("Receive Cheque"),
                    rec._company_account("cheque_received_account_id", _("Cheques Received Account")),
                    rec._partner_account("receivable"),
                    date=rec.cheque_date,
                )
                rec.state = "holding"
                rec.message_post(body=_("Cheque submitted and moved to holding."))
            else:
                rec.action_approve()

    def action_approve(self):
        self._check_state(["draft"])
        for rec in self:
            if rec.cheque_type != "issued":
                raise UserError(_("Only issued cheques can be approved."))
            rec._create_move(
                "issue",
                _("Issue Cheque"),
                rec._partner_account("payable"),
                rec._company_account("cheque_issued_account_id", _("Cheques Issued Account")),
                date=rec.cheque_date,
            )
            rec.state = "approved"
            rec.message_post(body=_("Issued cheque approved and accounting entry posted."))

    def action_deposit(self):
        self._check_state(["holding", "returned"])
        for rec in self:
            if rec.cheque_type != "received":
                raise UserError(_("Only received cheques can be deposited."))
            if rec.due_date and rec.due_date > fields.Date.context_today(rec):
                raise UserError(_("Cannot deposit a post-dated cheque before its due date."))
            if rec.state == 'returned' and rec.return_count >= rec.company_id.cheque_max_redeposit_attempts:
                raise UserError(_("Cannot re-deposit cheque. Maximum re-deposit attempts (%s) exceeded.") % rec.company_id.cheque_max_redeposit_attempts)
            rec._create_move(
                "deposit",
                _("Deposit Cheque"),
                rec._company_account("cheque_under_collection_account_id", _("Cheques Under Collection Account")),
                rec._company_account("cheque_received_account_id", _("Cheques Received Account")),
            )
            rec.state = "deposited"
            rec.message_post(body=_("Cheque deposited under collection."))

    def action_clear(self):
        self._check_state(["deposited"])
        for rec in self:
            rec._create_move(
                "clear",
                _("Clear Cheque"),
                rec._bank_account(),
                rec._company_account("cheque_under_collection_account_id", _("Cheques Under Collection Account")),
            )
            rec.state = "cleared"
            rec.message_post(body=_("Cheque cleared."))

    def action_mark_cashed(self):
        self._check_state(["handed_over"])
        for rec in self:
            rec._create_move(
                "cash",
                _("Cheque Cashed"),
                rec._company_account("cheque_issued_account_id", _("Cheques Issued Account")),
                rec._bank_account(),
            )
            rec.state = "cashed"
            rec.message_post(body=_("Issued cheque was cashed."))

    def action_hand_over(self):
        self._check_state(["approved"])
        self.write({"state": "handed_over", "handover_date": fields.Date.context_today(self)})
        self.message_post(body=_("Cheque handed over."))

    def action_void(self):
        self._check_state(["draft", "approved", "handed_over"])
        self.write({"state": "void"})
        self.message_post(body=_("Cheque voided."))

    def action_cancel(self):
        self._check_state(["draft", "holding", "returned"])
        self.write({"state": "cancelled"})
        self.message_post(body=_("Cheque cancelled."))

    def action_open_return_wizard(self):
        self.ensure_one()
        if self.state not in ("deposited", "cleared", "handed_over"):
            raise UserError(_("Only deposited, cleared, or handed-over cheques can be returned."))
        return {
            "name": _("Return Cheque"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.return.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {"default_cheque_id": self.id},
        }

    def action_print_cheque(self):
        self.ensure_one()
        return self.env.ref("cheque_tracking.action_report_cheque_print").report_action(self)

    def action_view_entries(self):
        self.ensure_one()
        return {
            "name": _("Cheque Journal Entries"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("cheque_id", "=", self.id)],
            "context": {"default_cheque_id": self.id},
        }

    def _create_high_value_activity(self):
        threshold = self.company_id.cheque_approval_threshold
        if threshold and self.amount_company_currency > threshold:
            self.activity_schedule(
                "mail.mail_activity_data_todo",
                summary=_("High-value cheque approval required"),
                note=_("Review and approve issued cheque %s.") % self.display_name,
                user_id=self.responsible_id.id or self.env.user.id,
            )

    @api.model
    def _cron_pdc_maturity_reminder(self):
        today = fields.Date.context_today(self)
        companies = self.env["res.company"].search([])
        for company in companies:
            date_to = today + relativedelta(days=company.cheque_pdc_reminder_days or 7)
            cheques = self.search([
                ("company_id", "=", company.id),
                ("cheque_type", "=", "received"),
                ("state", "=", "holding"),
                ("due_date", ">=", today),
                ("due_date", "<=", date_to),
            ])
            for cheque in cheques:
                cheque.activity_schedule(
                    "mail.mail_activity_data_todo",
                    summary=_("Post-dated cheque maturing"),
                    note=_("Cheque %s matures on %s.") % (cheque.display_name, cheque.due_date),
                    user_id=cheque.responsible_id.id or self.env.user.id,
                )
    @api.model
    def _cron_stale_cheque_detection(self):
        stale_cheques = self.search([("state", "in", ("holding", "deposited"))]).filtered("is_stale")
        for cheque in stale_cheques:
            cheque.message_post(body=_("Cheque is stale based on company configuration."))
            cheque.activity_schedule(
                "mail.mail_activity_data_todo",
                summary=_("Stale cheque follow-up"),
                note=_("Review stale cheque %s.") % cheque.display_name,
                user_id=cheque.responsible_id.id or self.env.user.id,
            )
