import datetime
from email.policy import default

from odoo import fields, models, api


class TestHistory(models.Model):
    _name = 'test.history'
    _description = 'Description'

    user_id = fields.Many2one('res.users')
    property_id = fields.Many2one('test.app.odoo')
    old_state =fields.Char()
    new_state = fields.Char()