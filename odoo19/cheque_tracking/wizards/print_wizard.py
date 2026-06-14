from odoo import fields, models


class ChequePrintWizard(models.TransientModel):
    _name = "cheque.print.wizard"
    _description = "Cheque Print Wizard"

    cheque_ids = fields.Many2many("cheque.cheque", string="Cheques")
    template = fields.Selection(
        [("standard", "Standard Cheque"), ("compact", "Compact Cheque")],
        default="standard",
        required=True,
    )

    def action_print(self):
        self.ensure_one()
        cheques = self.cheque_ids or self.env["cheque.cheque"].browse(self.env.context.get("active_ids", []))
        return self.env.ref("cheque_tracking.action_report_cheque_print").report_action(cheques)

