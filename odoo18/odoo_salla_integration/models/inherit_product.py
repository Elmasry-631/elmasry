# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from html import escape
import copy
import logging

from odoo import fields, models, api
from odoo.addons.odoo_multi_channel_sale.models.feeds import feed

_logger = logging.getLogger(__name__)

auth_url = "https://accounts.salla.sa/oauth2/auth"
token_url = "https://accounts.salla.sa/oauth2/token"


class InheritWkFeed(models.Model):
    _inherit = "wk.feed"

    @api.model
    def get_product_fields(self):
        ProductFields = copy.deepcopy(feed.ProductFields)
        ProductFields.append('salla_product_attribute_options')
        return ProductFields
    
    def required_field_not_filled(self, fields, vals):
        res = super(InheritWkFeed, self).required_field_not_filled(fields, vals)
        channel_id = self._context.get('channel_id')
        if channel_id:
            if channel_id.channel == 'salla':
                if 'customer_email' in res:
                    res.remove('customer_email')
                if 'invoice_email' in res:
                    res.remove('invoice_email')
                if 'invoice_partner_id' in res:
                    res.remove('invoice_partner_id')
        return res

    @api.model
    def get_product_id(self, store_product_id, line_variant_ids, channel_id, default_code=None, barcode=None):
        if channel_id.channel != 'salla':
            return super(InheritWkFeed, self).get_product_id(
                store_product_id, line_variant_ids, channel_id, default_code, barcode,
            )

        line_variant_ids = line_variant_ids or 'No Variants'
        unresolved_variant = line_variant_ids == 'SALLA_UNRESOLVED_VARIANT'
        message = ''
        match = self._get_variant_mapping(channel_id, store_product_id, line_variant_ids)
        if match:
            product_id, resolve_message = channel_id._salla_resolve_product_mapping(
                match, default_code=default_code, barcode=barcode,
            )
            message += resolve_message
            if product_id:
                return dict(product_id=product_id, message=message)

        if unresolved_variant:
            no_variant_match = self._get_variant_mapping(channel_id, store_product_id, 'No Variants')
            if no_variant_match:
                product_id, resolve_message = channel_id._salla_resolve_product_mapping(
                    no_variant_match, default_code=default_code, barcode=barcode,
                )
                message += (
                    '<br/>Salla unresolved variant fell back to No Variants mapping '
                    f'[StoreID: {store_product_id}]'
                )
                message += resolve_message
                if product_id:
                    return dict(product_id=product_id, message=message)

            product_id = channel_id._salla_find_active_product(default_code=default_code, barcode=barcode)
            if product_id:
                match = channel_id._salla_upsert_product_mappings(
                    product_id, store_product_id, 'No Variants',
                    default_code=default_code, barcode=barcode,
                )
                self = self._with_variant_mapping_in_context(match)
                message += (
                    '<br/>Salla unresolved variant repaired by SKU/barcode as No Variants '
                    f'[StoreID: {store_product_id}, ProductID: {product_id.id}]'
                )
                return dict(product_id=product_id, message=message)

        if not unresolved_variant:
            product_id = channel_id._salla_find_active_product(default_code=default_code, barcode=barcode)
            if product_id:
                match = channel_id._salla_upsert_product_mappings(
                    product_id, store_product_id, line_variant_ids,
                    default_code=default_code, barcode=barcode,
                )
                self = self._with_variant_mapping_in_context(match)
                message += (
                    '<br/>Salla product mapping repaired by SKU/barcode '
                    f'[StoreID: {store_product_id}, VariantID: {line_variant_ids}, ProductID: {product_id.id}]'
                )
                return dict(product_id=product_id, message=message)

        res = super(InheritWkFeed, self).get_product_id(
            store_product_id, line_variant_ids, channel_id, default_code, barcode,
        )
        product_id = res.get('product_id')
        message += res.get('message', '')
        if product_id:
            match = self._get_variant_mapping(channel_id, store_product_id, line_variant_ids)
            if match:
                product_id, resolve_message = channel_id._salla_resolve_product_mapping(
                    match, default_code=default_code, barcode=barcode,
                )
                message += resolve_message
            elif 'active' in product_id._fields and not product_id.active:
                product_id = channel_id._salla_unarchive_product(product_id)
                message += (
                    '<br/>Salla product was reactivated after feed evaluation '
                    f'[StoreID: {store_product_id}, ProductID: {product_id.id}]'
                )
        return dict(product_id=product_id, message=message)


