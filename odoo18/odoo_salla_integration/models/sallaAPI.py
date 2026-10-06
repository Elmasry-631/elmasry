# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
import requests
import json
import re
from time import sleep
from datetime import date, datetime, timedelta
from .fetch_data import FetchData
from urllib.parse import urlparse, parse_qs
from logging import getLogger
from odoo.exceptions import UserError
_logger = getLogger(__name__)

SALLA_CUSTOMER_PAGE_SIZE = 60
SALLA_CUSTOMER_WINDOW_LIMIT = 9900
SALLA_CUSTOMER_DEFAULT_START = date(2000, 1, 1)
SALLA_CUSTOMER_WINDOW_DAYS = 366


class SallaApi:

    def __init__(self, client_id, client_secret, access_token, refresh_token, channel=False, **kw):
        self.channel_id = channel
        self.id = channel.id
        self.env = channel.env
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = access_token
        self.refresh_token = refresh_token
        # self.pricelist_id = pricelist_id
        # self.location_id = kw.get('location_id')

    def __enter__(self):
        self.import_url = "https://api.salla.dev/admin/v2/"
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        del self

    # def pre_get(self, kw):
    #     options = {}
    #     options['limit'] = kw['page_size']
    #     if 'next_url' in kw:
    #         options['next_url'] = kw['next_url']
    #     return options

    def fetch_data(self):  # The fetch data object
        return FetchData(self.channel_id)

    def get_headers(self):
        return {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + str(self.access_token)
        }

    def salla_pagination(self, pagination, kw):
        if pagination.get('links'):
            next_url = pagination.get("links").get('next')
            if next_url:
                kw['next_url'] = next_url
            else:
                kw['next_url']= None
                
        return kw

    # +++++++++++++++++++Response+++++++++++
    def salla_response(self, endpoint, method="GET", data={}, params={}, headers={}):
        headers = headers or self.get_headers()
        payload = json.dumps(data) if data else data
        for attempt in range(4):
            try:
                response = requests.request(
                    method, endpoint, headers=headers, data=payload, params=params, timeout=60)
            except requests.RequestException as e:
                _logger.error('Salla API network error on %s: %r', endpoint, e)
                raise UserError(f'Salla API unreachable: {e}') from e
            if response.status_code in (200, 201):
                return response.json()
            if response.status_code == 429 and attempt < 3:
                try:
                    wait = int(response.headers.get('Retry-After') or 5)
                except ValueError:
                    wait = 5
                wait = min(max(wait, 1), 60)
                _logger.warning('Salla rate limit hit on %s, sleeping %ss', endpoint, wait)
                sleep(wait)
                continue
            body = response.text[:500]
            # 404/422 are expected for some records (deleted order, non-shippable order).
            log = _logger.info if response.status_code in (404, 422) else _logger.error
            log('Salla API %s %s -> HTTP %s: %s', method, endpoint, response.status_code, body)
            if response.status_code in (401, 403, 429) or response.status_code >= 500:
                # Abort the run instead of pretending the store has no data.
                raise UserError(f'Salla API error {response.status_code} on {endpoint}: {body}')
            return []
        return []

    # ++++++++++++++++++++++Import++++++++++++++++++++++++++++++++++

    def get_categories(self, **kw):
        if kw.get('next_url'):
            endpoint = kw.get('next_url')
        else:
            endpoint = self.import_url + "categories"
        kw.setdefault('page_size', 20)
        params = {'with': 'items'}
        if kw.get('filter_type') == "id":
            endpoint += f"/{kw.get('object_id')}"
        if endpoint:
            response = self.salla_response(endpoint, params=params)
            if response and response.get('data'):
                if response.get('pagination'):
                    kw = self.salla_pagination(response.get('pagination'), kw)
                else:
                    kw.pop('next_url', None)
                if isinstance(response.get('data'), list):
                    categories = self.fetch_data().get_all_categories(response.get('data'))
                    _logger.info(
                        'Salla categories fetched: %s record(s), next_url=%s',
                        len(categories), kw.get('next_url'),
                    )
                    return categories, kw
                # entered id of child category
                if response.get('data').get('parent_id'):
                    kw.update({'object_id': response.get('data').get('parent_id')})
                    return self.get_categories(**kw)
                categories = self.fetch_data().get_all_categories([response.get('data')])
                kw.pop('next_url', None)
                return categories, kw
        return [], kw

    def get_shippings(self, **kw):
        if kw.get('filter_type') == "id":
            endpoint = self.import_url + \
                f"shipping/companies/{kw.get('object_id')}"
        else:
            endpoint = self.import_url+"shipping/companies"
        response = self.salla_response(endpoint)
        if response:
            if response.get('data'):
                if isinstance(response.get('data'), list):
                    return [self.fetch_data().get_shipping_vals(self.channel_id, data) for data in response.get('data')], kw
                else:
                    return [self.fetch_data().get_shipping_vals(self.channel_id, response.get('data'))], kw

        return [], kw

    @staticmethod
    def _customer_filter_date(value, default):
        if not value:
            return default
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, date):
            return value
        try:
            return datetime.fromisoformat(str(value)).date()
        except ValueError as exc:
            raise UserError(
                f"Invalid Salla customer import date: {value}"
            ) from exc

    def _init_customer_windows(self, kw):
        """Initialize an inclusive overall range and its first yearly window."""
        if kw.get('customer_range_from'):
            return
        range_from = self._customer_filter_date(
            kw.get('salla_from_date'),
            SALLA_CUSTOMER_DEFAULT_START,
        )
        range_to = self._customer_filter_date(
            kw.get('salla_to_date'),
            date.today(),
        )
        if range_from > range_to:
            raise UserError(
                "Salla customer import From Date must be before To Date."
            )
        window_to = min(
            range_from + timedelta(days=SALLA_CUSTOMER_WINDOW_DAYS - 1),
            range_to,
        )
        kw.update({
            'customer_range_from': range_from.isoformat(),
            'customer_range_to': range_to.isoformat(),
            'customer_window_from': range_from.isoformat(),
            'customer_window_to': window_to.isoformat(),
            'customer_page': 1,
        })

    def _advance_customer_window(self, kw):
        """Move to the next inclusive window; return False at range end."""
        current_to = date.fromisoformat(kw['customer_window_to'])
        range_to = date.fromisoformat(kw['customer_range_to'])
        next_from = current_to + timedelta(days=1)
        if next_from > range_to:
            kw['customer_windows_done'] = True
            kw.pop('next_url', None)
            return False
        next_to = min(
            next_from + timedelta(days=SALLA_CUSTOMER_WINDOW_DAYS - 1),
            range_to,
        )
        kw.update({
            'customer_window_from': next_from.isoformat(),
            'customer_window_to': next_to.isoformat(),
            'customer_page': 1,
        })
        kw.pop('next_url', None)
        return True

    def _shrink_customer_window(self, kw):
        """Halve an oversized date window, failing only for >9,900/day."""
        window_from = date.fromisoformat(kw['customer_window_from'])
        window_to = date.fromisoformat(kw['customer_window_to'])
        days = (window_to - window_from).days + 1
        if days <= 1:
            raise UserError(
                "Salla has more than 9,900 customers on "
                f"{window_from.isoformat()}. Its API cannot page beyond 10,000 "
                "records for one date; import that day using customer IDs."
            )
        window_to = window_from + timedelta(days=(days // 2) - 1)
        kw['customer_window_to'] = window_to.isoformat()
        kw['customer_page'] = 1
        kw.pop('next_url', None)

    def get_partners(self, **kw):
        customer_data_list = []
        kw['page_size'] = SALLA_CUSTOMER_PAGE_SIZE
        if kw.get('object_id'):
            endpoint = self.import_url + "customers/" + kw.get('object_id')
            response = self.salla_response(endpoint)
            if response and response.get('data'):
                customer_data_list.append(
                    self.fetch_data().process_customer(response['data'])
                )
            return customer_data_list, kw

        self._init_customer_windows(kw)
        while not kw.get('customer_windows_done'):
            customer_page = kw.get('customer_page', 1)
            is_window_first_page = customer_page == 1
            endpoint = self.import_url + "customers"
            params = {
                'page': customer_page,
                'per_page': SALLA_CUSTOMER_PAGE_SIZE,
                'date_from': kw['customer_window_from'],
                'date_to': kw['customer_window_to'],
            }

            response = self.salla_response(endpoint, params=params)
            if not response:
                raise UserError(
                    "Salla customer import request failed. Check the preceding "
                    "Salla API error in the Odoo log, then retry this import."
                )

            pagination = response.get('pagination') or {}
            total = pagination.get('total') or 0
            if is_window_first_page and total > SALLA_CUSTOMER_WINDOW_LIMIT:
                _logger.info(
                    'Salla customer range %s..%s has %s records; shrinking window',
                    kw['customer_window_from'],
                    kw['customer_window_to'],
                    total,
                )
                self._shrink_customer_window(kw)
                continue

            customers = response.get('data') or []
            if not isinstance(customers, list):
                customers = [customers]

            current_page = pagination.get('currentPage') or customer_page
            total_pages = pagination.get('totalPages') or current_page
            if current_page < total_pages:
                kw['customer_page'] = current_page + 1
            else:
                has_more_windows = self._advance_customer_window(kw)
                if has_more_windows and customers:
                    # Prevent ApiTransaction from stopping on a short final page.
                    kw['page_size'] = len(customers)

            if customers:
                customer_data_list = [
                    self.fetch_data().process_customer(customer)
                    for customer in customers
                ]
                return customer_data_list, kw

            # Skip empty date windows internally instead of ending the import.
            if kw.get('customer_windows_done'):
                break

        return customer_data_list, kw

    # Get products
    def get_products(self, **kw):
        params = {}
        product_data_list = []
        endpoint = self.import_url+f"products"
        if kw.get('filter_type') == "id":
            product_store_ids = list(set(s.strip() for s in kw.get('object_id').split(',')))
            for product_store_id in product_store_ids:
                if product_store_id:
                    endpoint = self.import_url + "products/" + product_store_id
                    response = self.salla_response(endpoint, params=params)
                    if response:
                        product_data = self.fetch_data().import_product_vals(response.get('data'))
                        product_data_list.append(product_data)
                        kw.update({'page_size': kw.get('page_size')+1})
        else:
            kw.update({'page_size': kw.get('page_size') if kw.get('page_size') <= 65 else 65})
            if not kw.get('next_url'):
                params = {'page': 1, 'per_page': kw.get('page_size')}
                if (kw.get('salla_product_keyword') and kw.get('salla_enable_keyword')) and (not kw.get('filter_type') == "date"):  # any keyword
                    params.update({'keyword': kw.get('salla_product_keyword')})
            else:
                endpoint = kw.get('next_url')
            response = self.salla_response(endpoint, params=params)
            if response:
                if response.get('data'):
                    if isinstance(response.get('data'), list):
                        product_data_list = [self.fetch_data().import_product_vals(product) for product in response.get('data')]
                        if response.get('pagination'):
                            kw = self.salla_pagination(
                                response.get('pagination'), kw)
                        else:
                            kw.update({'page_size': kw.get('page_size')+1})
        return product_data_list, kw

    def get_order_status(self, order_status_id):
        params = {}
        status_list = []
        endpoint = self.import_url + "orders/statuses"
        response = self.salla_response(endpoint, params=params)
        if response.get('data'):
            for data in response.get('data'):
                if str(data.get('original').get('id')) == order_status_id:
                    status_list.append(str(data.get('id')))
                    status_list.append(order_status_id)
        return status_list
        
    def _format_salla_date_param(self, value):
        """Salla filters orders by creation DATE only (yyyy-mm-dd)."""
        if not value:
            return value
        if hasattr(value, 'strftime'):
            return value.strftime('%Y-%m-%d')
        return str(value)[:10]

    def _enrich_order_with_items_and_shipments(self, data):
        """Fill missing items/shipments if order detail payload is incomplete."""
        if not data or not isinstance(data, dict):
            return data
        order_id = data.get('id')
        if not order_id:
            return data
        order_id = str(order_id)
        # Pickup / digital orders answer 422 on the shipments endpoint: skip them.
        shippable = (data.get('features') or {}).get('shippable', True)
        if not data.get('shipments') and shippable:
            shipments_resp = self.salla_response(
                self.import_url + "shipments?order_id=" + order_id,
                params={},
            )
            if shipments_resp and shipments_resp.get('data'):
                data['shipments'] = shipments_resp.get('data')
        if not data.get('items'):
            items_resp = self.salla_response(
                self.import_url + "orders/items?order_id=" + order_id,
                params={},
            )
            if items_resp and items_resp.get('data'):
                data['items'] = items_resp.get('data')
        return data

    def _fetch_order_detail(self, order_id):
        """Fetch full order detail (same shape previously provided by expanded=true)."""
        if not order_id:
            return False
        response = self.salla_response(
            self.import_url + "orders/" + str(order_id),
            params={},
        )
        if not response or not response.get('data'):
            return False
        return self._enrich_order_with_items_and_shipments(response.get('data'))

    # Get Orders
    def get_orders(self, **kw):
        order_data_list = []
        kw.update({'page_size': 15})  # order api has page size or limit is 15
        # Do not send `expanded`: Salla rejects Python bool True ("True") and the
        # param is deprecated for newer apps. List IDs, then fetch order details.
        params = {}
        if kw.get('filter_type') == "id":
            order_store_ids = list(set(s.strip() for s in kw.get('object_id').split(',')))
            for order_store_id in order_store_ids:
                if order_store_id:
                    data = self._fetch_order_detail(order_store_id)
                    if data:
                        order_data_list.append(self.fetch_data().process_order(data))
        else:
            if kw.get('next_url'):
                endpoint = kw.get('next_url')
                if kw.get('salla_order_status'):
                    parsed_url = urlparse(endpoint)
                    query_params = parse_qs(parsed_url.query)
                    page_value = query_params.get('page', [''])[0]
                    if page_value:
                        params.update({'status[]': kw.get('salla_order_status_list_id'), 'page': page_value})
                        endpoint = self.import_url + f"orders"
            else:
                if kw.get('filter_type') == "date":
                    params.update({
                        'from_date': self._format_salla_date_param(kw.get('salla_from_date')),
                        'to_date': self._format_salla_date_param(kw.get('salla_to_date')),
                    })
                    endpoint = self.import_url + "orders"
                else:  # by all
                    if kw.get('salla_order_status'):
                        status_list_id = self.get_order_status(kw.get('salla_order_status'))
                        params.update({'status[]': status_list_id})
                        kw.update({'salla_order_status_list_id': status_list_id})
                    params.update({'page': 1})
                    endpoint = self.import_url + f"orders"
            response = self.salla_response(endpoint, params=params)
            if response:
                if isinstance(response.get('data'), list):
                    order_data_list = []
                    for summary in response.get('data'):
                        # Prefer full order detail so line amounts/tax match expanded shape.
                        data = self._fetch_order_detail(summary.get('id')) or summary
                        data = self._enrich_order_with_items_and_shipments(data)
                        order_data_list.append(self.fetch_data().process_order(data))
                    if response.get("pagination"):
                        kw = self.salla_pagination(response.get('pagination'), kw)
        return order_data_list, kw

    # ++++++++++++++++++++++++Export++++++++++++++++++++++++++++++++++++

    def post_category(self, record, initial_record_id):
        return_list = [False, ""]
        cat_id = self.post_category_data(record, initial_record_id)
        if cat_id:
            return_list = [True, {"id": cat_id}]
        return return_list

    def post_category_data(self, record, initial_record_id):
        p_cat_id = 0
        if record.parent_id:
            parent_id = record.parent_id
            is_parent_mapped = self.channel_id.match_category_mappings(
                odoo_category_id=parent_id.id)
            if not is_parent_mapped:
                p_cat_id = self.post_category(parent_id, initial_record_id)
                if p_cat_id[0]:
                    p_cat_id = p_cat_id[1].get('id')
            else:
                p_cat_id = is_parent_mapped.store_category_id
        return self.export_category_data(record, initial_record_id, p_cat_id)

    def export_category_data(self, record, initial_record_id, parent_cat_id):
        returnid = False
        endpoint = self.import_url + "categories"
        data = {
            'name': record.name,
        }
        if parent_cat_id:
            data.update({'parent_id': parent_cat_id})
        response = self.salla_response(endpoint, method="POST", data=data)
        if response:
            returnid = response.get('data').get("id")
            if record.id != initial_record_id:
                self.channel_id.create_category_mapping(
                    record, returnid, leaf_category=False)
        return returnid

    def image_url(self, record): # Generate Image URL
        config_parameter = self.env['ir.config_parameter']
        url = config_parameter.get_param('web.base.url')
        if not url.endswith('/'):
            url += '/'
        name = record.name.replace(' ', '-').replace('/', '-')
        url += f"channel/image/{record._name}/{record.id}/image_1920/{name}.png"
        return url

    def post_product(self, record):
        options = []
        if record.attribute_line_ids:
            for rec in record.attribute_line_ids:
                data = {
                    "name": rec.attribute_id.name,
                    "display_type": "text",
                }
                values = []
                for val in rec.value_ids:
                    values.append(
                        {"name": val.name, "display_value": val.name})
                data.update({'values': values})
                options.append(data)
        data = self.get_export_product_vals(record, options)
        if data:
            if not record.attribute_line_ids:
                    data.update({"quantity": self.channel_id.get_quantity(record.product_variant_id)})
            endpoint = self.import_url + 'products'
            response = self.salla_response(endpoint, method="POST", data=data)
            if response:
                product_id = int(response.get('data').get('id'))
                if response.get('data').get('options') and response.get('data').get('skus'):
                    salla_product_attribute_option_vals = {}
                    for rec in response.get('data').get('skus'):
                        related_options = rec.get("related_option_values")
                        related_options.sort()
                        val = {
                            "_".join(map(str, related_options)): rec.get("id")
                        }
                        salla_product_attribute_option_vals.update(val)
                    variant_ids = self.match_remote_local_variants(self.post_manage_local_variants(
                        record), self.post_manage_remote_variants(response.get('data').get('skus'), response.get('data').get('options')))
                    if variant_ids:
                        record.write(
                            {'salla_product_attribute_options': salla_product_attribute_option_vals or False})
                        return True, {'id': product_id, 'variants': variant_ids}
                if not record.default_code:
                    record.write({'default_code': data.get('sku')})
                return True, {"id": product_id, "variants": [{"id": 'No Variants'}]}
        return False, {}

    def get_export_product_vals(self, record, options):
        sku = record.default_code
        if not len(record.product_variant_ids) > 1:
            if not sku: # Single Variant
                if self.channel_id.sku_sequence_id:
                    sku = self.channel_id.sku_sequence_id.next_by_id()
                else:
                    _logger.info(
                        'Error: SKU(Internal Refrence) or parent code is required for product syncronization')
                    return False
        else: # Multiple Variant 
            sku = record.wk_default_code or '' # Not required to pass SKU
        category_ids = record.channel_category_ids.filtered(
            lambda c: c.instance_id .id == self.channel_id.id).extra_category_ids
        
        if  not record.weight and not len(record.product_variant_ids) > 1:
            raise UserError("Please enter the weight. This field is required (For Salla).")
        if not category_ids:
            if self.channel_id.default_category_id and self.channel_id._context.get('operation') != 'update':
                category_mapped = self.channel_id.match_category_mappings(
                    odoo_category_id=self.channel_id.default_category_id.id)
                if not category_mapped:  # default category
                    default_category_vals = self.post_category(
                        self.channel_id.default_category_id, self.channel_id.default_category_id.id)
                    store_category_ids = [default_category_vals[1].get(
                        'id')] if default_category_vals[0] else []
                    self.channel_id.create_category_mapping(
                        self.channel_id.default_category_id, store_category_ids[0], leaf_category=False) if store_category_ids else None
                else:
                    store_category_ids = [
                        category_mapped.store_category_id]
            else:
                store_category_ids = []
        else:
            store_category_ids = list(map(lambda x: x.channel_mapping_ids.filtered(
                lambda x: x.channel_id == self.channel_id).store_category_id, category_ids))
        cleaner = re.compile('<.*?>')  # Removing HTML Tags
        subtitle = re.sub(
            cleaner, '', record.description) if record.description else record.name
        return {
            "name": record.name,
            "price": self.channel_id.pricelist_name._get_product_price(record, quantity=1),
            "status": "sale",
            "product_type": "product",
            # "quantity": record.qty_available,
            "description": record.description_sale or "",
            "categories": store_category_ids,
            "sale_price": self.channel_id.pricelist_name._get_product_price(record, quantity=1),
            "cost_price":record.standard_price,
            "require_shipping": True,
            "maximum_quantity_per_order": 1000,
            "unlimited_quantity": False,
            "sku": sku,
            "hide_quantity": False,
            "enable_upload_image": True,
            "enable_note": True,
            "pinned": True,
            "active_advance": True,
            "subtitle": subtitle,
            "promotion_title": "New",
            "metadata_title": record.name,
            "metadata_description": record.description_sale or "",
            "weight": record.weight or 0.00001,
            "images": [
                {
                    "original": self.image_url(record),
                    "thumbnail": self.image_url(record),
                    "alt": "image",
                    "default": True,
                    "sort": 5
                }
            ],
            'options': options if not self.channel_id._context.get('operation') == "update" else []
        }

    def post_manage_local_variants(self, record):
        """return->eg:
                {product.product(374,): {'Legs': 'Steel', 'Duration': '1 year'}, 
        product.product(375,): {'Legs': 'Steel', 'Duration': '2 year'}, 
        product.product(376,): {'Legs': 'Aluminium', 'Duration': '1 year'}, 
        product.product(377,): {'Legs': 'Aluminium', 'Duration': '2 year'}}
        """
        local_options = {}
        if record.attribute_line_ids:
            for product in record.product_variant_ids:
                values = {}
                for attribute in product.product_template_attribute_value_ids:
                    values.update(
                        {attribute.attribute_id.name: attribute.name})
                local_options.update({product: values})
        return local_options

    def post_manage_remote_variants(self, product_skus, options):
        """return->eg:
                {340856358: {'Legs': 'Steel', 'Duration': '1 year'},
                1715350823: {'Legs': 'Steel', 'Duration': '2 year'}, 
        807095328: {'Legs': 'Aluminium', 'Duration': '1 year'}, 
        232811297: {'Legs': 'Aluminium', 'Duration': '2 year'}}
        """
        options_val = {}
        remote_variants = {}
        for option in options:
            values = {value.get('id'): {option.get('name'): value.get(
                'name')} for value in option.get('values')}
            options_val.update(values)
        for sku in product_skus:
            remote_values = {}
            for value_id in sku.get('related_option_values'):
                remote_values.update(options_val.get(value_id))
            remote_variants.update({sku.get('id'): remote_values})
        return remote_variants

    # Updating variants during export operation
    def match_remote_local_variants(self, local_attributes, remote_attributes):
        """return->eg
                {'product.product(374,)': 340856358}
                {'product.product(375,)': 1715350823}
                {'product.product(376,)': 807095328}
                {'product.product(377,)': 232811297}
        """
        final_dict = {}
        variant_ids = []
        for a, b in local_attributes.items():
            for i, j in remote_attributes.items():
                if b == j:
                    final_dict.update({a: i})
                    break
        for variant_id, remote_id in final_dict.items():  # updating product during export operation
            self.update_product_variants(variant_id, remote_id)
            variant_ids.append({'id': remote_id})
        return variant_ids

    # +++++++++++++++++++++++++++Update+++++++++++++++++++++++++++++

    def update_salla_product(self, record_id, remote_id):
        try:
            if self.channel_id.debug == 'enable':
                _logger.info('Warning: During update opeartion the number of variants can not be updated from odoo to salla')
            number_of_variants = self.channel_id.match_product_mappings(remote_id, limit=False)
            # Check the number of variants
            if not len(number_of_variants) == len(record_id.product_variant_ids):
                _logger.error('Error: Can not change/update the number of variants from odoo to salla for product [{}]'.format(record_id.name))
                return [False, "Error in updating product"]
            endpoint = self.import_url+f'products/{remote_id}'
            data = self.get_export_product_vals(record_id, False)
            if data:
                default_ir_values = self.channel_id.default_multi_channel_values()
                avoid_duplicity = default_ir_values.get('avoid_duplicity')
                if avoid_duplicity:
                    _logger.warning('Warning: Can not update the product sku and barcode, avoid duplicity is enabled')
                    data.pop('sku', False)
                if not record_id.attribute_line_ids:
                    data.update({"quantity": self.channel_id.get_quantity(record_id.product_variant_id)})
                response = self.salla_response(
                    endpoint, method="PUT", data=data)
                if response:
                    # manage default code in mappings
                    if not avoid_duplicity:
                        match_template = self.channel_id.match_template_mappings(remote_id)
                        if match_template and data.get('sku', False):
                            match_template.default_code = data.get('sku')
                    if response.get('data').get('skus'):
                        # variable type product
                        for sku in response.get('data').get('skus'):
                            match = self.channel_id.match_product_mappings(
                                remote_id, sku.get('id'))
                            if match and (not avoid_duplicity) and self.channel_id._context.get('operation') == "update":
                                self.update_product_variants(
                                    match.product_name, sku.get('id'), avoid_duplicity)
                    else:
                        # simple type product
                        match = self.channel_id.match_product_mappings(remote_id)
                        if match and (not avoid_duplicity) and self.channel_id._context.get('operation') == "update":
                            match.default_code = record_id.default_code
                    return [True, response]
        except Exception as e:
            _logger.error(
                'Error: exception occurred during update %r', e, exc_info=True)
        return [False, "Error in updating product"]

    def update_product_variants(self, record_id, remote_id, avoid_duplicity = False):
        endpoint = self.import_url + f'products/variants/{remote_id}'
        data = {
            "price": self.channel_id.pricelist_name._get_product_price(record_id, quantity=1),
            "sale_price": self.channel_id.pricelist_name._get_product_price(record_id, quantity=1),
            "stock_quantity": self.channel_id.get_quantity(record_id),
            "cost_price":record_id.standard_price,
            "weight": record_id.weight,
        }
        if not (self.channel_id._context.get('operation') == "update") or (self.channel_id._context.get('operation') == "update" and (not avoid_duplicity)):
            data.update({
                "sku": record_id.default_code or "",
                "barcode": record_id.barcode or "",
            })
        response = self.salla_response(endpoint, method="PUT", data=data)
        if not response:
            _logger.error('Error in updating product variant %r', remote_id)
                

    def update_category(self, record, initial_record_id, remoteid):
        return_list = [False, '']
        response = self.salla_sync_categories_update(
            record, initial_record_id, remoteid)
        if response:
            return_list = [True, {"id": response}]
        return return_list

    def salla_sync_categories_update(self, record, initial_record_id, remote_id):
        parent_remote_id = False
        if record.parent_id.id:
            is_parent_mapped = self.channel_id.match_category_mappings(
                odoo_category_id=record.parent_id.id)
            if is_parent_mapped:
                parent_remote_id = self.update_category(
                    record.parent_id, initial_record_id, is_parent_mapped.store_category_id)
            else:
                parent_remote_id = self.post_category(
                    record.parent_id, initial_record_id)
            if isinstance(parent_remote_id, list):
                parent_remote_id = parent_remote_id[1].get("id")
        return self.salla_update_category(record, parent_remote_id, remote_id)

    def salla_update_category(self, record, parent_remote_id, remote_id):
        endpoint = self.import_url + f'categories/{remote_id}'
        data = {'name': record.name, }
        if parent_remote_id:
            data.update({'parent_id': parent_remote_id})
        response = self.salla_response(endpoint, method="PUT", data=data)
        if response:
            return response.get('data').get('id')
        return False

    # +++++++++++++++++++++++Core Methods++++++++++++++++++++++++++
    def set_quantity(self, product_id, qty=0, type="product"):
        if type == "product":
            endpoint = "products/quantities/" + product_id
        else:
            endpoint = "products/quantities/variant/" + product_id
        endpoint = self.import_url + endpoint
        data = {
            "quantity": qty,
        }
        res = self.salla_response(endpoint, method="PUT", data=data)
