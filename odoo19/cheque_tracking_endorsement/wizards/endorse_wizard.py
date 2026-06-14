from odoo import _, fields, models
from odoo.exceptions import UserError


class ChequeEndorseWizard(models.TransientModel):
    _name = "cheque.endorse.wizard"
    _description = "Endorse Cheque Wizard"

    cheque_id = fields.Many2one("cheque.cheque", required=True, readonly=True)
    current_beneficiary_id = fields.Many2one("res.partner", readonly=True)
    endorsee_partner_id = fields.Many2one("res.partner", required=True)
    endorsement_date = fields.Date(required=True, default=fields.Date.context_today)
    reason = fields.Text()
    create_vendor_bill = fields.Boolean(default=True)

    def action_confirm(self):
        self.ensure_one()
        if not self.cheque_id:
            raise UserError(_("Please select a cheque to endorse."))
        self.cheque_id.action_endorse(
            endorsee_partner=self.endorsee_partner_id,
            endorsement_date=self.endorsement_date,
            reason=self.reason,
            create_vendor_bill=self.create_vendor_bill,
        )
        return {"type": "ir.actions.act_window_close"}
