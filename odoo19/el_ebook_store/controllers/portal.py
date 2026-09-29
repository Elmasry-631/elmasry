import base64
from odoo import http
from odoo.http import request
from odoo import fields
from odoo.exceptions import AccessError, UserError


class EbookPortal(http.Controller):

    @http.route('/my/library', type='http', auth='user', website=True)
    def my_library(self, **kw):
        """Customer's e-book library page — shows all purchased books."""
        partner = request.env.user.partner_id
        libraries = request.env['ebook.library'].search([
            ('partner_id', '=', partner.id),
        ])
        vals = {'libraries': libraries, 'user': request.env.user}
        return request.render('el_ebook_store.portal_my_library', vals)

    @http.route('/my/ebook/<int:library_id>/read', type='http', auth='user', website=True)
    def read_ebook(self, library_id, **kw):
        """Open the online e-book reader.
        Access is through the LIBRARY entry — not through the code.
        The code was already expired at purchase time. The book stays
        in the customer's library permanently."""
        library = request.env['ebook.library'].browse(library_id)
        if not library.exists():
            raise AccessError("E-book not found.")
        if library.partner_id != request.env.user.partner_id:
            raise AccessError("You don't have access to this e-book.")
        if library.state == 'expired':
            raise UserError("This e-book access has expired.")
        # Log the access (for analytics — does NOT touch the code)
        library.sudo().write({
            'last_access': fields.Datetime.now(),
            'access_count': library.access_count + 1,
        })
        # Create access log
        request.env['ebook.access.log'].sudo().create({
            'library_id': library.id,
            'partner_id': library.partner_id.id,
            'product_tmpl_id': library.product_tmpl_id.id,
        })
        # Get the PDF file
        product = library.product_tmpl_id
        if not product.ebook_file:
            raise UserError("E-book file not found.")
        pdf_data = base64.b64decode(product.ebook_file)
        return request.make_response(pdf_data, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', 'inline'),
            ('Content-Length', len(pdf_data)),
        ])

    @http.route('/my/ebook/<int:library_id>/download', type='http', auth='user', website=True)
    def download_ebook(self, library_id, **kw):
        """Download the e-book file.
        Access is through the LIBRARY entry — permanent access."""
        library = request.env['ebook.library'].browse(library_id)
        if not library.exists():
            raise AccessError("E-book not found.")
        if library.partner_id != request.env.user.partner_id:
            raise AccessError("You don't have access to this e-book.")
        if library.state == 'expired':
            raise UserError("This e-book access has expired.")
        product = library.product_tmpl_id
        if not product.ebook_file:
            raise UserError("E-book file not found.")
        # Log the access
        library.sudo().write({
            'last_access': fields.Datetime.now(),
            'access_count': library.access_count + 1,
        })
        request.env['ebook.access.log'].sudo().create({
            'library_id': library.id,
            'partner_id': library.partner_id.id,
            'product_tmpl_id': library.product_tmpl_id.id,
        })
        pdf_data = base64.b64decode(product.ebook_file)
        filename = product.ebook_filename or f"{product.name}.pdf"
        return request.make_response(pdf_data, headers=[
            ('Content-Type', 'application/pdf'),
            ('Content-Disposition', f'attachment; filename="{filename}"'),
            ('Content-Length', len(pdf_data)),
        ])
