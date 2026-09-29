from odoo import models


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    def write(self, vals):
        previous = {record.id: record.state for record in self} if 'state' in vals else {}
        result = super().write(vals)
        for record in self:
            if record.id in previous:
                self.env['mobile.webhook.event']._queue_status_change(record, 'payment.status_changed', previous[record.id], record.state)
        return result
