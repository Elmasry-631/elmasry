import json

from odoo import http
from odoo.http import request


class ZKBiometric(http.Controller):
    @http.route('/v1/api_zk', type='http', auth='none', csrf=False, methods=['POST'])
    def api_zk_biometric(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['hr.attendance'].sudo().create(vals)
        print(res)
        if res:
            return request.make_json_response(
                {
                    "massage": "success"
                }, status=201
            )
