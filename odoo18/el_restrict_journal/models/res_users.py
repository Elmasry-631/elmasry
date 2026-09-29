# -*- coding: utf-8 -*-
# el_restrict_journal — res.users extension (WHITELIST mode)
#
# Adds the "Allowed Journals" Many2many field to res.users.
# This field lists account.journal records that the user IS ALLOWED
# to use for create/write operations on account.move and account.payment.
#
# Whitelist semantics (opposite of blacklist):
#   * Empty list = unrestricted user (default Odoo behavior — sees all journals).
#   * Non-empty list = user can ONLY see/use the journals in this list.
#   * Journals NOT in this list are COMPLETELY HIDDEN from the user
#     (not just read-only — invisible in lists, dropdowns, search).
#
# How the "hide completely" is enforced:
#   1. When admin sets allowed_journal_ids to non-empty, the user is
#      automatically added to group_restrict_journal_user (via write override).
#   2. Record rules on that group HIDE non-allowed journals (perm_read=False).
#   3. Python overrides on account.move/account.payment raise ValidationError
#      if user tries to create/write with a non-allowed journal.
#   4. When admin clears allowed_journal_ids, the user is automatically
#      removed from group_restrict_journal_user → no rules apply → sees all.

from odoo import api, fields, models


class ResUsers(models.Model):
    """Add allowed journals per user (whitelist)."""

    _inherit = "res.users"

    allowed_journal_ids = fields.Many2many(
        comodel_name="account.journal",
        relation="el_restrict_journal_allowed_users_rel",
        column1="user_id",
        column2="journal_id",
        string="Allowed Journals",
        help="Journals this user IS ALLOWED to use. Leave empty for "
        "unrestricted users (default Odoo behavior — sees all journals). "
        "When non-empty, the user can ONLY see and use these journals; "
        "all other journals are completely hidden.",
    )

    # ------------------------------------------------------------------
    # Auto-manage group membership: when allowed_journal_ids is non-empty,
    # add user to group_restrict_journal_user. When empty, remove.
    # This is what makes the record rules "active" only when restriction
    # is configured — avoiding the "empty list hides everything" problem.
    # ------------------------------------------------------------------
    def write(self, vals):
        # Security: only managers can edit allowed_journal_ids
        if "allowed_journal_ids" in vals and not self.env.user.has_group(
            "el_restrict_journal.group_restrict_journal_manager"
        ):
            if not self.env.is_admin():
                from odoo.exceptions import AccessError

                raise AccessError(
                    "You cannot modify the Allowed Journals field. "
                    "Only members of the 'Restricted Journal: Manager' "
                    "group can configure this."
                )

        res = super().write(vals)

        # Auto-manage group membership based on allowed_journal_ids
        if "allowed_journal_ids" in vals:
            group_user = self.env.ref(
                "el_restrict_journal.group_restrict_journal_user", raise_if_not_found=False
            )
            if group_user:
                for user in self:
                    if user.allowed_journal_ids:
                        # Non-empty whitelist → user should be in the group
                        if group_user not in user.group_ids:
                            user.sudo().write(
                                {"group_ids": [(4, group_user.id)]}
                            )
                    else:
                        # Empty whitelist → user should NOT be in the group
                        if group_user in user.group_ids:
                            user.sudo().write(
                                {"group_ids": [(3, group_user.id)]}
                            )
        return res
