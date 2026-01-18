from pickle import FALSE
import json
import requests
from odoo import http
from odoo.http import request


class TestApi(http.Controller):
    @http.route("/v1/test_api", type="http",auth = "none", csrf=False, methods=["POST"])
    def test_read_api(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['test.app.odoo'].sudo().create(vals)
        print(res)
        if res:
            return request.make_json_response(
                {
                    "massage": "success"
                }, status=201
            )

    @http.route("/v1/test_api", type="json", auth="none", csrf=False, methods=["POST"])
    def test_read_api(self):
        args = request.httprequest.data.decode()
        vals = json.loads(args)
        res = request.env['test.app.odoo'].sudo().create(vals)
        print(res)
        if res:
           return [ {
                "massage": "success"
            }]
