from odoo import fields, models


class EbookLibrary(models.Model):
    _name = 'ebook.library'
    _description = 'Customer E-Book Library'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'purchase_date desc'

    partner_id = fields.Many2one('res.partner', string='Customer', required=True, index=True)
    product_tmpl_id = fields.Many2one('product.template', string='E-Book', required=True)
    code_id = fields.Many2one('ebook.code', string='Access Code', tracking=True)
    order_id = fields.Many2one('sale.order', string='Sale Order')
    state = fields.Selection([
        ('purchased', 'Purchased'),
        ('accessible', 'Accessible'),
        ('expired', 'Expired'),
    ], string='Status', default='accessible', tracking=True)
    purchase_date = fields.Datetime(string='Purchase Date', default=fields.Datetime.now)
    last_access = fields.Datetime(string='Last Access')
    access_count = fields.Integer(string='Access Count', default=0)

    # NOTE: No action_mark_accessed() here — the portal controller
    # directly updates last_access and access_count without touching
    # the code. The code is expired at purchase time and never used again.
