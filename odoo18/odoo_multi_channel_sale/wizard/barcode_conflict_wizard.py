# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from collections import defaultdict
from logging import getLogger

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = getLogger(__name__)


ACTION_SELECTION = [
    ('skip', 'Skip (manual review)'),
    ('keep_preferred_clear_extras', 'Keep preferred product & clear barcode on extras'),
    ('clear_feed_barcode', 'Clear barcode on all feed lines'),
    ('clear_feed_keep_first', 'Clear barcode on feed duplicates (keep first)'),
    ('clear_template_barcode', 'Clear template barcode only'),
    ('normalize_hash', 'Normalize # prefix to match Odoo product'),
]

CONFLICT_TYPE_SELECTION = [
    ('odoo_duplicate', 'Duplicate barcode on Odoo products'),
    ('feed_duplicate', 'Duplicate barcode inside feed'),
    ('template_variant_share', 'Template and variant share barcode'),
    ('hash_mismatch', 'Hash prefix mismatch (#)'),
    ('mixed', 'Multiple conflict types'),
]


def _barcode_equivalents(barcode):
    """Return exact barcode plus common # / no-# equivalent."""
    if not barcode:
        return set()
    barcode = barcode.strip()
    equivalents = {barcode}
    if barcode.startswith('#'):
        stripped = barcode[1:].strip()
        if stripped:
            equivalents.add(stripped)
    else:
        equivalents.add('#' + barcode)
    return equivalents


def _format_product_barcode_state(products):
    parts = []
    for product in products:
        parts.append(
            'id=%s sku=%r barcode=%r active=%s tmpl=%s' % (
                product.id,
                product.default_code or '',
                product.barcode or '',
                product.active,
                product.product_tmpl_id.id,
            )
        )
    return '; '.join(parts) if parts else '(none)'


