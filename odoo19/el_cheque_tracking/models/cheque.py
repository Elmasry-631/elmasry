# -*- coding: utf-8 -*-
"""Core cheque model with full lifecycle for received and issued cheques.

The cheque.cheque model implements two parallel lifecycles:

- **Received cheques** (cheque_type == 'received'):
    draft -> holding -> deposited -> cleared -> returned (-> deposited via
    re-deposit wizard). Each transition posts an accounting entry:
    receipt, deposit, clearance, or return reversal.

- **Issued cheques** (cheque_type == 'issued'):
    draft -> approved -> handed_over -> cashed, with a return path from
    handed_over and a void path from draft / approved / handed_over.

All state transitions post ``account.move`` records tagged with a
``cheque_stage`` field so that the audit trail is queryable.
"""
from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ChequeCheque(models.Model):
    _name = "cheque.cheque"
    _description = "Cheque"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "cheque_date desc, id desc"
    _rec_name = "name"

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------
    name = fields.Char(
        string="Reference",
        default="New",
        readonly=True,
        copy=False,
        required=True,
        tracking=True,
    )
    cheque_type = fields.Selection(
        string="Cheque Type",
        selection=[("received", "Received"), ("issued", "Issued")],
        required=True,
        default="received",
        tracking=True,
    )
    cheque_number = fields.Char(string="Cheque Number", required=True, tracking=True)
    cheque_date = fields.Date(
        string="Cheque Date",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )
    due_date = fields.Date(string="Due Date", tracking=True)
    payee_name = fields.Char(string="Payee Name", tracking=True)

    # ------------------------------------------------------------------
    # Amount
    # ------------------------------------------------------------------
    amount = fields.Monetary(
        string="Amount",
        required=True,
        currency_field="currency_id",
        tracking=True,
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
        tracking=True,
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        related="company_id.currency_id",
        readonly=True,
    )
    amount_company_currency = fields.Monetary(
        string="Amount (Company Currency)",
        compute="_compute_amount_company_currency",
        store=True,
        currency_field="company_currency_id",
    )
    exchange_rate = fields.Float(
        string="Exchange Rate",
        digits=(12, 6),
        help="Manual conversion rate to company currency. Leave 0 to use "
             "the automatic currency rate for the cheque date.",
    )

    # ------------------------------------------------------------------
    # Relations
    # ------------------------------------------------------------------
    partner_id = fields.Many2one(
        string="Partner",
        comodel_name="res.partner",
        required=True,
        tracking=True,
    )
    bank_id = fields.Many2one(
        string="Bank",
        comodel_name="res.bank",
        required=True,
        tracking=True,
    )
    bank_branch_id = fields.Many2one(
        string="Bank Branch",
        comodel_name="res.partner",
    )
    bank_account_id = fields.Many2one(
        string="Cheque Bank Account",
        comodel_name="res.partner.bank",
    )
    deposit_account_id = fields.Many2one(
        string="Deposit / Drawee Bank Journal",
        comodel_name="account.journal",
        domain="[('type', '=', 'bank')]",
        required=True,
        tracking=True,
    )
    invoice_ids = fields.Many2many(
        string="Linked Invoices / Bills",
        comodel_name="account.move",
        relation="cheque_invoice_rel",
        column1="cheque_id",
        column2="move_id",
        domain="[('move_type', 'in', ('out_invoice', 'in_invoice', 'out_refund', 'in_refund'))]",
    )
    deposit_id = fields.Many2one(
        string="Deposit",
        comodel_name="cheque.deposit",
        readonly=True,
        copy=False,
    )
    journal_entry_id = fields.Many2one(
        string="Latest Journal Entry",
        comodel_name="account.move",
        readonly=True,
        copy=False,
    )
    move_ids = fields.One2many(
        string="Journal Entries",
        comodel_name="account.move",
        inverse_name="cheque_id",
        readonly=True,
    )
    move_count = fields.Integer(string="# Entries", compute="_compute_move_count")
    payment_ids = fields.One2many(
        string="Payments",
        comodel_name="account.payment",
        inverse_name="cheque_id",
        readonly=True,
    )
    payment_count = fields.Integer(string="# Payments", compute="_compute_payment_count")
    return_ids = fields.One2many(
        string="Return History",
        comodel_name="cheque.return",
        inverse_name="cheque_id",
        readonly=True,
    )
    return_count = fields.Integer(string="# Returns", compute="_compute_return_info", store=True)
    last_return_date = fields.Date(string="Last Return Date", compute="_compute_return_info", store=True)

    # ------------------------------------------------------------------
    # Workflow + flags
    # ------------------------------------------------------------------
    responsible_id = fields.Many2one(
        string="Responsible",
        comodel_name="res.users",
        default=lambda self: self.env.user,
        tracking=True,
    )
    handover_date = fields.Date(string="Handover Date", tracking=True)
    handover_recipient = fields.Char(string="Handover Recipient", tracking=True)
    expected_clearing_date = fields.Date(string="Expected Clearing Date", tracking=True)
    state_changed_date = fields.Datetime(
        string="State Changed Date",
        default=fields.Datetime.now,
        readonly=True,
        copy=False,
    )
    state = fields.Selection(
        string="Status",
        selection=[
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
        copy=False,
    )
    is_post_dated = fields.Boolean(string="Post-Dated", compute="_compute_date_flags", store=True)
    is_stale = fields.Boolean(string="Stale", compute="_compute_date_flags", store=True)
    days_until_due = fields.Integer(string="Days Until Due", compute="_compute_days")
    days_in_state = fields.Integer(string="Days in State", compute="_compute_days")
    notes = fields.Text(string="Notes")
    company_id = fields.Many2one(
        string="Company",
        comodel_name="res.company",
        default=lambda self: self.env.company,
        required=True,
        index=True,
    )

    # ------------------------------------------------------------------
    # Constraints
    # ------------------------------------------------------------------
    _cheque_number_bank_date_uniq = models.Constraint(
        "unique(cheque_number, bank_id, cheque_date, company_id)",
        "Cheque number, bank, and date must be unique per company.",
    )
    _amount_positive = models.Constraint(
        "check(amount > 0)",
        "Cheque amount must be positive.",
    )
    _due_date_after_cheque_date = models.Constraint(
        "check(due_date IS NULL OR due_date >= cheque_date)",
        "Due date cannot be earlier than cheque date.",
    )

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"].sudo()
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = sequence.next_by_code("cheque.cheque") or "New"
        records = super().create(vals_list)
        for record in records:
            record.message_post(body=_("Cheque created."))
            if record.cheque_type == "issued" and record._is_high_value():
                record._create_high_value_activity()
        return records

    def write(self, vals):
        track_state = "state" in vals
        result = super().write(vals)
        if track_state:
            self.write({"state_changed_date": fields.Datetime.now()})
        return result

    def unlink(self):
        if self.filtered(lambda c: c.payment_ids):
            raise UserError(_("You cannot delete a cheque that is linked to payments."))
        if self.filtered(lambda c: c.invoice_ids):
            raise UserError(_("You cannot delete a cheque that is linked to invoices or bills."))
        if self.filtered(lambda c: c.move_ids.filtered(lambda m: m.line_ids.reconciled)):
            raise UserError(
                _("You cannot delete a cheque whose journal items are reconciled.")
            )
        return super().unlink()

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------
    @api.depends("amount", "currency_id", "company_id", "cheque_date", "exchange_rate")
    def _compute_amount_company_currency(self):
        for rec in self:
            if not rec.amount or not rec.currency_id or not rec.company_id:
                rec.amount_company_currency = 0.0
                continue
            if rec.exchange_rate:
                rec.amount_company_currency = rec.amount * rec.exchange_rate
            else:
                rec.amount_company_currency = rec.currency_id._convert(
                    rec.amount,
                    rec.company_id.currency_id,
                    rec.company_id,
                    rec.cheque_date or fields.Date.context_today(rec),
                )

    @api.depends("cheque_date", "due_date", "state", "company_id", "state_changed_date")
    def _compute_date_flags(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.is_post_dated = bool(rec.due_date and rec.due_date > today)
            stale_months = rec.company_id.cheque_stale_months or 0
            rec.is_stale = False
            if stale_months and rec.cheque_date and rec.state in ("holding", "deposited"):
                stale_cutoff = rec.cheque_date + relativedelta(months=stale_months)
                rec.is_stale = today > stale_cutoff

    @api.depends("due_date", "state_changed_date")
    def _compute_days(self):
        today = fields.Date.context_today(self)
        for rec in self:
            rec.days_until_due = (
                (rec.due_date - today).days if rec.due_date else 0
            )
            if rec.state_changed_date:
                rec.days_in_state = (fields.Datetime.to_date(today) -
                                     fields.Datetime.to_date(rec.state_changed_date)).days
            else:
                rec.days_in_state = 0

    @api.depends("move_ids")
    def _compute_move_count(self):
        for rec in self:
            rec.move_count = len(rec.move_ids)

    @api.depends("payment_ids")
    def _compute_payment_count(self):
        for rec in self:
            rec.payment_count = len(rec.payment_ids)

    @api.depends("return_ids", "return_ids.return_date")
    def _compute_return_info(self):
        for rec in self:
            rec.return_count = len(rec.return_ids)
            if rec.return_ids:
                rec.last_return_date = max(rec.return_ids.mapped("return_date"))
            else:
                rec.last_return_date = False

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _is_high_value(self):
        """Return True if this issued cheque exceeds the company approval threshold."""
        self.ensure_one()
        threshold = self.company_id.cheque_approval_threshold or 0.0
        return bool(threshold) and self.amount_company_currency > threshold

    def _create_high_value_activity(self):
        """Schedule an approval activity for a high-value issued cheque."""
        self.ensure_one()
        self.activity_schedule(
            "mail.mail_activity_data_todo",
            summary=_("High-value cheque approval required"),
            note=_("Review and approve issued cheque %s.") % self.display_name,
            user_id=self.responsible_id.id or self.env.user.id,
        )

    def _to_company_currency(self, amount, date=None):
        """Convert ``amount`` (in cheque currency) to company currency."""
        self.ensure_one()
        if not self.currency_id or self.currency_id == self.company_id.currency_id:
            return amount
        if self.exchange_rate:
            return amount * self.exchange_rate
        return self.currency_id._convert(
            amount,
            self.company_id.currency_id,
            self.company_id,
            date or self.cheque_date or fields.Date.context_today(self),
        )

    def _require_account(self, account_field, label):
        """Return the configured company account for ``account_field`` or raise."""
        self.ensure_one()
        account = self.company_id[account_field]
        if not account:
            raise UserError(
                _("Please configure %s in Cheque Tracking settings.") % label
            )
        return account

    def _require_bank_journal_default_account(self):
        """Return the default debit account of the cheque's bank journal."""
        self.ensure_one()
        if not self.deposit_account_id.default_account_id:
            raise UserError(
                _("Please select a bank journal with a default account.")
            )
        return self.deposit_account_id.default_account_id

    def _require_partner_account(self):
        """Return the partner receivable / payable account based on cheque_type."""
        self.ensure_one()
        if self.cheque_type == "received":
            account = self.partner_id.property_account_receivable_id
            label = _("the partner receivable account")
        else:
            account = self.partner_id.property_account_payable_id
            label = _("the partner payable account")
        if not account:
            raise UserError(
                _("Please configure the partner accounting account (%s).") % label
            )
        return account

    def _post_cheque_move(self, stage, date, lines, ref=None):
        """Create and post an ``account.move`` tagged with cheque_stage.

        :param stage: one of receipt/deposit/clearance/return/issue/cash/void
        :param date:  accounting date
        :param lines: list of dicts with keys: account_id, debit, credit,
                      partner_id (optional), name (optional)
        :param ref:   optional move reference; defaults to cheque name + stage
        :return:      the posted ``account.move`` record
        """
        self.ensure_one()
        if not lines:
            raise UserError(_("No journal lines to post for cheque %s.") % self.name)
        move_vals = {
            "ref": ref or _("%(cheque)s — %(stage)s") % {
                "cheque": self.name, "stage": stage,
            },
            "date": date,
            "journal_id": self.deposit_account_id.id,
            "cheque_id": self.id,
            "cheque_stage": stage,
            "line_ids": [],
        }
        for ln in lines:
            move_vals["line_ids"].append((0, 0, {
                "account_id": ln["account_id"],
                "partner_id": ln.get("partner_id", self.partner_id.id),
                "debit": ln.get("debit", 0.0),
                "credit": ln.get("credit", 0.0),
                "name": ln.get("name", move_vals["ref"]),
            }))
        move = self.env["account.move"].sudo().create(move_vals)
        move.action_post()
        self.journal_entry_id = move.id
        return move

    def _reverse_move(self, move, reason=None):
        """Reverse a posted ``account.move`` and return the reversal move."""
        self.ensure_one()
        if not move or move.state != "posted":
            return self.env["account.move"]
        reversal = move._reverse_moves(
            default_values_list=[{
                "ref": reason or _("Reversal for cheque %s") % self.name,
                "date": fields.Date.context_today(self),
                "cheque_id": self.id,
                "cheque_stage": "return",
            }],
            cancel=False,
        )
        return reversal

    # ------------------------------------------------------------------
    # Received-cheque lifecycle
    # ------------------------------------------------------------------
    def action_receive(self):
        """Draft -> Holding. Posts receipt entry: Dr Cheques Received / Cr Receivable."""
        for rec in self:
            if rec.cheque_type != "received":
                raise UserError(_("Only received cheques can be received."))
            if rec.state != "draft":
                raise UserError(_("Only draft cheques can be received."))
            cheques_received = rec._require_account(
                "cheque_received_account_id", _("Cheques Received Account"),
            )
            receivable = rec._require_partner_account()
            amount = rec._to_company_currency(rec.amount)
            rec._post_cheque_move(
                stage="receipt",
                date=rec.cheque_date,
                lines=[
                    {"account_id": cheques_received.id, "debit": amount},
                    {"account_id": receivable.id, "credit": amount},
                ],
            )
            rec.state = "holding"
            rec.message_post(body=_("Cheque submitted and moved to holding."))

    def action_deposit(self):
        """Holding -> Deposited. Posts deposit entry: Dr Under Collection / Cr Cheques Received."""
        for rec in self:
            if rec.cheque_type != "received":
                raise UserError(_("Only received cheques can be deposited."))
            if rec.state not in ("holding", "returned"):
                raise UserError(
                    _("Only holding or returned cheques can be deposited.")
                )
            if rec.is_post_dated and rec.due_date and \
                    rec.due_date > fields.Date.context_today(rec):
                raise UserError(
                    _("Cannot deposit a post-dated cheque before its due date.")
                )
            if rec.state == "returned":
                max_attempts = rec.company_id.cheque_max_redeposits or 0
                if max_attempts and rec.return_count >= max_attempts:
                    raise UserError(
                        _("Cannot re-deposit cheque. Maximum re-deposit "
                          "attempts (%s) exceeded.") % max_attempts
                    )
            under_collection = rec._require_account(
                "cheque_under_collection_account_id",
                _("Cheques Under Collection Account"),
            )
            cheques_received = rec._require_account(
                "cheque_received_account_id", _("Cheques Received Account"),
            )
            amount = rec._to_company_currency(rec.amount)
            rec._post_cheque_move(
                stage="deposit",
                date=fields.Date.context_today(rec),
                lines=[
                    {"account_id": under_collection.id, "debit": amount},
                    {"account_id": cheques_received.id, "credit": amount},
                ],
            )
            rec.state = "deposited"
            rec.message_post(body=_("Cheque deposited under collection."))

    def action_clear(self):
        """Deposited -> Cleared. Posts clearance entry: Dr Bank / Cr Under Collection."""
        for rec in self:
            if rec.cheque_type != "received":
                raise UserError(_("Only received cheques can be cleared."))
            if rec.state != "deposited":
                raise UserError(_("Only deposited cheques can be cleared."))
            bank = rec._require_bank_journal_default_account()
            under_collection = rec._require_account(
                "cheque_under_collection_account_id",
                _("Cheques Under Collection Account"),
            )
            amount = rec._to_company_currency(rec.amount)
            rec._post_cheque_move(
                stage="clearance",
                date=fields.Date.context_today(rec),
                lines=[
                    {"account_id": bank.id, "debit": amount},
                    {"account_id": under_collection.id, "credit": amount},
                ],
            )
            rec.state = "cleared"
            rec.message_post(body=_("Cheque cleared."))

    # ------------------------------------------------------------------
    # Issued-cheque lifecycle
    # ------------------------------------------------------------------
    def action_approve(self):
        """Draft -> Approved. Posts issue entry: Dr Payable / Cr Cheques Issued."""
        for rec in self:
            if rec.cheque_type != "issued":
                raise UserError(_("Only issued cheques can be approved."))
            if rec.state != "draft":
                raise UserError(_("Only draft issued cheques can be approved."))
            payable = rec._require_partner_account()
            cheques_issued = rec._require_account(
                "cheque_issued_account_id", _("Cheques Issued Account"),
            )
            amount = rec._to_company_currency(rec.amount)
            rec._post_cheque_move(
                stage="issue",
                date=rec.cheque_date,
                lines=[
                    {"account_id": payable.id, "debit": amount},
                    {"account_id": cheques_issued.id, "credit": amount},
                ],
            )
            rec.state = "approved"
            rec.message_post(body=_("Issued cheque approved and accounting entry posted."))

    def action_hand_over(self):
        """Approved -> Handed Over. Records physical delivery only (no entry)."""
        for rec in self:
            if rec.cheque_type != "issued":
                raise UserError(_("Only issued cheques can be handed over."))
            if rec.state != "approved":
                raise UserError(_("Only approved issued cheques can be handed over."))
            rec.write({
                "state": "handed_over",
                "handover_date": fields.Date.context_today(rec),
            })
            rec.message_post(body=_("Cheque handed over."))

    def action_cash(self):
        """Handed Over -> Cashed. Posts cashing entry: Dr Cheques Issued / Cr Bank."""
        for rec in self:
            if rec.cheque_type != "issued":
                raise UserError(_("Only issued cheques can be cashed."))
            if rec.state != "handed_over":
                raise UserError(_("Only handed-over issued cheques can be cashed."))
            cheques_issued = rec._require_account(
                "cheque_issued_account_id", _("Cheques Issued Account"),
            )
            bank = rec._require_bank_journal_default_account()
            amount = rec._to_company_currency(rec.amount)
            rec._post_cheque_move(
                stage="cash",
                date=fields.Date.context_today(rec),
                lines=[
                    {"account_id": cheques_issued.id, "debit": amount},
                    {"account_id": bank.id, "credit": amount},
                ],
            )
            rec.state = "cashed"
            rec.message_post(body=_("Issued cheque was cashed."))

    # ------------------------------------------------------------------
    # Return + void + cancel
    # ------------------------------------------------------------------
    def action_return(self):
        """Open the return wizard for this cheque."""
        self.ensure_one()
        if self.state not in ("deposited", "cleared", "handed_over"):
            raise UserError(
                _("Only deposited, cleared, or handed-over cheques can be returned.")
            )
        return {
            "name": _("Return Cheque"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.return.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_cheque_id": self.id,
                "default_return_date": fields.Date.context_today(self),
            },
        }

    def _apply_return(self, return_date, reason_id, bank_charges=0.0, penalty_amount=0.0):
        """Apply a return: reverse the latest move + post optional charges/penalty."""
        self.ensure_one()
        # Create the return record
        return_record = self.env["cheque.return"].sudo().create({
            "cheque_id": self.id,
            "return_date": return_date,
            "return_reason_id": reason_id,
            "bank_charges": bank_charges,
            "penalty_amount": penalty_amount,
        })

        # Reverse the latest move (issue or receipt / deposit / clearance)
        latest_move = self.move_ids.sorted("date")[-1:] if self.move_ids else self.env["account.move"]
        if latest_move:
            self._reverse_move(latest_move, reason=_("Cheque returned. Reason: %s") %
                               (self.env["cheque.return.reason"].browse(reason_id).name
                                if reason_id else _("Unknown")))

        # Post optional bank charges + penalty entries
        if bank_charges > 0:
            bank_charges_account = self.company_id.cheque_bank_charges_account_id
            if not bank_charges_account:
                raise UserError(
                    _("Please configure the Cheque Bank Charges Account.")
                )
            bank = self._require_bank_journal_default_account()
            self._post_cheque_move(
                stage="return",
                date=return_date,
                lines=[
                    {"account_id": bank_charges_account.id, "debit": bank_charges},
                    {"account_id": bank.id, "credit": bank_charges},
                ],
                ref=_("%(cheque)s — bank charges") % {"cheque": self.name},
            )

        if penalty_amount > 0:
            penalty_account = self.company_id.cheque_penalty_income_account_id
            if not penalty_account:
                raise UserError(
                    _("Please configure the Cheque Penalty Income Account.")
                )
            receivable = self._require_partner_account()
            self._post_cheque_move(
                stage="return",
                date=return_date,
                lines=[
                    {"account_id": receivable.id, "debit": penalty_amount},
                    {"account_id": penalty_account.id, "credit": penalty_amount},
                ],
                ref=_("%(cheque)s — penalty") % {"cheque": self.name},
            )

        self.state = "returned"
        self.message_post(body=_("Cheque returned. Reason: %s") %
                          (return_record.return_reason_id.name or _("Unknown")))
        # Schedule a follow-up activity
        self.activity_schedule(
            "mail.mail_activity_data_todo",
            summary=_("Follow up returned cheque"),
            note=_("Follow up returned cheque with partner."),
            user_id=self.responsible_id.id or self.env.user.id,
        )
        return return_record

    def action_void(self):
        """Void an issued cheque (draft / approved / handed_over)."""
        for rec in self:
            if rec.cheque_type != "issued":
                raise UserError(_("Only issued cheques can be voided."))
            if rec.state not in ("draft", "approved", "handed_over"):
                raise UserError(
                    _("Only draft, approved, or handed-over issued cheques can be voided.")
                )
            # Reverse any posted entries
            if rec.move_ids:
                latest_move = rec.move_ids.sorted("date")[-1:]
                if latest_move:
                    rec._reverse_move(
                        latest_move[0],
                        reason=_("Issued cheque voided."),
                    )
            rec.state = "void"
            rec.message_post(body=_("Cheque voided."))

    def action_cancel(self):
        """Cancel a draft cheque (no entries to reverse)."""
        for rec in self:
            if rec.state != "draft":
                raise UserError(_("Only draft cheques can be cancelled."))
            rec.state = "cancelled"
            rec.message_post(body=_("Cheque cancelled."))

    def action_reset_to_draft(self):
        """Reset a cancelled cheque back to draft."""
        for rec in self:
            if rec.state != "cancelled":
                raise UserError(_("Only cancelled cheques can be reset to draft."))
            rec.state = "draft"
            rec.message_post(body=_("Cheque reset to draft."))

    # ------------------------------------------------------------------
    # Smart-button actions
    # ------------------------------------------------------------------
    def action_view_moves(self):
        self.ensure_one()
        return {
            "name": _("Cheque Journal Entries"),
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", self.move_ids.ids)],
            "context": {"default_cheque_id": self.id},
        }

    def action_view_payments(self):
        self.ensure_one()
        return {
            "name": _("Payments"),
            "type": "ir.actions.act_window",
            "res_model": "account.payment",
            "view_mode": "list,form",
            "domain": [("id", "in", self.payment_ids.ids)],
        }

    # ------------------------------------------------------------------
    # Cron jobs
    # ------------------------------------------------------------------
    @api.model
    def _cron_pdc_maturity_reminder(self):
        """For each company, schedule activities for post-dated received
        cheques that will mature within the company's PDC reminder window.
        """
        today = fields.Date.context_today(self)
        companies = self.env["res.company"].search([])
        for company in companies:
            reminder_days = company.cheque_pdc_reminder_days or 7
            date_to = today + relativedelta(days=reminder_days)
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
                    note=_("Cheque %s matures on %s.") %
                          (cheque.display_name, cheque.due_date),
                    user_id=cheque.responsible_id.id or self.env.user.id,
                )

    @api.model
    def _cron_stale_cheque_detection(self):
        """Flag and post a chatter note on stale cheques based on company config."""
        stale_cheques = self.search([
            ("state", "in", ("holding", "deposited")),
        ]).filtered("is_stale")
        for cheque in stale_cheques:
            cheque.message_post(
                body=_("Cheque is stale based on company configuration.")
            )
            cheque.activity_schedule(
                "mail.mail_activity_data_todo",
                summary=_("Stale cheque follow-up"),
                note=_("Review stale cheque %s.") % cheque.display_name,
                user_id=cheque.responsible_id.id or self.env.user.id,
            )
