# -*- coding: utf-8 -*-
import base64
import json
from unittest.mock import patch

import requests

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

REQUESTS_POST = 'odoo.addons.smsa_express_delivery_carrier.models.smsa_delivery_carrier.requests.post'


class FakeResponse:

    def __init__(self, status_code, payload, content_type='application/json; charset=utf-8'):
        self.status_code = status_code
        self.headers = {'Content-Type': content_type}
        self._payload = payload
        self.text = json.dumps(payload)

    def json(self):
        return self._payload


def smsa_success(awb='290000000001', with_file=True):
    waybill = {'awb': awb}
    if with_file:
        waybill['awbFile'] = base64.b64encode(b'%PDF-1.4 label').decode()
    return FakeResponse(200, {'sawb': awb, 'waybills': [waybill]})


@tagged('post_install', '-at_install')
class TestSmsaShipping(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        saudi_arabia = cls.env.ref('base.sa')
        cls.warehouse = cls.env['stock.warehouse'].search([('company_id', '=', cls.env.company.id)], limit=1)
        cls.warehouse.partner_id.write({
            'street': 'King Fahd Rd 1', 'city': 'Riyadh', 'country_id': saudi_arabia.id, 'phone': '0110000000',
        })
        cls.carrier = cls.env.ref('smsa_express_delivery_carrier.smsa_express_delivery_carrier')
        cls.carrier.write({'smsa_test_passkey': 'test-key', 'prod_environment': False, 'is_cod': False})
        cls.customer = cls.env['res.partner'].create({
            'name': 'SMSA Customer', 'street': 'Olaya St 5', 'city': 'Riyadh',
            'country_id': saudi_arabia.id, 'phone': '+966 50 000 0000',
        })
        cls.book = cls.env['product.product'].create({
            'name': 'Paper Book', 'type': 'consu', 'is_storable': True, 'weight': 0.5, 'list_price': 80,
        })
        cls.env['stock.quant'].with_context(inventory_mode=True).create({
            'product_id': cls.book.id, 'location_id': cls.warehouse.lot_stock_id.id, 'inventory_quantity': 20,
        }).action_apply_inventory()

    def _create_delivery(self, pack=True):
        order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'order_line': [(0, 0, {'product_id': self.book.id, 'product_uom_qty': 2})],
        })
        order.set_delivery_line(self.carrier, 25.0)
        order.action_confirm()
        picking = order.picking_ids
        if pack:
            picking.move_line_ids._put_in_pack().shipping_weight = 1.0
        return picking

    def test_payload_has_every_field_smsa_requires(self):
        picking = self._create_delivery()
        payload = self.carrier._smsa_prepare_shipment(picking)
        self.assertEqual(payload['CODAmount'], 0.0)
        self.assertEqual(payload['ContentDescription'], 'Paper Book')
        self.assertEqual(payload['Parcels'], 1)
        self.assertEqual(payload['Weight'], 1.0)
        self.assertEqual(payload['WeightUnit'], 'KG')
        self.assertEqual(payload['ServiceCode'], 'EDDL')
        self.assertEqual(payload['DeclaredValue'], picking.sale_id.amount_total)
        self.assertEqual(payload['ConsigneeAddress']['ContactPhoneNumber'], '+966500000000')

    def test_cash_on_delivery_collects_the_unpaid_amount(self):
        self.carrier.is_cod = True
        picking = self._create_delivery()
        payload = self.carrier._smsa_prepare_shipment(picking)
        self.assertEqual(payload['CODAmount'], picking.sale_id.amount_total)

    def test_send_to_shipper_creates_the_waybill(self):
        picking = self._create_delivery()
        with patch(REQUESTS_POST, return_value=smsa_success()) as post:
            picking.send_to_shipper()
        post.assert_called_once()
        self.assertEqual(picking.carrier_tracking_ref, '290000000001')
        self.assertTrue(picking.label_genrated)
        self.assertEqual(picking.smsa_sawb, '290000000001')
        self.assertEqual(picking.wk_content_description, 'Paper Book')
        label = self.env['ir.attachment'].search([
            ('res_model', '=', 'stock.picking'), ('res_id', '=', picking.id), ('name', '=', 'SMSA_290000000001.pdf'),
        ])
        self.assertTrue(label)

    def test_waybill_without_file_keeps_the_tracking_number(self):
        picking = self._create_delivery()
        with patch(REQUESTS_POST, return_value=smsa_success(with_file=False)):
            picking.send_to_shipper()
        self.assertEqual(picking.carrier_tracking_ref, '290000000001')

    def test_missing_data_is_reported_at_once_before_calling_smsa(self):
        picking = self._create_delivery(pack=False)
        self.customer.write({'phone': False, 'city': 'Ri'})
        with patch(REQUESTS_POST) as post, self.assertRaises(UserError) as error:
            picking.send_to_shipper()
        post.assert_not_called()
        message = str(error.exception)
        self.assertIn('the phone number is missing', message)
        self.assertIn('the city must be between 3 and 50 characters', message)
        self.assertIn('Put the products in a package', message)

    def test_missing_passkey(self):
        self.carrier.smsa_test_passkey = False
        picking = self._create_delivery()
        with self.assertRaisesRegex(UserError, 'the SMSA Test passkey is missing'):
            picking.send_to_shipper()

    def test_smsa_validation_errors_are_readable(self):
        picking = self._create_delivery()
        response = FakeResponse(400, {
            'title': 'One or more validation errors occurred.',
            'errors': {
                'ConsigneeAddress.City': ['City length between 3 and 50 characters'],
                'CODAmount': ['COD Amount value is required'],
            },
        }, 'application/problem+json; charset=utf-8')
        with patch(REQUESTS_POST, return_value=response), self.assertRaises(UserError) as error:
            picking.send_to_shipper()
        message = str(error.exception)
        self.assertIn('SMSA cannot create the waybill for %s' % picking.name, message)
        self.assertIn('Customer address - City: City length between 3 and 50 characters', message)
        self.assertIn('Cash on delivery amount: COD Amount value is required', message)

    def test_rejected_passkey(self):
        picking = self._create_delivery()
        response = FakeResponse(401, {'title': 'Unauthorized', 'status': 401}, 'application/problem+json')
        with patch(REQUESTS_POST, return_value=response), \
                self.assertRaisesRegex(UserError, 'SMSA rejected the Test passkey'):
            picking.send_to_shipper()

    def test_service_down_and_timeout(self):
        picking = self._create_delivery()
        with patch(REQUESTS_POST, return_value=FakeResponse(503, {})), \
                self.assertRaisesRegex(UserError, 'not available right now'):
            picking.send_to_shipper()
        with patch(REQUESTS_POST, side_effect=requests.Timeout()), \
                self.assertRaisesRegex(UserError, 'did not answer'):
            picking.send_to_shipper()
        with patch(REQUESTS_POST, side_effect=requests.ConnectionError()), \
                self.assertRaisesRegex(UserError, 'Could not connect to SMSA'):
            picking.send_to_shipper()

    def test_package_type_search(self):
        package_type = self.env.ref('smsa_express_delivery_carrier.packaging_smsa_express')
        found = self.env['stock.package.type'].name_search('SMSA Custom')
        self.assertIn(package_type.id, [record_id for record_id, _name in found])
