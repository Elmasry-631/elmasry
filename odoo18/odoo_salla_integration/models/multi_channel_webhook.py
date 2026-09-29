# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################

from odoo import api, fields, models
import logging, json, requests, random, string
_logger = logging.getLogger(__name__)
from ..models.fetch_data import FetchData
from .multi_channel_sale import webkul_callback_url
from odoo.exceptions import UserError

class MultiChannelSale(models.Model):
    _inherit = "multi.channel.sale"
    
    create_order_webhook_secret = fields.Char(default=lambda self: self._generate_unique_code(32))
    update_order_webhook_secret = fields.Char(default=lambda self: self._generate_unique_code(32))

    def _generate_unique_code(self, length=5):
        return ''.join(random.choices(string.ascii_letters,k=length))

    def unsubscribe_active_event(self, url, type):
        """Disable all active webhooks with same event and same URL.
        """
        event_type = 'order.created' if type == 'create' else 'order.updated' if type == 'update' else False
        if event_type:
            endpoint = 'https://api.salla.dev/admin/v2/webhooks'
            api = self.get_sallaApi()
            res = api.salla_response(endpoint, method='GET')
            if res and res.get('data'):
                data = list(filter(lambda x:x.get('event') == event_type and x.get('url') == url, res.get('data')))
                for event in data:
                    res = api.salla_response('https://api.salla.dev/admin/v2/webhooks/unsubscribe', 
                                            method="DELETE", params={'id': event.get('id')})

    def activate_salla_order_webhook(self, url, type): 
        if type not in ['create','update']:
            _logger.error(f'Salla Channel does not support webhook for {type} order')
            return False
        if not url.startswith('https'):
            url = url.replace('http','https')
        if type == 'create':
            event = 'order.created'
            id_field = 'order_webhook_id'
        else:
            event = 'order.updated'
            id_field = 'order_update_webhook_id'
        params = {
            "event": event,
            "salla_verification_key":self.salla_verification_key,
            "activate":'subscribe',
        }
        endpoint = webkul_callback_url + "/webhook/setup"
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            result = response.json()
            if response.ok:
                if result.get('status_code') != 200:
                    raise
                _logger.info(f'Requested Webhook for {type} has been Activated Successfully')
                data = result.get('data',{})
                webhook_id = data.get('id', False)
                self.write({id_field: webhook_id})
            else:
                raise Exception('Error in activating event, please check error in Odoo logs!')
        except Exception as e:
            _logger.exception(f"Unhandled error during webhook activation.")
            raise UserError(result.get('message'))

    def deactivate_salla_order_webhook(self, url, type):
        if type not in ['create','update']:
            _logger.error(f'Salla does not support webhook for {type} order')
            return False
        if not url.startswith('https'):
            url = url.replace('http','https')
        endpoint = webkul_callback_url + "/webhook/setup"
        params = {
            'salla_verification_key':self.salla_verification_key,
            'activate':'unsubscribe'
        }
        if type == 'create':
            id_field = 'order_webhook_id'
            params.update({'id':self.order_webhook_id} if self.order_webhook_id else {'id':"order.created"})
        else:
            id_field = 'order_update_webhook_id'
            params.update({'id':self.order_update_webhook_id} if self.order_update_webhook_id else {'id':"order.updated"})
        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            result = response.json()
            if response.ok:
                if result.get('status_code') != 200:
                    raise
                self.write({id_field: False})
                _logger.info(f'Requested Webhook for {type} has been Deactivated Successfully')
            else:
                raise Exception(f'Error in un-subscribing event, for more information please check error logs!')
        except Exception as e:
            _logger.exception(f"Unhandled error during webhook activation.")
            raise UserError(result.get('message'))
        
    def salla_order_webhook_data(self, data, headers, type, **kwargs):
        return_data = {}
        if data:
            json_data = json.loads(data.decode())
            order = json_data.get('data')
            order_data = FetchData(self).process_order(order)
            if order_data:
                return_data = {
                        'store_id': order_data.get('store_id'),
                        'data': order_data,
                    }
                if type == 'create':
                    return return_data
                if type == 'update':
                    return_data.update({'update_case': 'complete_update'})
                    return return_data

                else:
                    _logger.error('Please Check the Secret Key you have entered')        
        else:
            _logger.error('Please Check the Order Data')
            
    def salla_webhook_create_product_data(self, data, header, **kwargs):
        self.create_update_product(data, **kwargs)
        
    def salla_webhook_update_product_data(self, data, header, **kwargs):
        self.create_update_product(data, **kwargs)
    
    def create_update_product(self, data, **kwargs):
        try:
            payload = json.loads(data.decode())
            json_data = payload.get('data')
        except Exception as e:
            _logger.error(f"Failed to parse JSON: {e}")
            return

        message = ""
        product_data = FetchData(self).import_product_vals(json_data)
        
        if not product_data:
            _logger.warning("Data missing or invalid.")
            return
        store_id = product_data.get('store_id') if isinstance(product_data, dict) else None
        product_data_list = product_data if isinstance(product_data, list) else [product_data]
        matched = self.match_product_mappings(store_id)
        if not matched:
            message = "<br/><span class='text-info'>Realtime Product Created Successfully</span>"
        s_id, e_id, feed_id = self.env['product.feed'].with_context(channel_id=self)._create_feeds(product_data_list)

        if feed_id:
            additional_msg = "<br/><span class='text-info'>Realtime Product Updated Successfully</span>" if not message else message
            feed_id.message = additional_msg +(str(feed_id.message) or "")
            result_msg = self.evaluate_webhook(self, feed_id)
            if result_msg:
                message += result_msg

        if message:
            _logger.info(message)
    
    def salla_webhook_delete_product_data(self, data, header, **kwargs):
        try:
            payload = json.loads(data.decode())
            json_data = payload.get('data')
        except Exception as e:
            _logger.error(f"Failed to parse JSON: {e}")
            return
        
        if not json_data:
            _logger.warning("Data missing or invalid.")
            return
        
        store_id = json_data.get('id')
        match = self.match_template_mappings(store_id)
        if match:
            feed = self.match_product_feeds(store_id)
            if feed:
                feed.write({
                    'active': False,
                    'state': 'cancel',
                    'message': '<br/>Salla product delete webhook received; mapping preserved for historical orders.',
                })
            message = "Realtime Product Delete: Mapping preserved for historical orders."
        else:
            message = 'Realtime Product Delete: Mapping not found at odoo.'

        _logger.info(message)
    
    def salla_webhook_create_customer_data(self, data, header, **kwargs):
        self.create_update_customer(data, **kwargs)
        
    def salla_webhook_update_customer_data(self, data, header, **kwargs):
        self.create_update_customer(data, **kwargs)
        
    def create_update_customer(self, data, **kwargs):
        try:
            payload = json.loads(data.decode())
            json_data = payload.get('data')
        except Exception as e:
            _logger.error(f"Failed to parse JSON: {e}")
            return

        message = ""
        customer_data = FetchData(self).process_customer(json_data)
        if not customer_data:
            _logger.warning("Data missing or invalid.")
            return
        store_id = customer_data.get('store_id') if isinstance(customer_data, dict) else None
        customer_data_list = customer_data if isinstance(customer_data, list) else [customer_data]
        matched = self.match_partner_mappings(store_id)
        if not matched:
            message = "<br/><span class='text-info'>Realtime Customer Created Successfully</span>"
        s_id, e_id, feed_id = self.env['partner.feed'].with_context(channel_id=self)._create_feeds(customer_data_list)

        if feed_id:
            additional_msg = "<br/><span class='text-info'>Realtime Customer Updated Successfully</span>" if not message else message
            feed_id.message = additional_msg +(str(feed_id.message) or "")
            result_msg = self.evaluate_webhook(self, feed_id)
            if result_msg:
                message += result_msg

        if message:
            _logger.info(message)
    
    def salla_webhook_create_category_data(self, data, header, **kwargs):
        self.create_update_category(data, **kwargs)
    
    def salla_webhook_update_category_data(self, data, header, **kwargs):
        self.create_update_category(data, **kwargs)
        
    def create_update_category(self, data, **kwargs):
        try:
            payload = json.loads(data.decode())
            json_data = payload.get('data')
        except Exception as e:
            _logger.error(f"Failed to parse JSON: {e}")
            return

        message = ""
        store_id = json_data.get('id') if isinstance(category_data, dict) else None
        json_data = json_data if isinstance(json_data, list) else [json_data]
        category_data = FetchData(self).get_all_categories(json_data)
        
        if not category_data:
            _logger.warning("Data missing or invalid.")
            return
        
        category_data_list = category_data if isinstance(category_data, list) else [category_data]
        matched = self.match_category_mappings(store_id)
        if not matched:
            message = "<br/><span class='text-info'>Realtime Category Created Successfully</span>"
        s_id, e_id, feed_id = self.env['category.feed'].with_context(channel_id=self)._create_feeds(category_data_list)
        if feed_id:
            for feed in feed_id:
                additional_msg = "<br/><span class='text-info'>Realtime Category Updated Successfully</span>" if not message else message
                feed.message = additional_msg +(str(feed.message) or "")
                result_msg = self.evaluate_webhook(self, feed)
                if result_msg:
                    message += result_msg

        if message:
            _logger.info(message)
            
    def salla_webhook_create_storetax_data(self, data, header, **kwargs):
        try:
            payload = json.loads(data.decode())
            json_data = payload.get('data')
        except Exception as e:
            _logger.error(f"Failed to parse JSON: {e}")
            return
        
        message = "Real Time Store Tax Created Successfully"
        store_tax_value_id = float(json_data.get('tax')) if isinstance(json_data, dict) else None
        if not store_tax_value_id:
            _logger.info(f"#########: Store Tax Data : {json_data}")
            return
        
        tax_map_obj = self.env['channel.account.mappings']
        odoo_tax_obj = self.env['account.tax']
        matched = tax_map_obj.search([('store_tax_value_id', '=', str(store_tax_value_id)),('channel_id', '=', self.id),('tax_type', '=', 'percent')], limit=1)
        if not matched:
            tx_name = f"{self.channel}_{self.id}_{store_tax_value_id}"
            domain = [('amount', '=', store_tax_value_id), ('amount_type', '=', 'percent'), ('name', '=', tx_name)]
            tx = self.env['account.tax'].search(domain, limit=1)
            if not tx:
                tx = odoo_tax_obj.create(
                    {
                        'name': tx_name,
                        'amount_type': 'percent',
                        'price_include': False,
                        'amount': store_tax_value_id,
                    }
                )
            tax_map_obj.create(
                    {
                        'channel_id': self.id,
                        'store_tax_value_id': str(store_tax_value_id),
                        'tax_type': 'percent',
                        'include_in_price': False,
                        'tax_name': tx.id,
                        'odoo_tax_id': tx.id,
                    }
                )
        else:
            message = "Store Tax Already Mapped"
        _logger.info(message)
            
    def salla_webhook_create_shipping_company_data(self, data, header, **kwargs):
        self.create_update_shipping_company(data, **kwargs)
        
    def salla_webhook_update_shipping_company_data(self, data, header, **kwargs):
        self.create_update_shipping_company(data, **kwargs)
        
    def create_update_shipping_company(self, data, **kwargs):
        try:
            payload = json.loads(data.decode())
            json_data = payload.get('data')
        except Exception as e:
            _logger.error(f"Failed to parse JSON: {e}")
            return
        
        message = ""
        store_id = json_data.get('id') if isinstance(json_data, dict) else None
        
        if not json_data:
            _logger.warning("Data missing or invalid.")
            return
        
        shipping_company_name = json_data.get('name')
        matched = self.match_carrier_mappings(shipping_company_name)
        if not matched:
            message = "<br/><span class='text-info'>Realtime Shipping Company Created Successfully</span>"
            
        shipping_company_data_list = [
            {
                'channel_id':self.id,
                'store_id':store_id,
                'name':shipping_company_name,
                'shipping_carrier':shipping_company_name,
            }
        ]
        s_id, e_id, feed_id = self.env['shipping.feed'].with_context(channel_id=self)._create_feeds(shipping_company_data_list)
        if feed_id:
            for feed in feed_id:
                additional_msg = "<br/><span class='text-info'>Realtime Shipping Company Updated Successfully</span>" if not message else message
                feed.message = additional_msg +(str(feed.message) or "")
                result_msg = self.evaluate_webhook(self, feed)
                if result_msg:
                    message += result_msg

        if message:
            _logger.info(message)
            
    def salla_webhook_delete_shipping_company_data(self, data, header, **kwargs):
        try:
            payload = json.loads(data.decode())
            json_data = payload.get('data')
        except Exception as e:
            _logger.error(f"Failed to parse JSON: {e}")
            return
        
        if not json_data:
            _logger.warning("Data missing or invalid.")
            return
        
        store_id = json_data.get('id')
        shipping_company_name = json_data.get('name')
        domain = [('shipping_service_id', '=', store_id)]
        match = self.match_carrier_mappings(domain=domain)
        if match:
            match.unlink()
            message = "Realtime Shipping Company Deleted Successfully"
        else:
            message = 'Realtime Shipping Company Delete: Mapping not found at odoo.'

        _logger.info(message)
        
    
    def evaluate_webhook(self, channel, feed_id):
        message = "RealTime Feed Created/Updated Successfully, "
        if channel.auto_evaluate_feed:
            feed_id.with_context(from_webhook=True).import_items()
            if feed_id.state == 'done':
                message = "RealTime Evaluated Successfully, "
        return message + f'[Ref: {feed_id.name}, StoreID: {feed_id.store_id}]'
