# -*- coding: utf-8 -*-
"""Partner extension with cheque stat counters.

Uses ``read_group`` to avoid N+1 when many partners are loaded at once
(e.g. in a list view). All counters and totals are computed (non-stored);
if a partner list view needs to filter/sort on these, they should be
indexed separately.
"""
from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    received_cheque_count = fields.Integer(
        string="# Received Cheques", compute="_compute_cheque_stats",
    )
    issued_cheque_count = fields.Integer(
        string="# Issued Cheques", compute="_compute_cheque_stats",
    )
    bounced_cheque_count = fields.Integer(
        string="# Bounced Cheques", compute="_compute_cheque_stats",
    )
    total_cheque_received = fields.Monetary(
        string="Total Received",
        compute="_compute_cheque_stats",
        currency_field="company_currency_id",
        help="Total amount of received cheques in the partner's company currency.",
    )
    total_cheque_issued = fields.Monetary(
        string="Total Issued",
        compute="_compute_cheque_stats",
        currency_field="company_currency_id",
        help="Total amount of issued cheques in the partner's company currency.",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency",
        comodel_name="res.currency",
        compute="_compute_company_currency_id",
        search="_search_company_currency_id",
        ondelete="restrict",
    )

    def _compute_company_currency_id(self):
        for partner in self:
            company = partner.company_id or self.env.company
            partner.company_currency_id = company.currency_id

    def _search_company_currency_id(self, operator, value):
        return [("company_id.currency_id", operator, value)]

    @api.depends("company_currency_id")
    def _compute_cheque_stats(self):
        """Compute cheque counters + totals for all partners in one shot."""
        if not self:
            return
        partner_ids = self.ids
        domain = [("partner_id", "in", partner_ids)]
        Cheque = self.env["cheque.cheque"]

        # Group by partner + cheque_type to get counts + amount sums
        type_groups = Cheque.read_group(
            domain,
            ["amount_company_currency:sum"],
            ["partner_id", "cheque_type"],
            lazy=False,
        )
        received_count = {pid: 0 for pid in partner_ids}
        issued_count = {pid: 0 for pid in partner_ids}
        received_total = {pid: 0.0 for pid in partner_ids}
        issued_total = {pid: 0.0 for pid in partner_ids}
        for grp in type_groups:
            pid_pair = grp.get("partner_id")
            pid = pid_pair[0] if isinstance(pid_pair, (tuple, list)) else pid_pair
            if not pid or pid not in received_count:
                continue
            ctype = grp.get("cheque_type")
            count = grp.get("__count", 0) or 0
            total = grp.get("amount_company_currency") or 0.0
            if ctype == "received":
                received_count[pid] = count
                received_total[pid] = total
            elif ctype == "issued":
                issued_count[pid] = count
                issued_total[pid] = total

        # Returned cheques counted separately
        return_groups = Cheque.read_group(
            domain + [("state", "=", "returned")],
            [],
            ["partner_id"],
            lazy=False,
        )
        bounced_count = {pid: 0 for pid in partner_ids}
        for grp in return_groups:
            pid_pair = grp.get("partner_id")
            pid = pid_pair[0] if isinstance(pid_pair, (tuple, list)) else pid_pair
            if pid and pid in bounced_count:
                bounced_count[pid] = grp.get("__count", 0) or 0

        for partner in self:
            pid = partner.id
            partner.received_cheque_count = received_count.get(pid, 0)
            partner.issued_cheque_count = issued_count.get(pid, 0)
            partner.bounced_cheque_count = bounced_count.get(pid, 0)
            partner.total_cheque_received = received_total.get(pid, 0.0)
            partner.total_cheque_issued = issued_total.get(pid, 0.0)

    def action_view_received_cheques(self):
        self.ensure_one()
        return self._action_view_cheques("received")

    def action_view_issued_cheques(self):
        self.ensure_one()
        return self._action_view_cheques("issued")

    def _action_view_cheques(self, cheque_type):
        return {
            "name": _("Cheques"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.cheque",
            "view_mode": "list,form,kanban,calendar,pivot,graph",
            "domain": [("partner_id", "=", self.id), ("cheque_type", "=", cheque_type)],
            "context": {"default_partner_id": self.id, "default_cheque_type": cheque_type},
        }
