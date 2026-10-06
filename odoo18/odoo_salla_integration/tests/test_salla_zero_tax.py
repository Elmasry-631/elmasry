from odoo.addons.odoo_multi_channel_sale.tests.common import (
    TestMultiChannelCommon,
)
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class TestSallaZeroTax(TestMultiChannelCommon):

    def setUp(self):
        super().setUp()
        self.channel.channel = 'salla'
        self.zero_tax = self.env['account.tax'].create({
            'name': 'Salla test 0%',
            'amount': 0,
            'amount_type': 'percent',
            'type_tax_use': 'sale',
            'company_id': self.channel.company_id.id,
        })
        self.feed = self.env['order.feed'].create({
            'channel_id': self.channel.id,
            'store_id': 'salla-zero-tax-order',
            'name': 'salla-zero-tax-order',
        })

    def test_lines_without_tax_get_the_channel_zero_tax(self):
        self.channel.salla_zero_tax_id = self.zero_tax
        self.assertEqual(self.feed.get_taxes_ids(False), [(6, 0, self.zero_tax.ids)])
        self.assertEqual(self.feed.get_taxes_ids("[{'rate': 0}]"), [(6, 0, self.zero_tax.ids)])

    def test_lines_with_tax_are_untouched(self):
        self.channel.salla_zero_tax_id = self.zero_tax
        res = self.feed.get_taxes_ids("[{'rate': 15, 'included_in_price': False}]")
        self.assertTrue(res and res[0][2], res)
        self.assertNotIn(self.zero_tax.id, res[0][2])

    def test_without_setting_nothing_changes(self):
        self.channel.salla_zero_tax_id = False
        self.assertFalse(self.feed.get_taxes_ids(False))
        self.assertEqual(self.feed.get_taxes_ids("[{'rate': 0}]"), [(6, 0, [])])

    def test_other_channels_are_untouched(self):
        self.channel.channel = 'odoo'
        self.channel.salla_zero_tax_id = self.zero_tax
        self.assertFalse(self.feed.get_taxes_ids(False))