class BarcodeConflictWizard(models.TransientModel):
    _name = 'barcode.conflict.wizard'
    _description = 'Resolve Product Feed Barcode Conflicts'

    feed_ids = fields.Many2many(
        comodel_name='product.feed',
        relation='barcode_conflict_wizard_feed_rel',
        column1='wizard_id',
        column2='feed_id',
        string='Product Feeds',
    )
    line_ids = fields.One2many(
        comodel_name='barcode.conflict.line',
        inverse_name='wizard_id',
        string='Conflicts',
    )
    conflict_count = fields.Integer(
        string='Conflict Count',
        compute='_compute_conflict_count',
    )
    summary = fields.Html(
        string='Summary',
    )

    @api.depends('line_ids')
    def _compute_conflict_count(self):
        for wizard in self:
            wizard.conflict_count = len(wizard.line_ids)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Prefer opening an already-created wizard via create_from_feeds().
        # default_get still fills values for Action-menu opens before save.
        feeds = self._get_active_feeds()
        line_commands, summary = self._prepare_conflict_lines(feeds)
        res.update({
            'feed_ids': [(6, 0, feeds.ids)],
            'line_ids': line_commands,
            'summary': summary,
        })
        return res

    @api.model
    def create_from_feeds(self, feeds=None):
        """Create wizard + lines on the server so readonly fields are stored."""
        feeds = feeds if feeds is not None else self._get_active_feeds()
        feeds = feeds.exists()
        _logger.info(
            'Barcode conflict wizard | open | feed_ids=%s store_ids=%s states=%s',
            feeds.ids,
            feeds.mapped('store_id'),
            feeds.mapped('state'),
        )
        line_commands, summary = self._prepare_conflict_lines(feeds)
        wizard = self.create({
            'feed_ids': [(6, 0, feeds.ids)],
            'line_ids': line_commands,
            'summary': summary,
        })
        _logger.info(
            'Barcode conflict wizard | created | wizard_id=%s conflict_lines=%s',
            wizard.id,
            len(wizard.line_ids),
        )
        for line in wizard.line_ids:
            _logger.info(
                'Barcode conflict wizard | line | feed_id=%s barcode=%r type=%s '
                'action=%s preferred=%s products=%s sources=%r',
                line.feed_id.id,
                line.barcode,
                line.conflict_type,
                line.action,
                line.preferred_product_id.id if line.preferred_product_id else False,
                line.product_ids.ids,
                line.feed_source,
            )
        return wizard

    @api.model
    def action_open_wizard(self):
        """Entry point for list/form Action binding."""
        wizard = self.create_from_feeds()
        return {
            'name': _('Resolve Barcode Conflicts'),
            'type': 'ir.actions.act_window',
            'res_model': 'barcode.conflict.wizard',
            'res_id': wizard.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
        }

    @api.model
    def _get_active_feeds(self):
        active_model = self.env.context.get('active_model')
        if active_model != 'product.feed':
            return self.env['product.feed']
        feeds = self.env['product.feed'].browse(self.env.context.get('active_ids') or [])
        if not feeds and self.env.context.get('active_id'):
            feeds = self.env['product.feed'].browse(self.env.context['active_id'])
        return feeds.exists()

    @api.model
    def _prepare_conflict_lines(self, feeds):
        commands = []
        if not feeds:
            return commands, _('<p>No product feeds selected.</p>')

        for feed in feeds:
            commands.extend(self._scan_feed_conflicts(feed))

        if not commands:
            summary = _(
                '<p>No barcode conflicts detected on the selected feed(s). '
                'You can close this wizard and evaluate the feed.</p>'
            )
        else:
            summary = _(
                '<p>Found <b>%s</b> barcode conflict(s). Review the recommended '
                'actions, adjust if needed, then Apply (or Apply &amp; Evaluate).</p>'
            ) % len(commands)
        _logger.info(
            'Barcode conflict wizard | scan done | feeds=%s conflicts=%s',
            feeds.ids,
            len(commands),
        )
        return commands, summary

    @api.model
    def _scan_feed_conflicts(self, feed):
        Product = self.env['product.product'].with_context(active_test=False)
        Mapping = self.env['channel.product.mappings'].with_context(active_test=False)

        feed_sources = []
        if feed.barcode and str(feed.barcode).strip():
            feed_sources.append({
                'barcode': str(feed.barcode).strip(),
                'is_template': True,
                'variant_feed_id': False,
                'label': _('Template'),
                'sku': feed.default_code or '',
            })
        for variant in feed.feed_variants:
            if not variant.barcode or not str(variant.barcode).strip():
                continue
            feed_sources.append({
                'barcode': str(variant.barcode).strip(),
                'is_template': False,
                'variant_feed_id': variant.id,
                'label': _('Variant %s') % (
                    variant.default_code or variant.store_id or variant.id
                ),
                'sku': variant.default_code or '',
            })

        _logger.info(
            'Barcode conflict wizard | scan feed | feed_id=%s store_id=%s '
            'template_barcode=%r variant_barcodes=%s',
            feed.id,
            feed.store_id,
            feed.barcode or '',
            [
                (variant.id, variant.default_code or '', variant.barcode or '')
                for variant in feed.feed_variants if variant.barcode
            ],
        )

        by_barcode = defaultdict(list)
        for source in feed_sources:
            by_barcode[source['barcode']].append(source)

        commands = []
        consumed = set()

        for barcode, sources in by_barcode.items():
            if barcode in consumed:
                continue

            equivalents = _barcode_equivalents(barcode)
            related_sources = []
            related_barcodes = set()
            for other_barcode, other_sources in by_barcode.items():
                if other_barcode in equivalents:
                    related_sources.extend(other_sources)
                    related_barcodes.add(other_barcode)
            consumed.update(related_barcodes)

            products = Product.search([('barcode', 'in', list(equivalents))])
            conflict_types = []

            if len(products) > 1:
                conflict_types.append('odoo_duplicate')

            has_template = any(source['is_template'] for source in related_sources)
            has_variant = any(not source['is_template'] for source in related_sources)
            if has_template and has_variant:
                conflict_types.append('template_variant_share')
            elif len(related_sources) > 1:
                conflict_types.append('feed_duplicate')

            product_barcodes = {p.barcode for p in products if p.barcode}
            if products and related_barcodes and product_barcodes:
                if not (related_barcodes & product_barcodes):
                    conflict_types.append('hash_mismatch')
                elif any(
                    (pb or '').startswith('#') != barcode.startswith('#')
                    for pb in product_barcodes
                ) and barcode not in product_barcodes:
                    conflict_types.append('hash_mismatch')

            if not conflict_types:
                continue

            preferred = self._pick_preferred_product(feed, products, related_sources)
            action = self._recommend_action(conflict_types, related_sources, products)
            conflict_type = conflict_types[0] if len(conflict_types) == 1 else 'mixed'
            source_labels = '; '.join(
                '%s%s' % (
                    source['label'],
                    (' [%s]' % source['sku']) if source['sku'] else '',
                )
                for source in related_sources
            )
            product_info = '; '.join(
                '%s [%s] (id=%s, active=%s, barcode=%s)' % (
                    product.display_name,
                    product.default_code or '',
                    product.id,
                    product.active,
                    product.barcode or '',
                )
                for product in products
            ) or _('No matching Odoo products')

            mapping_count = 0
            if products and feed.channel_id:
                mapping_count = Mapping.search_count([
                    ('channel_id', '=', feed.channel_id.id),
                    ('product_name', 'in', products.ids),
                ])

            note_parts = []
            if 'odoo_duplicate' in conflict_types:
                note_parts.append(_('%s Odoo products share this barcode') % len(products))
            if 'feed_duplicate' in conflict_types:
                note_parts.append(_('%s feed lines share this barcode') % len(related_sources))
            if 'template_variant_share' in conflict_types:
                note_parts.append(_('Template and variant use the same barcode'))
            if 'hash_mismatch' in conflict_types:
                note_parts.append(_('Feed barcode form differs from Odoo (# prefix)'))
            if mapping_count:
                note_parts.append(_('%s channel mapping(s) on these products') % mapping_count)

            _logger.info(
                'Barcode conflict wizard | conflict | feed_id=%s barcode=%r '
                'equivalents=%s types=%s preferred=%s products=[%s] recommend=%s',
                feed.id,
                barcode,
                sorted(equivalents),
                conflict_types,
                preferred.id if preferred else False,
                _format_product_barcode_state(products),
                action,
            )

            commands.append((0, 0, {
                'feed_id': feed.id,
                'barcode': barcode,
                'related_barcodes': ', '.join(sorted(related_barcodes)),
                'conflict_type': conflict_type,
                'feed_source': source_labels,
                'product_ids': [(6, 0, products.ids)],
                'product_info': product_info,
                'preferred_product_id': preferred.id if preferred else False,
                'recommended_action': action,
                'action': action,
                'note': '; '.join(note_parts),
                'variant_feed_ids': [(6, 0, [
                    source['variant_feed_id']
                    for source in related_sources
                    if source['variant_feed_id']
                ])],
                'affects_template': has_template,
            }))
        return commands

    @api.model
    def _pick_preferred_product(self, feed, products, sources):
        if not products:
            return self.env['product.product']

        Mapping = self.env['channel.product.mappings'].with_context(active_test=False)
        mapped = Mapping.search([
            ('channel_id', '=', feed.channel_id.id),
            ('store_product_id', '=', feed.store_id),
            ('product_name', 'in', products.ids),
        ])
        mapped_products = mapped.mapped('product_name')
        active_mapped = mapped_products.filtered('active')
        if active_mapped:
            return active_mapped[0]
        if mapped_products:
            return mapped_products[0]

        skus = {source['sku'] for source in sources if source.get('sku')}
        if skus:
            by_sku = products.filtered(lambda product: product.default_code in skus and product.active)
            if by_sku:
                return by_sku[0]
            by_sku = products.filtered(lambda product: product.default_code in skus)
            if by_sku:
                return by_sku[0]

        active = products.filtered('active')
        return active[:1] or products[:1]

    @api.model
    def _recommend_action(self, conflict_types, sources, products):
        if 'odoo_duplicate' in conflict_types and products:
            return 'keep_preferred_clear_extras'
        if 'hash_mismatch' in conflict_types and products:
            return 'normalize_hash'
        if 'template_variant_share' in conflict_types:
            return 'clear_template_barcode'
        if 'feed_duplicate' in conflict_types:
            return 'clear_feed_keep_first'
        return 'skip'

    def _log_feed_barcode_snapshot(self, stage):
        for feed in self.feed_ids:
            _logger.info(
                'Barcode conflict wizard | %s | feed snapshot | feed_id=%s store_id=%s '
                'state=%s template_barcode=%r variants=%s',
                stage,
                feed.id,
                feed.store_id,
                feed.state,
                feed.barcode or '',
                [
                    (variant.id, variant.store_id or '', variant.default_code or '', variant.barcode or '')
                    for variant in feed.feed_variants
                ],
            )

    def _verify_barcodes_after_apply(self):
        Product = self.env['product.product'].with_context(active_test=False)
        for line in self.line_ids.filtered(lambda row: row.action != 'skip' and row.barcode):
            equivalents = list(_barcode_equivalents(line.barcode))
            live = Product.search([('barcode', 'in', equivalents)])
            _logger.info(
                'Barcode conflict wizard | verify after apply | barcode=%r equivalents=%s '
                'owners=[%s] preferred=%s',
                line.barcode,
                equivalents,
                _format_product_barcode_state(live),
                line.preferred_product_id.id if line.preferred_product_id else False,
            )
            if len(live) > 1:
                _logger.warning(
                    'Barcode conflict wizard | verify AFTER APPLY STILL DUPLICATE | '
                    'barcode=%r still on %s products: [%s]',
                    line.barcode,
                    len(live),
                    _format_product_barcode_state(live),
                )

    def action_apply(self):
        self.ensure_one()
        actionable = self.line_ids.filtered(lambda line: line.action != 'skip')
        _logger.info(
            'Barcode conflict wizard | apply start | wizard_id=%s lines=%s actionable=%s '
            'actions=%s',
            self.id,
            len(self.line_ids),
            len(actionable),
            [(line.barcode, line.action, line.preferred_product_id.id) for line in self.line_ids],
        )
        self._log_feed_barcode_snapshot('before apply')
        if not actionable and self.line_ids:
            raise UserError(_('All conflict rows are set to Skip. Choose an action first.'))
        if not self.line_ids:
            return {'type': 'ir.actions.act_window_close'}

        messages = []
        for line in actionable:
            messages.append(line._apply_action())
        self._verify_barcodes_after_apply()
        self._log_feed_barcode_snapshot('after apply')
        _logger.info(
            'Barcode conflict wizard | apply done | wizard_id=%s messages=%s',
            self.id,
            messages,
        )
        return self.env['multi.channel.sale'].display_message(
            '<p>%s</p><ul>%s</ul><p>%s</p>' % (
                _('Applied barcode conflict fixes:'),
                ''.join('<li>%s</li>' % msg for msg in messages if msg),
                _('You can now Evaluate Feed.'),
            )
        )

    def action_apply_and_evaluate(self):
        self.ensure_one()
        actionable = self.line_ids.filtered(lambda line: line.action != 'skip')
        _logger.info(
            'Barcode conflict wizard | apply+evaluate start | wizard_id=%s actionable=%s '
            'feed_ids=%s',
            self.id,
            len(actionable),
            self.feed_ids.ids,
        )
        self._log_feed_barcode_snapshot('before apply+evaluate')
        if self.line_ids and not actionable:
            raise UserError(_('All conflict rows are set to Skip. Choose an action first.'))
        for line in actionable:
            line._apply_action()
        self._verify_barcodes_after_apply()
        self._log_feed_barcode_snapshot('after apply / before evaluate')
        feeds = self.feed_ids.filtered(lambda feed: feed.state != 'done')
        if not feeds:
            _logger.warning(
                'Barcode conflict wizard | apply+evaluate | no unevaluated feeds | feed_ids=%s',
                self.feed_ids.ids,
            )
            return self.env['multi.channel.sale'].display_message(
                _('<p>Fixes applied, but no unevaluated feeds remain to evaluate.</p>')
            )
        _logger.info(
            'Barcode conflict wizard | evaluate start | feed_ids=%s states=%s',
            feeds.ids,
            feeds.mapped('state'),
        )
        return feeds.with_context(
            channel_id=feeds[:1].channel_id,
            barcode_conflict_debug=True,
        ).import_items()


