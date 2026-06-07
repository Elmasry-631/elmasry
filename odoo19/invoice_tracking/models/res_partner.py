
from odoo import models, fields, api

class PartnerCode(models.Model):
    _name = 'partner.code'
    _description = 'Partner Code'
    # res_partner_id = fields.Many2one('res.partner')
    name = fields.Char('Code')

    _code_uniq = models.Constraint('unique(name)', "Tag code already exists!")


class ResPartner(models.Model):
    _inherit = 'res.partner'

    code_id = fields.Many2one('partner.code')
