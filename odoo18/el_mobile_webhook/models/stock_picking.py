from odoo import models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def write(self, vals):
        previous = {record.id: record.state for record in self} if 'state' in vals else {}
        result = super().write(vals)
        for record in self:
            if record.id in previous:
                self.env['mobile.webhook.event']._queue_status_change(record, 'delivery.status_changed', previous[record.id], record.state)
        return result
