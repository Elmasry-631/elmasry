# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################
from odoo import http
from odoo.http import request

from logging import getLogger
_logger = getLogger(__name__)


class OdooSallaConnector(http.Controller):
	@http.route('/salla/authenticate', type='http', auth='public')
	def odoo_salla_connector(self, *args, **kwargs):
		return_key, instance_id = kwargs.get('state') , False
		multichannel = request.env['multi.channel.sale']
		if return_key:
			try:
				connection = multichannel.search([('salla_verification_key','=',return_key)], limit=1)
				if not connection:
					_logger.error(f"Authentication Failed, there is no multichannel instance with verification key: '{return_key}' in your odoo")
				else:
					instance_id = connection.id
					if kwargs.get('error'):
						connection.write({'state': 'error'})
						_logger.error('Error: %r', kwargs)
					else:
						result = self.client_salla_connected(kwargs)
			except Exception as e:
				_logger.error("Error Found While Generating Access Token %r", str(e))
		return request.redirect(multichannel.redirect_to_channel(instance_id))
	
	
	def client_salla_connected(self, kwargs):
		access_token = kwargs.get('access_token')
		refresh_token = kwargs.get('refresh_token')
		# token_expiry = kwargs.get('token_expiry')
		store_name = kwargs.get('store_name')
		store_id = kwargs.get('store_id')
		verification_key = kwargs.get('state')

		channel = request.env['multi.channel.sale'].sudo().search([
		('salla_verification_key', '=', verification_key)
		], limit=1)

		if channel:
			return channel.write({
			'access_token': access_token,
			'refresh_token': refresh_token,
			# 'salla_token_expiry': token_expiry,
			'salla_store_name': store_name,
			'salla_store_id': store_id,
			'state': 'validate',
			})
		return False