class MultiChannelSale(models.Model):
    _inherit = "multi.channel.sale"

    def _salla_preferred_record(self, records):
        active = records.filtered(lambda rec: 'active' not in rec._fields or rec.active)
        record = (active or records)[:1]
        if not record:
            return record
        if record._name == 'product.product':
            self._salla_unarchive_product(record)
        elif 'active' in record._fields and not record.active:
            record.write({'active': True})
        return record

    def _salla_unarchive_product(self, product):
        if not product:
            return product
        template = product.product_tmpl_id
        if template and 'active' in template._fields and not template.active:
            template.write({'active': True})
        if 'active' in product._fields and not product.active:
            product.write({'active': True})
        return product

    def _salla_identifier_domains(self, default_code=None, barcode=None):
        domains = []
        if barcode:
            domains.append([('barcode', '=', barcode)])
        if default_code:
            domains.append([('default_code', '=', default_code)])
        return domains

    def _salla_find_active_product(self, default_code=None, barcode=None, exclude_product=False):
        Product = self.env['product.product'].with_context(active_test=False)
        for domain in self._salla_identifier_domains(default_code=default_code, barcode=barcode):
            products = Product.search(domain)
            if exclude_product:
                products = products.filtered(lambda product: product.id != exclude_product.id)
            active_products = products.filtered(lambda product: 'active' not in product._fields or product.active)
            if active_products:
                return active_products[:1]
        return self.env['product.product']

    def _salla_upsert_product_mappings(self, product, store_product_id, store_variant_id, default_code=None, barcode=None):
        mapping_vals = {
            'default_code': default_code or product.default_code,
            'barcode': barcode or product.barcode,
        }
        self.create_template_mapping(product.product_tmpl_id, store_product_id, mapping_vals.copy())
        return self.create_product_mapping(
            product.product_tmpl_id,
            product,
            store_product_id,
            store_variant_id or 'No Variants',
            mapping_vals,
        )

    def _salla_resolve_product_mapping(self, mapping, default_code=None, barcode=None):
        product = mapping.product_name
        if not product:
            return product, ''
        if 'active' not in product._fields or product.active:
            return product, ''

        default_code = default_code or product.default_code or mapping.default_code
        barcode = barcode or product.barcode or mapping.barcode
        active_product = self._salla_find_active_product(
            default_code=default_code,
            barcode=barcode,
            exclude_product=product,
        )
        if active_product:
            self._salla_upsert_product_mappings(
                active_product,
                mapping.store_product_id,
                mapping.store_variant_id,
                default_code=default_code,
                barcode=barcode,
            )
            message = (
                '<br/>Salla archived mapping remapped to active product '
                f'[StoreID: {mapping.store_product_id}, VariantID: {mapping.store_variant_id}, '
                f'OldProductID: {product.id}, NewProductID: {active_product.id}]'
            )
            _logger.info(message)
            return active_product, message

        self._salla_unarchive_product(product)
        message = (
            '<br/>Salla mapped product reactivated '
            f'[StoreID: {mapping.store_product_id}, VariantID: {mapping.store_variant_id}, ProductID: {product.id}]'
        )
        _logger.info(message)
        return product, message

    @api.model
    def match_odoo_template(self, vals, variant_lines):
        if len(self) != 1 or self.channel != 'salla':
            return super(MultiChannelSale, self).match_odoo_template(vals, variant_lines)

        Template = self.env['product.template'].with_context(active_test=False)
        record = self.env['product.template']
        barcode = vals.get('barcode')
        if barcode:
            record = self._salla_preferred_record(Template.search([('barcode', '=', barcode)]))
        if not record:
            ir_values = self.default_multi_channel_values()
            default_code = vals.get('default_code')
            if ir_values.get('avoid_duplicity') and default_code:
                record = self._salla_preferred_record(Template.search([('default_code', '=', default_code)]))
            if not record and variant_lines:
                Product = self.env['product.product'].with_context(active_test=False)
                barcode_list = variant_lines.filtered(lambda line: line.barcode).mapped('barcode')
                if barcode_list:
                    product = self._salla_preferred_record(Product.search([('barcode', 'in', barcode_list)]))
                    if product:
                        return product.product_tmpl_id
                if ir_values.get('avoid_duplicity'):
                    default_code_list = variant_lines.filtered(lambda line: line.default_code).mapped('default_code')
                    if default_code_list:
                        product = self._salla_preferred_record(Product.search([('default_code', 'in', default_code_list)]))
                        if product:
                            return product.product_tmpl_id
                for var in variant_lines:
                    match = self.match_odoo_product(var.read([])[0])
                    if match:
                        record = match.product_tmpl_id
                        break
        return record

    @api.model
    def match_odoo_product(self, vals, obj='product.product'):
        if len(self) != 1 or self.channel != 'salla':
            return super(MultiChannelSale, self).match_odoo_product(vals, obj=obj)

        oe_env = self.env[obj].with_context(active_test=False)
        record = self.env[obj]
        barcode = vals.get('barcode')
        if barcode:
            record = self._salla_preferred_record(oe_env.search([('barcode', '=', barcode)]))
        if not record:
            default_code = vals.get('default_code')
            ir_values = self.default_multi_channel_values()
            if ir_values.get('avoid_duplicity') and default_code:
                record = self._salla_preferred_record(oe_env.search([('default_code', '=', default_code)]))
            if not record and 'product_template_attribute_value_ids' in vals and 'product_tmpl_id' in vals:
                _ids = vals['product_template_attribute_value_ids'][0][2]
                ids = ','.join([str(i) for i in sorted(_ids)])
                domain = [('product_tmpl_id', '=', vals['product_tmpl_id'])]
                if ids:
                    domain += [('product_template_attribute_value_ids', 'in', _ids)]
                candidates = oe_env.search(domain).filtered(
                    lambda prod: prod.product_template_attribute_value_ids._ids2str() == ids
                )
                record = self._salla_preferred_record(candidates)
        return record

    def action_salla_product_dedup_diagnostics(self):
        self.ensure_one()
        if self.channel != 'salla':
            return self.display_message("<p>This diagnostic is only available for Salla channels.</p>")

        Product = self.env['product.product'].with_context(active_test=False)
        product_mappings = self.env['channel.product.mappings'].with_context(active_test=False).search([
            ('channel_id', '=', self.id),
        ])
        archived_mappings = product_mappings.filtered(
            lambda mapping: mapping.product_name and not mapping.product_name.active
        )
        duplicate_skus = Product.read_group(
            [('default_code', '!=', False)],
            ['default_code'],
            ['default_code'],
            lazy=False,
        )
        duplicate_skus = [
            group for group in duplicate_skus
            if (group.get('__count') or group.get('default_code_count') or 0) > 1
        ]
        sku_mapping_groups = {}
        for mapping in product_mappings:
            sku = mapping.default_code or mapping.product_name.default_code
            if sku:
                sku_mapping_groups.setdefault(sku, set()).add(mapping.product_name.id)
        split_mapping_skus = {
            sku: product_ids for sku, product_ids in sku_mapping_groups.items()
            if len(product_ids) > 1
        }
        order_ids = self.env['channel.order.mappings'].search([
            ('channel_id', '=', self.id),
        ]).mapped('order_name').ids
        archived_order_lines = self.env['sale.order.line'].with_context(active_test=False).search([
            ('order_id', 'in', order_ids),
            ('product_id.active', '=', False),
        ], limit=50)

        lines = [
            '<h3>Salla Product Dedup Diagnostics</h3>',
            f'<p>Archived product mappings: <b>{len(archived_mappings)}</b></p>',
            f'<p>Duplicate SKUs in Odoo products: <b>{len(duplicate_skus)}</b></p>',
            f'<p>SKUs mapped to multiple Odoo products: <b>{len(split_mapping_skus)}</b></p>',
            f'<p>Recent Salla order lines using archived products: <b>{len(archived_order_lines)}</b></p>',
        ]
        if archived_mappings:
            lines.append('<h4>Archived mappings sample</h4><ul>')
            for mapping in archived_mappings[:20]:
                lines.append(
                    '<li>StoreID: %s, VariantID: %s, Product: %s [%s]</li>' % (
                        escape(str(mapping.store_product_id)),
                        escape(str(mapping.store_variant_id)),
                        escape(mapping.product_name.display_name or ''),
                        mapping.product_name.id,
                    )
                )
            lines.append('</ul>')
        if split_mapping_skus:
            lines.append('<h4>Split mapping SKU sample</h4><ul>')
            for sku, product_ids in list(split_mapping_skus.items())[:20]:
                lines.append(
                    '<li>SKU: %s, Product IDs: %s</li>' % (
                        escape(str(sku)),
                        escape(', '.join(map(str, sorted(product_ids)))),
                    )
                )
            lines.append('</ul>')
        return self.display_message(''.join(lines))

class ProductVariantFeed(models.Model):
    _inherit = "product.feed"
    salla_product_attribute_options = fields.Char()


class ProductProduct(models.Model):
    _inherit = "product.template"

    # When variant is added in any order then we will require this field value
    # We create a dict to hold the variant id and the options related to that variant
    # we will match these options and assign a variant id to order during import
    # (order data has not variant id but options)
    salla_product_attribute_options = fields.Char()
