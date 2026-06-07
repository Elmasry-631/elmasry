from odoo import http
from odoo.http import request
import base64

class PublicImage(http.Controller):

    @http.route('/public/partner/image/<int:partner_id>', type='http', auth='public')
    def get_partner_image(self, partner_id):
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if partner.image_1920:
            image = base64.b64decode(partner.image_1920)
            return request.make_response(image, [
                ('Content-Type', 'image/jpeg')
            ])
        return request.not_found()
