from odoo import models


class AccountMove(models.Model):
    _inherit = 'account.move'

    def write(self, vals):
        previous = {record.id: record.state for record in self} if 'state' in vals else {}
        result = super().write(vals)
        for record in self.filtered(lambda move: move.move_type in ('out_invoice', 'out_refund')):
            if record.id in previous:
                self.env['mobile.webhook.event']._queue_status_change(record, 'invoice.status_changed', previous[record.id], record.state)
        return result
