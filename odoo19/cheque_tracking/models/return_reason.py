from odoo import fields, models


class ChequeReturnReason(models.Model):
    _name = "cheque.return.reason"
    _description = "Cheque Return Reason"
    _order = "code, name"

    name = fields.Char(required=True, translate=True)
    code = fields.Char(required=True, size=10)
    category = fields.Selection(
        [
            ("funds", "Insufficient Funds"),
            ("signature", "Signature / Authorization"),
            ("account", "Account Problem"),
            ("date", "Date Problem"),
            ("bank_error", "Bank Error"),
            ("other", "Other"),
        ],
        required=True,
        default="other",
    )
    description = fields.Text()
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)

    _code_company_uniq = models.Constraint(
        "unique(code, company_id)",
        "Return reason code must be unique per company.",
    )
