from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    payment_gateway_id = fields.Many2one(
        'sale.payment.gateway',
        string="Payment Gateway"
    )
    def write(self, vals):
        res = super().write(vals)

        if 'carrier_id' in vals and not self.env.context.get('skip_sync_from_sale'):
            for picking in self:
                if picking.state not in ['done', 'cancel']:
                    sale = self.env['sale.order'].search(
                        [('name', '=', picking.origin)],
                        limit=1
                    )
                    if sale:
                        sale.with_context(skip_sync_from_picking=True).write({
                            'carrier_id': vals['carrier_id']
                        })

        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    payment_gateway_id = fields.Many2one(
        'sale.payment.gateway',
        string="Payment Gateway"
    )

    def _get_new_picking_values(self):
        """Inherit method for pass value from sale order to delivery order."""
        res = super(StockMove, self)._get_new_picking_values()
        res["payment_gateway_id"] = self.sale_line_id.order_id.payment_gateway_id.id
        return res
