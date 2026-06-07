from odoo import fields, models, api


class Well(models.Model):
    _name = 'oil.well'
    _description = 'Oil Well'

    name = fields.Char()
