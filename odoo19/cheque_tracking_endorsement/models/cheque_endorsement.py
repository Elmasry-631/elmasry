from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ChequeEndorsement(models.Model):
    _name = "cheque.endorsement"
    _description = "Cheque Endorsement"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "endorsement_date desc, sequence desc, id desc"

    name = fields.Char(default="New", readonly=True, copy=False, required=True, tracking=True)
    cheque_id = fields.Many2one("cheque.cheque", required=True, ondelete="cascade", index=True, tracking=True)
    company_id = fields.Many2one(related="cheque_id.company_id", store=True, readonly=True, index=True)
    currency_id = fields.Many2one(related="cheque_id.currency_id", store=True, readonly=True)
    amount = fields.Monetary(related="cheque_id.amount", store=True, readonly=True)
    endorser_id = fields.Many2one("res.partner", tracking=True)
    endorsee_id = fields.Many2one("res.partner", tracking=True)
    endorsement_date = fields.Date(required=True, default=fields.Date.context_today, tracking=True)
    reason = fields.Text(tracking=True)
    sequence = fields.Integer(readonly=True, index=True)
    move_id = fields.Many2one("account.move", string="Journal Entry", readonly=True, copy=False)
    vendor_bill_id = fields.Many2one("account.move", string="Vendor Bill", readonly=True, copy=False)
    state = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="draft",
        required=True,
        tracking=True,
    )
    user_id = fields.Many2one("res.users", default=lambda self: self.env.user, readonly=True, tracking=True)

    _sequence_per_check = models.Constraint(
        "unique(cheque_id, sequence)",
        "Endorsement sequence must be unique per cheque.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("cheque_id") and not vals.get("sequence"):
                cheque = self.env["cheque.cheque"].browse(vals["cheque_id"])
                vals["sequence"] = len(cheque.endorsement_ids) + 1
        records = super().create(vals_list)
        for record in records:
            if record.name == "New":
                record.name = "%s / %s" % (record.cheque_id.display_name, record.sequence)
            record.message_post(body=_("Cheque endorsement recorded."))
        return records

    @api.constrains("endorser_id", "endorsee_id", "endorsement_date")
    def _check_endorsement_data(self):
        today = fields.Date.context_today(self)
        for rec in self:
            if rec.state == "confirmed" and (not rec.endorser_id or not rec.endorsee_id):
                raise ValidationError(_("Confirmed endorsements must have both endorser and endorsee."))
            if rec.endorser_id and rec.endorsee_id and rec.endorser_id == rec.endorsee_id:
                raise ValidationError(_("Endorser and endorsee must be different."))
            if rec.endorsement_date and rec.endorsement_date > today:
                raise ValidationError(_("Endorsement date cannot be in the future."))

    def init(self):
        self.env.cr.execute("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'cheque_endorsement' AND column_name = 'endorser_partner_id'
                ) THEN
                    EXECUTE '
                        UPDATE cheque_endorsement
                           SET endorser_id = COALESCE(endorser_id, endorser_partner_id),
                               endorsee_id = COALESCE(endorsee_id, endorsee_partner_id),
                               user_id = COALESCE(user_id, endorsed_by)
                    ';
                END IF;
            END $$;
        """)
