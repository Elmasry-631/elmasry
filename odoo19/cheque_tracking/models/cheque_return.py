from odoo import api, fields, models


class ChequeReturn(models.Model):
    _name = "cheque.return"
    _description = "Cheque Return"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "return_date desc, id desc"

    name = fields.Char(default="New", readonly=True, copy=False, required=True)
    cheque_id = fields.Many2one("cheque.cheque", required=True, ondelete="cascade", index=True)
    return_date = fields.Date(required=True, default=fields.Date.context_today, tracking=True)
    return_reason_id = fields.Many2one("cheque.return.reason", required=True, tracking=True)
    bank_charges = fields.Monetary(default=0.0, currency_field="currency_id", tracking=True)
    penalty_amount = fields.Monetary(default=0.0, currency_field="currency_id", tracking=True)
    notes = fields.Text()
    currency_id = fields.Many2one(related="cheque_id.currency_id", store=True, readonly=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    move_ids = fields.One2many("account.move", "cheque_return_id", string="Journal Entries", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        sequence = self.env["ir.sequence"].sudo()
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = sequence.next_by_code("cheque.return") or "New"
        return super().create(vals_list)
