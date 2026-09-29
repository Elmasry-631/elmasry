# -*- coding: utf-8 -*-
# el_restrict_journal — account.journal extension
#
# Adds a computed "allowed_user_count" field that powers a future smart
# button on the journal form (showing how many users have this journal
# in their allowed list).

from odoo import api, fields, models


class AccountJournal(models.Model):
    """Add a smart-button count of users who have this journal allowed."""

    _inherit = "account.journal"

    allowed_user_count = fields.Integer(
        string="Allowed Users",
        compute="_compute_allowed_user_count",
        help="Number of users who have this journal in their allowed list.",
    )

    @api.depends_context("id")
    def _compute_allowed_user_count(self):
        """Count users who have this journal in their allowed_journal_ids."""
        if not self.ids:
            for journal in self:
                journal.allowed_user_count = 0
            return
        self.env.cr.execute(
            """
            SELECT journal_id, COUNT(DISTINCT user_id) AS cnt
            FROM el_restrict_journal_allowed_users_rel
            WHERE journal_id = ANY(%s)
            GROUP BY journal_id
            """,
            (list(self.ids),),
        )
        counts = {row[0]: row[1] for row in self.env.cr.fetchall()}
        for journal in self:
            journal.allowed_user_count = counts.get(journal.id, 0)
