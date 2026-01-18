from odoo import fields, models


class OdooTestTwo(models.Model):
    _name = "test.app.two"

    name = fields.Char()
    phone = fields.Char()
    address = fields.Char()

    test_app_odoo_ids = fields.One2many('test.app.odoo', 'test_app_two_id', string="Test App Odoo Records")



    def test_action(self):
        print(self.env['test.app.odoo'].create({'name': 'New Record', 'test_app_two_id': self.id})

              )
