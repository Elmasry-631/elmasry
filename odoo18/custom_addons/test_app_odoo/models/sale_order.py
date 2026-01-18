from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Description'


    field_id = fields.Many2one('test.app.odoo', string="Test App Odoo")

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            order.message_post(body="This is Elmasry!")
        return res