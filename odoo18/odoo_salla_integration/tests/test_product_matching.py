from odoo.addons.odoo_multi_channel_sale.tests.common import (
    TestMultiChannelCommon,
)
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestSallaProductMatching(TestMultiChannelCommon):

    def setUp(self):
        super().setUp()
        self.channel.channel = 'salla'

    def _archived_duplicate(self):
        template = self.env['product.template'].create({
            'name': 'Salla combination owner',
            'default_code': 'SALLA-ACTIVE-COMBINATION',
            'type': 'consu',
            'is_storable': True,
        })
        active_product = template.product_variant_id
        archived_product = self.env['product.product'].with_context(
            channel='salla',
        ).create({
            'product_tmpl_id': template.id,
            'active': False,
            'default_code': 'SALLA-ARCHIVED-COMBINATION',
            'barcode': 'SALLA-ARCHIVED-BARCODE',
        })
        return template, active_product, archived_product

    def test_matching_archived_product_has_no_side_effect(self):
        _template, _active_product, archived_product = (
            self._archived_duplicate()
        )

        matched = self.channel.match_odoo_product({
            'barcode': archived_product.barcode,
        })
        self.env.flush_all()

        self.assertEqual(matched, archived_product)
        self.assertFalse(
            archived_product.active,
            msg='Looking up a product must not reactivate it',
        )

    def test_evaluate_rejects_archived_duplicate_combination_cleanly(self):
        template, active_product, archived_product = (
            self._archived_duplicate()
        )
        feed = self.env['product.feed'].create({
            'channel_id': self.channel.id,
            'name': 'Salla archived collision feed',
            'store_id': 'salla-archived-collision',
        })
        variant = self.env['product.variant.feed'].create({
            'feed_templ_id': feed.id,
            'store_id': 'salla-archived-collision-variant',
            'name_value': '[]',
            'default_code': archived_product.default_code,
            'barcode': archived_product.barcode,
        })

        result = feed._safe_evaluate(
            lambda: feed._create_product_line(
                variant,
                template,
                feed.store_id,
                self.channel.location_id,
                self.channel,
            )
        )
        self.env.flush_all()

        self.assertEqual(result['state'], 'error')
        self.assertIn('Cannot reactivate', result['message'])
        self.assertTrue(active_product.active)
        self.assertFalse(archived_product.active)
