from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    received_cheque_count = fields.Integer(compute="_compute_cheque_stats")
    issued_cheque_count = fields.Integer(compute="_compute_cheque_stats")
    bounced_cheque_count = fields.Integer(compute="_compute_cheque_stats")
    total_cheque_received = fields.Float(compute="_compute_cheque_stats")
    total_cheque_issued = fields.Float(compute="_compute_cheque_stats")

    def _compute_cheque_stats(self):
        Cheque = self.env["cheque.cheque"]
        for partner in self:
            cheques = Cheque.search([("partner_id", "=", partner.id)])
            received = cheques.filtered(lambda chq: chq.cheque_type == "received")
            issued = cheques.filtered(lambda chq: chq.cheque_type == "issued")
            partner.received_cheque_count = len(received)
            partner.issued_cheque_count = len(issued)
            partner.bounced_cheque_count = len(cheques.filtered(lambda chq: chq.state == "returned"))
            partner.total_cheque_received = sum(received.mapped("amount_company_currency"))
            partner.total_cheque_issued = sum(issued.mapped("amount_company_currency"))

    def action_view_received_cheques(self):
        self.ensure_one()
        return self._action_view_cheques("received")

    def action_view_issued_cheques(self):
        self.ensure_one()
        return self._action_view_cheques("issued")

    def _action_view_cheques(self, cheque_type):
        return {
            "name": "Cheques",
            "type": "ir.actions.act_window",
            "res_model": "cheque.cheque",
            "view_mode": "list,form,kanban,calendar,pivot,graph",
            "domain": [("partner_id", "=", self.id), ("cheque_type", "=", cheque_type)],
            "context": {"default_partner_id": self.id, "default_cheque_type": cheque_type},
        }
