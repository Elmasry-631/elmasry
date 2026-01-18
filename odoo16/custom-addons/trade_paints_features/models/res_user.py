# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare
from odoo import exceptions, _
from odoo.exceptions import ValidationError
from lxml import etree

from odoo import api, fields, models, _



class User(models.Model):
    _inherit = 'res.users'

    limit_discount = fields.Float(string="Limit Discount", required=False)





