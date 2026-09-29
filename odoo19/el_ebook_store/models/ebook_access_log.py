from odoo import fields, models


class EbookAccessLog(models.Model):
    _name = 'ebook.access.log'
    _description = 'E-Book Access Log'
    _order = 'access_date desc'

    library_id = fields.Many2one('ebook.library', string='Library Entry', ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Customer', index=True)
    product_tmpl_id = fields.Many2one('product.template', string='E-Book', index=True)
    access_date = fields.Datetime(string='Access Date', default=fields.Datetime.now)
    ip_address = fields.Char(string='IP Address')
    user_agent = fields.Char(string='User Agent')
