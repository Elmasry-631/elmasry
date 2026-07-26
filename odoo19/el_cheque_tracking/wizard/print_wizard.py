# -*- coding: utf-8 -*-
"""Print wizard: choose report type for selected cheques."""
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class ChequePrintWizard(models.TransientModel):
    _name = "cheque.print.wizard"
    _description = "Cheque Print Wizard"

    report_type = fields.Selection(
        string="Report Type",
        selection=[
            ("cheque_print", "Cheque Print"),
            ("deposit_slip", "Deposit Slip"),
            ("cheque_register", "Cheque Register"),
        ],
        required=True,
        default="cheque_print",
    )
    cheque_ids = fields.Many2many(
        string="Cheques",
        comodel_name="cheque.cheque",
        relation="cheque_print_wiz_cheque_rel",
        column1="wizard_id",
        column2="cheque_id",
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_ids = self.env.context.get("active_ids", [])
        if active_ids and self.env.context.get("active_model") == "cheque.cheque":
            cheques = self.env["cheque.cheque"].browse(active_ids)
            res["cheque_ids"] = [(6, 0, cheques.ids)]
        return res

    def action_print(self):
        self.ensure_one()
        if not self.cheque_ids:
            raise UserError(_("Please select at least one cheque."))
        report_xml_id = {
            "cheque_print": "el_cheque_tracking.action_report_cheque_print",
            "deposit_slip": "el_cheque_tracking.action_report_deposit_slip",
            "cheque_register": "el_cheque_tracking.action_report_cheque_register",
        }[self.report_type]
        report = self.env.ref(report_xml_id)
        return report.report_action(self.cheque_ids)
