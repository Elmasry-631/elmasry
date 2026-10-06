from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_gateway_id = fields.Many2one(
        'sale.payment.gateway',
        string="Payment Gateway"
    )
    def write(self, vals):
        res = super().write(vals)

        if 'carrier_id' in vals and not self.env.context.get('skip_sync_from_picking'):
            for order in self:
                pickings = order.picking_ids.filtered(
                    lambda p: p.state not in ['done', 'cancel']
                )
                pickings.with_context(skip_sync_from_sale=True).write({
                    'carrier_id': vals['carrier_id']
                })

        return res

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        vals.update({
            'payment_gateway_id': self.payment_gateway_id.id,
            'carrier_id': self.carrier_id.id
        })
        return vals
