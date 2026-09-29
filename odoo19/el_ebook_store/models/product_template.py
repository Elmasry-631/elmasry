from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_ebook = fields.Boolean(string='Is E-Book', default=False)
    ebook_file = fields.Binary(string='E-Book File (PDF)', help='Upload the PDF file for this e-book')
    ebook_filename = fields.Char(string='File Name')
    ebook_sample = fields.Binary(string='Free Sample (PDF)', help='First few pages as a free preview')
    ebook_sample_filename = fields.Char(string='Sample File Name')
    ebook_access_type = fields.Selection([
        ('online', 'Online Reader Only'),
        ('download', 'Download Only'),
        ('both', 'Both Online & Download'),
    ], string='Access Type', default='online', help='How customers can access this e-book after purchase')
    ebook_author = fields.Char(string='Author')
    ebook_pages = fields.Integer(string='Pages')
    ebook_isbn = fields.Char(string='ISBN')
    ebook_total_codes = fields.Integer(string='Total Codes', compute='_compute_code_stats')
    ebook_codes_used = fields.Integer(string='Codes Used', compute='_compute_code_stats')
    ebook_codes_available = fields.Integer(string='Codes Available', compute='_compute_code_stats')

    def _compute_code_stats(self):
        for book in self:
            codes = self.env['ebook.code'].search([('product_tmpl_id', '=', book.id)])
            book.ebook_total_codes = len(codes)
            book.ebook_codes_used = len(codes.filtered(lambda c: c.state in ('used', 'assigned')))
            book.ebook_codes_available = len(codes.filtered(lambda c: c.state == 'available'))
