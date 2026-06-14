# -*- coding: utf-8 -*-

from odoo import http, _
from odoo.exceptions import AccessError, UserError
from odoo.http import request
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect


class ArcherMetaLeadAdsController(http.Controller):

    @http.route('/meta_lead_ads/oauth/callback', type='http', auth='public', methods=['GET'], csrf=False)
    def meta_oauth_callback(self, **kwargs):
        state = kwargs.get('state')
        code = kwargs.get('code')
        error = kwargs.get('error')

        if error:
            raise UserError(_("Meta authorization failed: %s") % error)

        credential_model = request.env['meta.app.credential'].sudo()
        credential_id = credential_model._validate_oauth_state(state)
        if not credential_id:
            raise AccessError(_("Invalid or expired OAuth state token."))

        credential = credential_model.browse(credential_id)
        if not credential.exists():
            raise NotFound()

        if not code:
            raise UserError(_("Meta did not return an authorization code."))

        credential.action_exchange_oauth_code(code)
        return redirect('/web#id=%s&model=meta.app.credential&view_type=form' % credential.id)
