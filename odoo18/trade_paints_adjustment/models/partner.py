from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TradeResPartner(models.Model):
    _inherit = "res.partner"

    def write(self, vals):
        res = super(TradeResPartner, self).write(vals)
        if not self.env.user.has_group('trade_paints_adjustment.partners_edit'):
            raise ValidationError("المستخدم الحالى لايمكنه التعديل")
        return res
