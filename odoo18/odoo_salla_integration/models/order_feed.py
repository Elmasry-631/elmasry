# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from logging import getLogger

from odoo import models

_logger = getLogger(__name__)


class OrderFeed(models.Model):
    _inherit = 'order.feed'

    def import_order(self, channel_id):
        """Evaluate one order feed without aborting the whole import.

        The base implementation lets a single failing order raise out of
        ``import_items()``, which rolls back the entire page and forces the
        import to restart from the beginning. Here the error is logged, the
        feed is marked as failed and the import keeps going.
        """
        if channel_id.channel != 'salla':
            return super().import_order(channel_id)
        try:
            return super().import_order(channel_id)
        except Exception as e:
            _logger.exception(
                'Salla order feed %s evaluation failed; marking feed as error '
                'and continuing the import.',
                self.id,
            )
            message = '<br/>%s' % (e)
            try:
                self.write({
                    'state': 'error',
                    'message': message,
                })
            except Exception:
                _logger.exception(
                    'Salla order feed %s: failed to mark the feed as error.',
                    self.id,
                )
            return dict(
                create_id=False,
                update_id=False,
                message=message,
            )