class BarcodeConflictLine(models.TransientModel):
    _name = 'barcode.conflict.line'
    _description = 'Barcode Conflict Line'
    _order = 'feed_id, barcode'

    wizard_id = fields.Many2one(
        comodel_name='barcode.conflict.wizard',
        required=True,
        ondelete='cascade',
    )
    feed_id = fields.Many2one(
        comodel_name='product.feed',
        string='Feed',
        required=True,
    )
    barcode = fields.Char(string='Barcode')
    related_barcodes = fields.Char(string='Related barcodes')
    conflict_type = fields.Selection(
        selection=CONFLICT_TYPE_SELECTION,
        string='Conflict',
    )
    feed_source = fields.Char(string='Feed source')
    product_ids = fields.Many2many(
        comodel_name='product.product',
        relation='barcode_conflict_line_product_rel',
        column1='line_id',
        column2='product_id',
        string='Conflicting products',
    )
    product_info = fields.Text(string='Products')
    preferred_product_id = fields.Many2one(
        comodel_name='product.product',
        string='Preferred product',
    )
    recommended_action = fields.Selection(
        selection=ACTION_SELECTION,
        string='Recommended',
    )
    action = fields.Selection(
        selection=ACTION_SELECTION,
        string='Action',
        required=True,
        default='skip',
    )
    note = fields.Char(string='Notes')
    variant_feed_ids = fields.Many2many(
        comodel_name='product.variant.feed',
        relation='barcode_conflict_line_variant_feed_rel',
        column1='line_id',
        column2='variant_feed_id',
        string='Variant feeds',
    )
    affects_template = fields.Boolean()

    def action_open_products(self):
        self.ensure_one()
        if not self.product_ids:
            raise UserError(_('No Odoo products linked to this conflict.'))
        return {
            'name': _('Conflicting Products'),
            'type': 'ir.actions.act_window',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.product_ids.ids)],
            'target': 'current',
            'context': {'active_test': False},
        }

    def _apply_action(self):
        self.ensure_one()
        action = self.action
        _logger.info(
            'Barcode conflict wizard | apply line | feed_id=%s barcode=%r action=%s '
            'preferred=%s wizard_products=%s variant_feeds=%s affects_template=%s',
            self.feed_id.id,
            self.barcode,
            action,
            self.preferred_product_id.id if self.preferred_product_id else False,
            self.product_ids.ids,
            self.variant_feed_ids.ids,
            self.affects_template,
        )
        if action == 'skip':
            return False
        if action == 'keep_preferred_clear_extras':
            return self._clear_odoo_extras()
        if action == 'clear_feed_barcode':
            return self._clear_feed_barcodes(keep_first=False)
        if action == 'clear_feed_keep_first':
            return self._clear_feed_barcodes(keep_first=True)
        if action == 'clear_template_barcode':
            return self._clear_template_barcode()
        if action == 'normalize_hash':
            return self._normalize_hash()
        return False

    def _live_products_for_barcode(self):
        """Re-query owners at apply time; wizard M2M can be empty/stale."""
        Product = self.env['product.product'].with_context(active_test=False)
        equivalents = list(_barcode_equivalents(self.barcode))
        live = Product.search([('barcode', 'in', equivalents)])
        combined = live | self.product_ids
        _logger.info(
            'Barcode conflict wizard | live barcode owners | barcode=%r equivalents=%s '
            'wizard_ids=%s live_ids=%s combined=[%s]',
            self.barcode,
            equivalents,
            self.product_ids.ids,
            live.ids,
            _format_product_barcode_state(combined),
        )
        return combined

    def _clear_odoo_extras(self):
        preferred = self.preferred_product_id
        if not preferred:
            raise UserError(
                _('Select a preferred product for barcode %s before applying.') % self.barcode
            )
        owners = self._live_products_for_barcode()
        if preferred not in owners and owners:
            _logger.warning(
                'Barcode conflict wizard | preferred %s not in live owners %s; '
                'still keeping preferred and clearing others',
                preferred.id,
                owners.ids,
            )
        extras = owners - preferred
        if not extras and len(owners) <= 1:
            msg = _('Barcode %s: preferred product already unique.') % self.barcode
            _logger.info('Barcode conflict wizard | clear extras | %s', msg)
            return msg

        # Clear extras first so assigning the preferred barcode cannot violate uniqueness.
        Mapping = self.env['channel.product.mappings']
        if extras:
            _logger.info(
                'Barcode conflict wizard | clearing barcodes | extras=[%s]',
                _format_product_barcode_state(extras),
            )
            extras.write({'barcode': False})
            mappings = Mapping.search([
                ('channel_id', '=', self.feed_id.channel_id.id),
                ('product_name', 'in', extras.ids),
            ])
            if mappings:
                _logger.info(
                    'Barcode conflict wizard | clearing mapping barcodes | mapping_ids=%s',
                    mappings.ids,
                )
                mappings.write({'barcode': False})

        equivalents = _barcode_equivalents(self.barcode)
        before = preferred.barcode
        if not preferred.barcode or preferred.barcode in equivalents:
            preferred.barcode = self.barcode
        _logger.info(
            'Barcode conflict wizard | preferred barcode set | product_id=%s '
            'before=%r after=%r',
            preferred.id,
            before,
            preferred.barcode,
        )
        return _(
            'Barcode %s: cleared from %s product(s); kept on %s.'
        ) % (self.barcode, len(extras), preferred.display_name)

    def _clear_feed_barcodes(self, keep_first=False):
        feed = self.feed_id
        cleared = []
        kept = None
        before = {
            'template': feed.barcode,
            'variants': {
                variant.id: variant.barcode
                for variant in self.variant_feed_ids.exists()
            },
        }

        if self.affects_template and feed.barcode:
            if keep_first and kept is None:
                kept = _('template')
            else:
                feed.barcode = False
                cleared.append(_('template'))

        variants = self.variant_feed_ids.exists().sorted('id')
        for variant in variants:
            if not variant.barcode:
                continue
            if keep_first and kept is None:
                kept = variant.default_code or variant.store_id or str(variant.id)
                continue
            variant.barcode = False
            cleared.append(variant.default_code or variant.store_id or str(variant.id))

        _logger.info(
            'Barcode conflict wizard | clear feed barcodes | feed_id=%s barcode=%r '
            'keep_first=%s before=%s cleared=%s kept=%s template_after=%r',
            feed.id,
            self.barcode,
            keep_first,
            before,
            cleared,
            kept,
            feed.barcode or '',
        )
        if not cleared:
            return _('Barcode %s: nothing to clear on feed.') % self.barcode
        msg = _('Barcode %s: cleared on feed line(s) %s.') % (self.barcode, ', '.join(cleared))
        if kept:
            msg += _(' Kept on %s.') % kept
        return msg

    def _clear_template_barcode(self):
        feed = self.feed_id
        before = feed.barcode
        if not feed.barcode:
            return _('Barcode %s: template already empty.') % self.barcode
        feed.barcode = False
        _logger.info(
            'Barcode conflict wizard | clear template barcode | feed_id=%s before=%r after=%r',
            feed.id,
            before,
            feed.barcode or '',
        )
        return _('Barcode %s: cleared from template feed.') % self.barcode

    def _normalize_hash(self):
        feed = self.feed_id
        target = None
        preferred = self.preferred_product_id
        if preferred and preferred.barcode:
            target = preferred.barcode
        elif self.product_ids:
            with_barcode = self.product_ids.filtered('barcode')
            if with_barcode:
                target = with_barcode[0].barcode
        if not target:
            # Fall back to stripping a leading # from the feed barcode.
            target = self.barcode[1:] if self.barcode.startswith('#') else self.barcode

        changed = []
        before = {
            'template': feed.barcode,
            'variants': {
                variant.id: variant.barcode
                for variant in self.variant_feed_ids.exists()
            },
        }
        if self.affects_template and feed.barcode and feed.barcode != target:
            feed.barcode = target
            changed.append(_('template'))
        for variant in self.variant_feed_ids.exists():
            if variant.barcode and variant.barcode != target:
                variant.barcode = target
                changed.append(variant.default_code or variant.store_id or str(variant.id))

        _logger.info(
            'Barcode conflict wizard | normalize hash | feed_id=%s from=%r to=%r '
            'before=%s changed=%s',
            feed.id,
            self.barcode,
            target,
            before,
            changed,
        )
        if not changed:
            return _('Barcode %s: feed already normalized to %s.') % (self.barcode, target)
        return _('Barcode %s: normalized feed line(s) %s → %s.') % (
            self.barcode, ', '.join(changed), target,
        )
