from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    payment_gateway_id = fields.Many2one(
        'sale.payment.gateway',
        string="Payment Gateway"
    )
    carrier_id = fields.Many2one(
        'delivery.carrier',
        string="Delivery Method"
    )

