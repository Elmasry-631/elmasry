# -*- coding: utf-8 -*-
# el_restrict_journal — account.payment extension (WHITELIST mode)
#
# Same defense-in-depth pattern as account.move:
#   1. Record rule on account.payment filters by journal_id (HIDE non-allowed)
#   2. Python overrides on create/write raise ValidationError
#   3. @api.constrains catches direct ORM writes

from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountPayment(models.Model):
    """Block non-allowed journals from being used on account.payment."""

    _inherit = "account.payment"

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        allowed = self.env.user.allowed_journal_ids
        if allowed:
            for rec in records:
                if rec.journal_id and rec.journal_id not in allowed:
                    raise ValidationError(
                        _(
                            "You are not allowed to create payments in the "
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
                            "You are not allowed to modify payments in the "
                            "journal '%(journal)s'. Your allowed journals are: "
                            "%(allowed)s.",
                            journal=rec.journal_id.display_name,
                            allowed=", ".join(allowed.mapped("display_name")),
                        )
                    )
        return res

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
