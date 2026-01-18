from odoo import fields, models, api


class Tag(models.Model):
    _name = 'tag'
    _description = 'tags'

    name = fields.Char()
