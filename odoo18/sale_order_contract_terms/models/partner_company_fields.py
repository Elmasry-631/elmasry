# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    x_id_no = fields.Char(string="ID No")

class ResCompany(models.Model):
    _inherit = "res.company"

    x_establishment_registration = fields.Char(string="Establishment Registration")
    x_represented_by = fields.Char(string="Represented by")
    x_representative_id_no = fields.Char(string="Representative ID No")
    x_po_box = fields.Char(string="PO Box")
