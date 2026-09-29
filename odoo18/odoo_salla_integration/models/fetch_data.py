# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from logging import getLogger
_logger = getLogger(__name__)
from odoo.addons.odoo_multi_channel_sale.tools import remove_tags

class FetchData:
    def __init__(self, channel_id, **kw):
        self.channel_id = channel_id
        self.id = channel_id.id
        self.env = channel_id.env

    @staticmethod
    def _salla_amount(value):
        """Normalize Salla price/cost payloads to a plain number."""
        if isinstance(value, dict):
            return value.get('amount') or 0
        return value or 0

    def get_all_categories(self, data):
        category_vals = []
        for val in data:
            category_vals.append(
                self.category_for_category(val))
        for val in data:
            if val.get('items'):
                category_vals.extend(self.get_all_categories(
                    val.get('items')))
        return category_vals

    def category_for_category(self, data):
        category_vals = ({
            "channel_id": self.channel_id.id,
            "channel": self.channel_id.channel,
            "leaf_category": False if data.get('items') else True,
            "parent_id": data.get('parent_id') or False,
            "store_id": data.get('id'),
            "name": data.get('name')
        })
        return category_vals

    def get_shipping_vals(self, channel_id, shipping_data):
        return {
            "name": shipping_data.get("name"),
            "store_id": shipping_data.get("id"),
            "shipping_carrier": shipping_data.get("name"),
            "channel_id": channel_id.id,
            "channel": channel_id.channel,
            "description": shipping_data.get("activation_type", False)
        }

    def process_customer(self, customer):
        customer_data = {
            'channel_id': self.channel_id.id,
            'store_id': customer.get('id'),
            'name': customer.get('first_name', False),
            'last_name':customer.get('last_name', False),
            'email': customer.get('email'),
            'mobile': customer.get('mobile'),
            'city': customer.get('city'),
            'street': customer.get('location', False),
            'country_code': customer.get('country_code') if customer.get('country_code') else customer.get('country'),
            'website': customer.get('urls').get('customer') if customer.get('urls') else False
        }
        address_data_list = []
        customer_data['contacts'] = address_data_list
        return customer_data

    def process_address(self, order, store_partner_id, type=False):
        contacts = {}
        billing_address = []
        email = order.get('customer').get('email')
        name = order.get('customer').get('first_name')+ " "+ order.get('customer').get('last_name')
        phone = order.get('customer').get('mobile')

        address = order.get('shipments', {})
        if isinstance(address, list):
            address = address[0]
            if isinstance(address, list):
                address = address[0]
            billing_address = address.get('ship_to', {})
            if billing_address:
                name = billing_address.get('name')
                phone = billing_address.get('phone')
        if not billing_address and order.get('shipping'):
            billing_address = order.get('shipping').get('address')
            receiver_data = order.get('shipping').get('receiver', {})
            if receiver_data and isinstance(receiver_data, dict):   
                name = receiver_data.get('name') if receiver_data.get('name') else name
                email = receiver_data.get('email') if receiver_data.get('email') else email
                phone = receiver_data.get('phone') if receiver_data.get('phone') else phone
        if billing_address:
            contacts.update({
                'invoice_partner_id': f'billing_{store_partner_id}' if store_partner_id else email,
                'invoice_name': name,
                'invoice_email':  email,
                'invoice_phone': phone,
                'invoice_street': billing_address.get('street_number'),
                'invoice_street2': billing_address.get('shipping_address') or billing_address.get('address_line'),
                'invoice_zip': billing_address.get('postal_code'),
                'invoice_city': billing_address.get('city'),
                'invoice_country_code': billing_address.get('country_code') or False,
                'same_shipping_billing': True
            })
        return contacts

    def import_product_vals(self, product):
        vals = self.get_product_basic_vals(product)
        if product.get('options'):
            variants, options = self.get_variant_vals(product)
            vals.update(
                {'variants': variants, 'salla_product_attribute_options': options})
        return vals

    def get_product_basic_vals(self, product):
        return {
            'store_id': product.get('id'),
            'name': product.get('name'),
            'channel_id': self.id,
            'channel': self.channel_id.channel,
            'description_sale': remove_tags(product.get('description') or ''),
            'description': product.get('promotion').get('sub_title'),
            'image_url': product.get('main_image'),
            'list_price': self._salla_amount((product.get('price') or {}).get('amount')),
            'standard_price': self._salla_amount(product.get('cost_price')),
            'weight': product.get("weight"),
            'wk_default_code': product.get("sku"),
            'default_code': product.get("sku"),
            'barcode': product.get("barcode") or product.get("gtin") or product.get("mpn"),
            'qty_available': product.get("quantity"),
            'extra_categ_ids': ",".join([str(x.get('id')) for x in product.get('categories')]) if product.get('categories') else False
        }

    def get_variant_vals(self, product):
        options = self.get_product_options(product.get('options'))
        variants = []
        salla_product_attribute_option_vals = {}
        for variant in product.get('skus') or []:
            name_value = []
            salla_options = variant.get('related_option_values') or []
            if salla_options:
                salla_options.sort()
                salla_product_attribute_option_vals.update(
                    {"_".join(map(str, salla_options)): variant.get('id')})
            if options and salla_options:
                name_value = [{
                    'name': options.get(attribute_id).get('name'),
                    'value': options.get(attribute_id).get('value_name'),
                } for attribute_id in salla_options if options.get(attribute_id)]
            variants.append({
                'default_code': variant.get('sku'),
                'barcode': variant.get('barcode'),
                'store_id': variant.get('id'),
                'qty_available': variant.get('stock_quantity'),
                'list_price': self._salla_amount((variant.get('price') or {}).get('amount')),
                'standard_price': self._salla_amount(variant.get('cost_price')),
                'weight': variant.get('weight'),
                # 'image_url': image_url,
                'name_value': name_value,
            })
        return variants, salla_product_attribute_option_vals or False

    def get_product_options(self, options):
        """
            options will be : 
            {
                value_id1: {option_name:name, option_id: id, value_name: value_name},
                value_id2: {option_name:name, option_id: id, value_name: value_name},
                ...
            }
        """
        option_vals = {}
        for option in options:
            for value in option.get('values'):
                option_vals.update({value.get('id'): {'name': option.get(
                    'name'), 'id': option.get('id'), 'value_name': value.get('name')}})
        return option_vals

    @staticmethod
    def _salla_tax_snapshot(tax):
        """Extract percent/amount from a Salla tax object for logging."""
        if not tax or not isinstance(tax, dict):
            return {'percent': None, 'amount': None, 'raw': tax}
        amount_obj = tax.get('amount')
        tax_amount = None
        if isinstance(amount_obj, dict):
            tax_amount = amount_obj.get('amount')
        elif amount_obj is not None:
            tax_amount = amount_obj
        return {
            'percent': tax.get('percent'),
            'amount': tax_amount,
            'raw': tax,
        }

    def _log_salla_order_line_tax(self, order_name, store_id, line_source, line_name, raw_tax, line_taxes):
        _logger.info(
            'Salla order tax | order_name=%s | store_id=%s | line=%s | name=%r | '
            'salla_tax=%s | feed_line_taxes=%s',
            order_name,
            store_id,
            line_source,
            line_name,
            self._salla_tax_snapshot(raw_tax),
            line_taxes,
        )

    def process_order(self, order):
        order_name = str(order.get('reference_id') or order.get('id'))
        store_id = order.get('id')
        order_amounts = order.get('amounts') or {}
        raw_order_tax = order_amounts.get('tax')
        _logger.info(
            'Salla order tax | order_name=%s | store_id=%s | order_level_tax=%s',
            order_name,
            store_id,
            self._salla_tax_snapshot(raw_order_tax),
        )
        order_data = {
            'channel_id': self.id,
            'store_id': store_id,
            'name': order_name,
            'currency': order.get('currency'),
            'date_order': order.get('date').get('date'),
            'confirmation_date': order.get('date').get('date'),
            'order_state': order.get('status').get('slug'),
            'line_type': 'multi'
        }
        if order.get('payment_method'):
            order_data.update(payment_method=order.get('payment_method'))
        if order.get('shipping') or order.get('shipments'):
            if type(order.get('shipping')) == dict:
                order_data.update(
                    {'carrier_id': order.get('shipping').get('company')})
            # elif type(order.get('shipments')) == dict:
            elif order.get('shipments'):
                shipments =order.get('shipments')[0]
                order_data.update(
                    {'carrier_id': shipments.get('courier_name')})     
        if order.get('customer'):
            customer = order.get('customer')
            order_data.update(
                {
                    'partner_id': customer.get('id'),
                    'customer_name': customer.get('first_name')+' '+customer.get('last_name'),
                    'customer_email': customer.get('email'),
                    'customer_mobile': customer.get('mobile'),
                    'customer_phone': customer.get('mobile'),
                }
            )
            contacts = self.process_address(order, customer.get('id'))
            order_data.update(contacts)
        order_lines = [(5, 0)]
        product_taxes_list = []
        for line in order.get("items") or []:
            line_product_id = line.get("product").get("id") if line.get("product") else line.get("product_id")
            exists = self.channel_id.match_template_mappings(line_product_id)
            attribute_options = False
            if not exists:
                #Update or create product feed only if there is no mapping exists
                attribute_options = self.create_product_feed(line_product_id)
            line_variant_id = "No Variants"
            if line.get("options"):
                line_variant_id = self.get_variant_id(line, attribute_options)
                if not line_variant_id and not attribute_options:
                    attribute_options = self.create_product_feed(line_product_id)
                    line_variant_id = self.get_variant_id(line, attribute_options)
                if not line_variant_id:
                    if self._should_use_no_variants_fallback(line_product_id):
                        line_variant_id = "No Variants"
                        _logger.warning(
                            'Salla variant unresolved for order %s product %s sku %s options %s; '
                            'using No Variants fallback',
                            order_name,
                            line_product_id,
                            line.get("sku", False),
                            line.get("options"),
                        )
                    else:
                        line_variant_id = "SALLA_UNRESOLVED_VARIANT"
                        _logger.error(
                            'Could not resolve Salla variant for order %s product %s sku %s options %s',
                            order_name,
                            line_product_id,
                            line.get("sku", False),
                            line.get("options"),
                        )
            amounts = line.get("amounts") or {}
            price_without_tax = amounts.get("price_without_tax") or {}
            raw_item_tax = amounts.get("tax")
            line_price = price_without_tax.get("amount")
            line_taxes = self.process_tax(raw_item_tax, line_price=line_price)
            product_taxes_list.append(line_taxes)
            order_line_data = {
                'line_name': line.get("name"),
                'line_product_id': line_product_id,
                'line_variant_ids': line_variant_id,
                'line_price_unit': line_price,
                'line_product_uom_qty': line.get("quantity"),
                'line_product_default_code': line.get("sku", False),
                'line_taxes': line_taxes,
            }
            self._log_salla_order_line_tax(
                order_name, store_id, 'product', line.get('name'), raw_item_tax, line_taxes,
            )
            order_lines.append((0, 0, order_line_data))
        # Discount Line and Delivery Line
        order_tax = self.process_tax(raw_order_tax)
        _logger.info(
            'Salla order tax | order_name=%s | store_id=%s | line=order_tax_processed | feed_line_taxes=%s',
            order_name,
            store_id,
            order_tax,
        )
        order_dicounts = order_amounts.get('discounts')
        product_taxes = self._uniform_product_taxes(product_taxes_list)
        if order_dicounts:
            discount_line = self.get_discount_line(order_dicounts, product_taxes=product_taxes)
            if discount_line:
                discount_vals = discount_line[2]
                self._log_salla_order_line_tax(
                    order_name,
                    store_id,
                    'discount',
                    discount_vals.get('line_name'),
                    raw_order_tax,
                    discount_vals.get('line_taxes'),
                )
                order_lines.append(discount_line)
        if order_amounts.get('shipping_cost'):
            delivery_line = self.get_delivery_line(order, order_tax)
            if delivery_line:
                delivery_vals = delivery_line[2]
                self._log_salla_order_line_tax(
                    order_name,
                    store_id,
                    'delivery',
                    delivery_vals.get('line_name'),
                    raw_order_tax,
                    delivery_vals.get('line_taxes'),
                )
                order_lines.append(delivery_line)
        cash_on_delivery = order_amounts.get('cash_on_delivery', {})
        if cash_on_delivery:
            amt = float(cash_on_delivery.get('amount', 0.0))
            if amt:
                cod_line = self.get_other_line('COD Charges', order_tax, amt, line_source='other_charge')
                if cod_line:
                    cod_vals = cod_line[2]
                    self._log_salla_order_line_tax(
                        order_name,
                        store_id,
                        'other_charge',
                        cod_vals.get('line_name'),
                        raw_order_tax,
                        cod_vals.get('line_taxes'),
                    )
                    order_lines.append(cod_line)
        order_data['line_ids'] = order_lines
        return order_data
    
    def get_other_line(self, name, order_tax, amount, line_source='other_charge'):
        if amount:
            return (0, 0, {
                'line_name': name,
                'line_price_unit': amount,
                'line_product_uom_qty': 1,
                'line_taxes': order_tax,
                'line_source': line_source,
            })
        return False

    def get_discount_line(self, order_dicounts, product_taxes=False):
        discount_amount = 0
        discount_line = False
        discount_label = 'Discount'
        for discount in order_dicounts:
            discount_amount += float(discount.get('discount') or 0)
            discount_label = discount.get('title') or discount.get('code') or discount_label
        if discount_amount:
            discount_line = (0, 0, {
                'line_name': 'Discount: {}'.format(discount_label),
                'line_price_unit': discount_amount,
                'line_product_uom_qty': 1,
                'line_source': 'discount',
                # Mirror product VAT for ZATCA; never use order-level shipping tax here.
                'line_taxes': product_taxes or False,
            })
        return discount_line
    
    def get_delivery_line(self, order, order_tax):
        delivery_amount = 0
        delivery_line = False
        if order.get('amounts').get('shipping_cost', {}).get('amount'):
            delivery_amount += order.get('amounts').get('shipping_cost', {}).get('amount')
        if delivery_amount:
            delivery_line = (0,0, {
                'line_name': 'Delivery',
                'line_price_unit': delivery_amount,
                'line_product_uom_qty': 1,
                'line_taxes': order_tax,
                'line_source': 'delivery',
            })
        return delivery_line

    def _get_salla_option_value_id(self, option_rec):
        """Extract a Salla option-value id from varying order-line option payloads."""
        value = option_rec.get('value')
        if isinstance(value, dict):
            opt_id = value.get('id')
            if opt_id is not None:
                return opt_id
        if isinstance(value, (int, float)):
            return int(value)
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.isdigit():
                return int(stripped)
        for key in ('value_id', 'option_value_id', 'id'):
            candidate = option_rec.get(key)
            if isinstance(candidate, (int, float)):
                return int(candidate)
            if isinstance(candidate, str) and candidate.strip().isdigit():
                return int(candidate.strip())
        return None

    def _get_variant_id_by_option_names(self, order_line_product, store_product_id):
        """Resolve variant store id by matching option name/value labels on the product feed."""
        options = order_line_product.get('options') or []
        line_attrs = []
        for rec in options:
            name = rec.get('name') or rec.get('option_name')
            value = rec.get('value')
            if isinstance(value, dict):
                val_name = value.get('name') or value.get('value')
            else:
                val_name = value
            if name and val_name:
                line_attrs.append((str(name).strip().lower(), str(val_name).strip().lower()))
        if not line_attrs:
            return False
        line_attrs_set = frozenset(line_attrs)
        feed = self.channel_id.match_product_feeds(store_product_id)
        if not feed:
            return False
        for variant in feed.feed_variants:
            if not variant.name_value:
                continue
            try:
                name_values = eval(variant.name_value)
            except Exception:
                continue
            variant_attrs = frozenset(
                (str(nv.get('name', '')).strip().lower(), str(nv.get('value', '')).strip().lower())
                for nv in name_values
                if nv.get('name') and nv.get('value')
            )
            if variant_attrs == line_attrs_set:
                return variant.store_id
        return False

    def _should_use_no_variants_fallback(self, store_product_id):
        """Return True when unresolved options should map to a simple (no-variant) product."""
        if self.channel_id.match_product_mappings(store_product_id, 'No Variants'):
            return True
        product_feed = self.channel_id.match_product_feeds(store_product_id)
        if product_feed and len(product_feed.feed_variants) <= 1:
            return True
        template_mapping = self.channel_id.match_template_mappings(store_product_id)
        if template_mapping:
            template = template_mapping.template_name
            if template and not template.salla_product_attribute_options:
                return True
        return False

    def get_variant_id(self, order_line_product, attribute_options=False):
        store_product_id = (
            order_line_product.get('product').get('id')
            if order_line_product.get('product')
            else order_line_product.get('product_id')
        )
        option_vals = []
        for rec in order_line_product.get('options') or []:
            opt_id = self._get_salla_option_value_id(rec)
            if opt_id is not None:
                option_vals.append(opt_id)
        if option_vals:
            option_vals.sort()
            value = '_'.join(map(str, option_vals))
            mappings = self.channel_id.match_template_mappings(store_product_id=store_product_id)
            if mappings:
                template_id = mappings.template_name
                if template_id and template_id.salla_product_attribute_options:
                    options = eval(template_id.salla_product_attribute_options)
                    variant_id = options.get(value)
                    if variant_id:
                        return variant_id
            elif attribute_options:
                variant_id = eval(attribute_options).get(value)
                if variant_id:
                    return variant_id
        variant_id = self._get_variant_id_by_option_names(order_line_product, store_product_id)
        if variant_id:
            return variant_id
        if order_line_product.get('options'):
            _logger.warning(
                'Could not resolve Salla variant for product %s with options %s',
                store_product_id, order_line_product.get('options'),
            )
        return False

    @staticmethod
    def _tax_dict(rate):
        return [
            {
                'included_in_price': False,
                'name': f"Salla Tax {rate}%",
                'rate': rate,
                'tax_type': 'percent',
            }
        ]

    @staticmethod
    def _uniform_product_taxes(product_taxes_list):
        """Return shared product tax when every taxed product uses the same rate."""
        taxes = [t for t in product_taxes_list if t]
        if not taxes:
            return False
        rates = set()
        for tax_entries in taxes:
            for entry in tax_entries:
                rates.add(entry.get('rate'))
        if len(rates) == 1:
            return taxes[0]
        return False

    def process_tax(self, tax, line_price=None):
        """Map a Salla tax object to multichannel feed tax dicts.

        Uses tax amount when present. For product lines with a positive price,
        falls back to percent when Salla sends amount=0 (common on coupon orders)
        so every line carries a VAT rate for ZATCA. Order-level shipping tax
        must be passed without line_price so amount=0 stays untaxed.
        """
        if not tax or not isinstance(tax, dict):
            return False
        amount_obj = tax.get('amount')
        tax_amount = None
        if isinstance(amount_obj, dict):
            tax_amount = amount_obj.get('amount')
        elif amount_obj is not None:
            tax_amount = amount_obj
        try:
            tax_amount = float(tax_amount) if tax_amount is not None else None
        except (TypeError, ValueError):
            tax_amount = None
        try:
            percent = float(tax.get('percent')) if tax.get('percent') is not None else None
        except (TypeError, ValueError):
            percent = None

        if tax_amount == 0:
            if percent and percent > 0 and line_price is not None:
                try:
                    if float(line_price) > 0:
                        return self._tax_dict(percent)
                except (TypeError, ValueError):
                    pass
            return False
        if tax_amount and tax_amount > 0 and percent:
            rate = percent
        elif percent and percent > 0 and tax_amount is None:
            rate = percent
        else:
            return False
        return self._tax_dict(rate)

    def create_product_feed(self, object_id): # orders item
        try:
            kw = dict(
                filter_type='id',
                object_id=str(object_id),
                page_size= self.channel_id.api_record_limit,
            )
            values, kw = self.channel_id.get_sallaApi().get_products(**kw)
            if values:
                vals = values[0]
                variants = vals.pop('variants', [])
                if variants:
                    feed_variants = [(0, 0, variant) for variant in variants]
                    vals.update(feed_variants=feed_variants)
                feed = self.channel_id.match_product_feeds(object_id)
                if not feed: #create product feed
                    feed = self.env['product.feed'].create(vals)
                return feed.salla_product_attribute_options
        except Exception as e:
            _logger.error('Error occurred %r',e, exc_info=True)            
        return False
