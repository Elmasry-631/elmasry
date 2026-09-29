# -*- coding: utf-8 -*-
# el_restrict_journal — account.move extension (WHITELIST mode)
#
# Blocks create/write when the journal_id is NOT in the current user's
# allowed list (user.allowed_journal_ids).
#
# Whitelist logic:
#   * Empty allowed_journal_ids = unrestricted user (no check).
#   * Non-empty allowed_journal_ids = user can only use journals in the list.
#
# Enforcement layers (defense in depth):
#   1. UI onchange — clears journal + warning popup if not allowed.
#   2. Record rules — HIDE non-allowed journals from list views and dropdowns.
#   3. Python overrides + @api.constrains — last line of defense.

from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    """Block non-allowed journals from being used on account.move."""

    _inherit = "account.move"

    # ------------------------------------------------------------------
    # CRUD overrides — second layer of defense (after record rules).
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        allowed = self.env.user.allowed_journal_ids
        if allowed:
            for rec in records:
                if rec.journal_id and rec.journal_id not in allowed:
                    raise ValidationError(
                        _(
                            "You are not allowed to create entries in the "
                            "journal '%(journal)s'. Your allowed journals are: "
                            "%(allowed)s.",
                            journal=rec.journal_id.display_name,
                            allowed=", ".join(allowed.mapped("display_name")),
                        )
                    )
        return records

    def write(self, vals):
        res = super().write(vals)
        allowed = self.env.user.allowed_journal_ids
        if allowed and vals.get("journal_id"):
            for rec in self:
                if rec.journal_id and rec.journal_id not in allowed:
                    raise ValidationError(
                        _(
                            "You are not allowed to modify entries in the "
                            "journal '%(journal)s'. Your allowed journals are: "
                            "%(allowed)s.",
                            journal=rec.journal_id.display_name,
                            allowed=", ".join(allowed.mapped("display_name")),
                        )
                    )
        return res

    # ------------------------------------------------------------------
    # Constraints — third layer of defense.
    # ------------------------------------------------------------------
    @api.constrains("journal_id")
    def _check_journal_allowed(self):
        allowed = self.env.user.allowed_journal_ids
        if not allowed:
            return  # Unrestricted user — no check
        for rec in self:
            if rec.journal_id and rec.journal_id not in allowed:
                raise ValidationError(
                    _(
                        "Journal '%(journal)s' is not in your allowed list. "
                        "Please select one of: %(allowed)s.",
                        journal=rec.journal_id.display_name,
                        allowed=", ".join(allowed.mapped("display_name")),
                    )
                )

    # ------------------------------------------------------------------
    # UI: immediate feedback when user picks a non-allowed journal.
    # ------------------------------------------------------------------
    @api.onchange("journal_id")
    def _onchange_journal_id(self):
        allowed = self.env.user.allowed_journal_ids
        if allowed and self.journal_id and self.journal_id not in allowed:
            journal_name = self.journal_id.display_name
            self.journal_id = False
            return {
                "warning": {
                    "title": _("Journal Not Allowed"),
                    "message": _(
                        "The journal '%(journal)s' is not in your allowed "
                        "list. Please select one of: %(allowed)s.",
                        journal=journal_name,
                        allowed=", ".join(allowed.mapped("display_name")),
                    ),
                }
            }
