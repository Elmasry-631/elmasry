# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
##############################################################################
from markupsafe import escape

from odoo import api, fields, models

# Slugs used when pushing status from Odoo to Salla (reverse sync).
SALLA_REVERSE_SYNC_STATE_MAP = {
    'sync_shipment': ('delivered', 'Shipment → Salla'),
    'sync_invoice': ('completed', 'Invoice paid → Salla'),
    'sync_cancel': ('canceled', 'Cancel → Salla'),
}

# Recommended mappings for Salla order import (informational).
SALLA_RECOMMENDED_ORDER_STATES = (
    'under_review', 'payment_pending', 'in_progress', 'shipped', 'delivering',
    'delivered', 'completed', 'canceled',
)

STATUS_STYLES = {
    'active': ('badge rounded-pill text-bg-success', 'Active'),
    'disabled': ('badge rounded-pill text-bg-secondary', 'Disabled'),
    'needs_config': ('badge rounded-pill text-bg-warning', 'Needs configuration'),
    'unsupported': ('badge rounded-pill text-bg-danger', 'Not supported'),
    'info': ('badge rounded-pill text-bg-primary', 'Available'),
}


class MultiChannelSaleConnectorStatus(models.Model):
    _inherit = 'multi.channel.sale'

    connector_status_html = fields.Html(
        string='Connector Status',
        compute='_compute_connector_status_html',
        sanitize=False,
    )
    connector_health_banner = fields.Char(
        string='Connector Health',
        compute='_compute_connector_status_html',
    )

    @api.depends(
        'channel', 'state', 'active', 'access_token',
        'import_order_cron', 'import_category_cron',
        'import_product_cron', 'import_partner_cron',
        'import_product_images_cron',
        'import_under_review_order_cron',
        'skip_product_images_bulk', 'skip_product_images_realtime',
        'auto_evaluate_feed', 'auto_sync_stock',
        'sync_invoice', 'sync_shipment', 'sync_cancel',
        'is_create_order_webhook', 'is_update_order_webhook',
        'order_state_ids', 'order_state_ids.channel_state',
        'import_order_date',
    )
    def _compute_connector_status_html(self):
        for channel in self:
            if channel.channel != 'salla':
                channel.connector_status_html = False
                channel.connector_health_banner = False
                continue
            lines = channel._salla_connector_feature_lines()
            channel.connector_status_html = channel._render_salla_connector_status_html(lines)
            issues = [
                line['label']
                for line in lines
                if line['status'] in ('needs_config', 'unsupported')
                and line.get('highlight')
            ]
            if issues:
                channel.connector_health_banner = (
                    '%s item(s) need attention: %s' % (len(issues), ', '.join(issues[:3]))
                )
            else:
                channel.connector_health_banner = 'All checked connector features look configured.'

    def _cron_is_active(self, xml_id):
        cron = self.env.ref(xml_id, raise_if_not_found=False)
        return bool(cron and cron.active)

    def _mapped_order_states(self):
        self.ensure_one()
        return set(self.order_state_ids.mapped('channel_state'))

    def _missing_reverse_sync_states(self):
        self.ensure_one()
        missing = []
        for field_name, (slug, label) in SALLA_REVERSE_SYNC_STATE_MAP.items():
            if self[field_name] and slug not in self._mapped_order_states():
                missing.append('%s (%s)' % (slug, label))
        return missing

    def _missing_recommended_order_states(self):
        self.ensure_one()
        mapped = self._mapped_order_states()
        return [slug for slug in SALLA_RECOMMENDED_ORDER_STATES if slug not in mapped]

    def _line(self, label, status, channel_on=None, global_on=None, notes='', highlight=True):
        style, status_label = STATUS_STYLES.get(status, STATUS_STYLES['info'])
        return {
            'label': label,
            'status': status,
            'status_label': status_label,
            'badge_class': style,
            'channel_on': channel_on,
            'global_on': global_on,
            'notes': notes,
            'highlight': highlight,
        }

    def _salla_connector_feature_lines(self):
        self.ensure_one()
        lines = []

        if self.state == 'validate' and self.access_token:
            conn_status, conn_note = 'active', 'Channel connected with access token.'
        elif self.state == 'validate':
            conn_status, conn_note = 'needs_config', 'Validated but access token is missing.'
        else:
            conn_status, conn_note = 'disabled', 'Connect the channel from the header first.'
        lines.append(self._line(
            'Salla connection',
            conn_status,
            channel_on=self.state == 'validate',
            notes=conn_note,
            highlight=conn_status != 'active',
        ))

        lines.append(self._line(
            'Manual import (orders, products, categories, customers)',
            'info',
            notes='Use Dashboard → Import on this channel.',
            highlight=False,
        ))

        order_cron_global = self._cron_is_active('odoo_multi_channel_sale.cron_import_order')
        order_status = 'disabled'
        if self.import_order_cron and order_cron_global:
            order_status = 'active'
        elif self.import_order_cron or order_cron_global:
            order_status = 'needs_config'
        order_notes = 'Imports orders from Salla into feeds.'
        if self.import_order_cron and not self.import_order_date:
            order_notes += ' Set "Orders Created After" on the Crons tab.'
        lines.append(self._line(
            'Order import cron',
            order_status,
            channel_on=self.import_order_cron,
            global_on=order_cron_global,
            notes=order_notes,
            highlight=order_status != 'active',
        ))

        under_review_cron_global = self._cron_is_active(
            'odoo_salla_integration.cron_resync_salla_under_review_orders',
        )
        under_review_status = 'disabled'
        if self.import_under_review_order_cron and under_review_cron_global:
            under_review_status = 'active'
        elif self.import_under_review_order_cron or under_review_cron_global:
            under_review_status = 'needs_config'
        lines.append(self._line(
            'Stalled order resync cron',
            under_review_status,
            channel_on=self.import_under_review_order_cron,
            global_on=under_review_cron_global,
            notes=(
                'Fallback every 2h: re-import non-invoiced non-terminal store statuses '
                'by order ID (age≥2h, max 200/run, queue rotated by last resync), '
                'forcing feed evaluation.'
            ),
            highlight=under_review_status == 'needs_config',
        ))

        if not self.is_update_order_webhook and not self.import_under_review_order_cron:
            lines.append(self._line(
                'Order status sync path',
                'needs_config',
                channel_on=False,
                notes=(
                    'Neither update webhook nor stalled-order resync is enabled; '
                    'store status changes may never reach Odoo.'
                ),
                highlight=True,
            ))

        category_cron_global = self._cron_is_active('odoo_multi_channel_sale.cron_import_category')
        category_status = 'disabled'
        if self.import_category_cron and category_cron_global:
            category_status = 'active'
        elif self.import_category_cron or category_cron_global:
            category_status = 'needs_config'
        lines.append(self._line(
            'Category import cron',
            category_status,
            channel_on=self.import_category_cron,
            global_on=category_cron_global,
            notes='Imports Salla categories into Odoo.',
            highlight=category_status != 'active',
        ))

        product_cron_global = self._cron_is_active('odoo_multi_channel_sale.cron_import_product')
        product_status = 'disabled'
        if self.import_product_cron and product_cron_global:
            product_status = 'active'
        elif self.import_product_cron or product_cron_global:
            product_status = 'needs_config'
        product_notes = (
            'Full paginated Salla product import into feeds (65/page). '
            'Turn Auto Evaluate OFF for large catalogs; use Feed Evaluation cron instead.'
        )
        lines.append(self._line(
            'Product import cron',
            product_status,
            channel_on=self.import_product_cron,
            global_on=product_cron_global,
            notes=product_notes,
            highlight=product_status != 'active',
        ))

        image_cron_global = self._cron_is_active(
            'odoo_multi_channel_sale.cron_import_product_images',
        )
        image_status = 'disabled'
        if self.import_product_images_cron and image_cron_global:
            image_status = 'active'
        elif self.import_product_images_cron or image_cron_global:
            image_status = 'needs_config'
        image_notes = 'Backfills template images from feed URLs when bulk import skipped images.'
        if self.skip_product_images_bulk:
            image_notes += ' Bulk skip-images is ON — enable this cron after feed evaluation.'
        lines.append(self._line(
            'Product image import cron',
            image_status,
            channel_on=self.import_product_images_cron,
            global_on=image_cron_global,
            notes=image_notes,
            highlight=image_status != 'active' and self.skip_product_images_bulk,
        ))

        lines.append(self._line(
            'Customer import cron',
            'unsupported',
            channel_on=False,
            global_on=self._cron_is_active('odoo_multi_channel_sale.cron_import_partner'),
            notes='Not implemented for Salla. Use manual Import → Customer or customer webhooks.',
        ))

        feed_eval_global = self._cron_is_active('odoo_multi_channel_sale.cron_evaluation')
        feed_status = 'active' if feed_eval_global else 'disabled'
        feed_notes = 'Processes pending feeds in chunks of 100 (orders, products, etc.).'
        if self.auto_evaluate_feed:
            feed_notes += ' Auto Evaluate is ON — imports evaluate inline (not recommended for thousands of products).'
        else:
            feed_notes += ' Recommended for large catalogs: keep OFF and enable global Feed Evaluation cron.'
        lines.append(self._line(
            'Feed evaluation',
            feed_status if not self.auto_evaluate_feed else 'info',
            channel_on=self.auto_evaluate_feed,
            global_on=feed_eval_global,
            notes=feed_notes,
            highlight=not self.auto_evaluate_feed and not feed_eval_global,
        ))

        lines.append(self._line(
            'Order created webhook',
            'active' if self.is_create_order_webhook else 'disabled',
            channel_on=self.is_create_order_webhook,
            notes='Realtime new orders from Salla → Odoo feeds.',
        ))
        lines.append(self._line(
            'Order updated webhook',
            'active' if self.is_update_order_webhook else 'disabled',
            channel_on=self.is_update_order_webhook,
            notes='Realtime order status updates from Salla.',
        ))
        lines.append(self._line(
            'Product webhooks',
            'info',
            notes='Configure from Webhooks tab (product create/update/delete).',
            highlight=False,
        ))

        stock_status = 'active' if self.auto_sync_stock else 'disabled'
        lines.append(self._line(
            'Stock sync (Odoo → Salla)',
            stock_status,
            channel_on=self.auto_sync_stock,
            notes='Pushes quantity when stock moves complete in mapped locations.',
        ))

        missing_reverse = self._missing_reverse_sync_states()
        for field_name, (slug, label) in SALLA_REVERSE_SYNC_STATE_MAP.items():
            enabled = self[field_name]
            if not enabled:
                lines.append(self._line(
                    label,
                    'disabled',
                    channel_on=False,
                    notes='Mapping required slug: %s' % slug,
                    highlight=False,
                ))
                continue
            if slug in self._mapped_order_states():
                rev_status = 'active'
                note = 'Order state mapping for "%s" is configured.' % slug
            else:
                rev_status = 'needs_config'
                note = 'Add channel state "%s" on Order State Mapping tab.' % slug
            lines.append(self._line(
                label,
                rev_status,
                channel_on=True,
                notes=note,
                highlight=rev_status != 'active',
            ))

        missing_recommended = self._missing_recommended_order_states()
        if missing_recommended:
            map_status = 'needs_config'
            map_note = 'Missing recommended mappings: %s.' % ', '.join(missing_recommended)
        else:
            map_status = 'active'
            map_note = 'Recommended Salla order state mappings are present.'
        if missing_reverse:
            map_note += ' Reverse sync also needs: %s.' % ', '.join(missing_reverse)
        lines.append(self._line(
            'Order state mappings',
            map_status,
            notes=map_note,
            highlight=map_status != 'active',
        ))

        return lines

    def _render_salla_connector_status_html(self, lines):
        self.ensure_one()
        rows = []
        for line in lines:
            channel_cell = '—'
            if line['channel_on'] is True:
                channel_cell = '<span class="text-success">On</span>'
            elif line['channel_on'] is False:
                channel_cell = '<span class="text-muted">Off</span>'
            global_cell = '—'
            if line['global_on'] is True:
                global_cell = '<span class="text-success">Active</span>'
            elif line['global_on'] is False:
                global_cell = '<span class="text-muted">Inactive</span>'
            rows.append(
                '<tr>'
                '<td class="align-middle"><strong>%s</strong>'
                '<div class="text-muted small">%s</div></td>'
                '<td class="align-middle"><span class="%s">%s</span></td>'
                '<td class="align-middle text-center">%s</td>'
                '<td class="align-middle text-center">%s</td>'
                '</tr>' % (
                    escape(line['label']),
                    escape(line['notes'] or ''),
                    escape(line['badge_class']),
                    escape(line['status_label']),
                    channel_cell,
                    global_cell,
                )
            )
        return (
            '<div class="o_salla_connector_status">'
            '<p class="text-muted mb-3">'
            'Overview of Salla connector capabilities on this channel. '
            '<strong>Channel</strong> = setting on this instance. '
            '<strong>Global cron</strong> = scheduled action in Odoo (Settings → Technical → Automation).'
            '</p>'
            '<table class="table table-sm table-striped table-bordered mb-0">'
            '<thead class="table-light">'
            '<tr>'
            '<th>Feature</th><th>Status</th>'
            '<th class="text-center">Channel</th>'
            '<th class="text-center">Global cron</th>'
            '</tr></thead><tbody>%s</tbody></table>'
            '<div class="alert alert-info mt-3 mb-0" role="alert">'
            '<strong>Large catalog import:</strong> Auto Evaluate OFF · Skip Product Images (Bulk) ON · '
            'Skip Product Images (Realtime) OFF · API Record Limit 65 · Feed Evaluation cron ON · '
            'Product Image cron ON after evaluation · Product import cron optional for periodic resync.'
            '</div>'
            '<p class="text-muted small mt-2 mb-0">'
            'Customer import cron is not supported on Salla (use manual import or webhooks).'
            '</p></div>'
        ) % ''.join(rows)
