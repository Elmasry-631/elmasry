# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import ValidationError

class User(models.Model):
    _inherit = 'res.users'

    limit_discount = fields.Float(string="Limit Discount", required=False)
