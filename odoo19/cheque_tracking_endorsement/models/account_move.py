from odoo import _, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    cheque_endorsement_id = fields.Many2one("cheque.endorsement", string="Cheque Endorsement", copy=False, index=True)
    cheque_stage = fields.Selection(selection_add=[("endorse", "Endorse Cheque")])

    def action_view_cheque(self):
        self.ensure_one()
        cheque = self.cheque_id or self.cheque_endorsement_id.cheque_id
        if not cheque:
            return False
        return {
            "name": _("Cheque"),
            "type": "ir.actions.act_window",
            "res_model": "cheque.cheque",
            "view_mode": "form",
            "res_id": cheque.id,
        }
