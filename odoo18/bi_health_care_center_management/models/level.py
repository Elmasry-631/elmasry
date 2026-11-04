# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Level(models.Model):
    _name = 'level.level'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='description')
