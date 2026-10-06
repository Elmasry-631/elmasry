# -*- coding: utf-8 -*-
from odoo import api, models


class WkFeed(models.Model):
    _inherit = 'wk.feed'

    def required_field_not_filled(self, fields, vals):
        channel = self.env.context.get('channel_id')
        if channel is not None and getattr(channel, 'channel', False) == 'salla':
            # Salla customers can register with a mobile number only.
            fields = [field for field in fields if field != 'customer_email']
        return super().required_field_not_filled(fields, vals)

    @api.model
    def get_categ_id(self, store_categ_id, channel_id):
        res = super().get_categ_id(store_categ_id, channel_id)
        if res.get('categ_id') or channel_id.channel != 'salla' or not store_categ_id:
            return res
        # A mapping or feed may exist already without being in the batch context
        # (created earlier in the same run): resolve it before calling Salla.
        mapping = channel_id.match_category_mappings(store_category_id=str(store_categ_id))
        if mapping:
            return dict(res, categ_id=mapping.odoo_category_id, message='')
        feeds = channel_id.match_category_feeds(str(store_categ_id))
        if not feeds:
            feeds = channel_id._salla_ensure_category_feeds(store_categ_id)
        if feeds:
            ctx = dict(self.env.context)
            by_channel = {key: dict(value) for key, value in (ctx.get('category_feeds') or {}).items()}
            by_channel.setdefault(channel_id.id, {}).update({feed.store_id: feed.id for feed in feeds})
            ctx['category_feeds'] = by_channel
            res = super(WkFeed, self.with_context(**ctx)).get_categ_id(store_categ_id, channel_id)
        if not res.get('categ_id') and channel_id.default_category_id:
            # Last resort: keep the product (and its orders) importable.
            res = dict(
                res,
                categ_id=channel_id.default_category_id.id,
                message=(res.get('message') or '')
                + '<br/>Salla category %s is unknown; the channel default category was used.' % store_categ_id,
            )
        return res
