# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

import base64
import json
import logging
import re

import requests

from odoo import api, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


prod_base_url = "https://ecomapis.smsaexpress.com"  # Production Environment
test_base_url = "https://ecomapis-sandbox.azurewebsites.net"  # Sandbox Environment
SMSA_TIMEOUT = 30

# Limits enforced by the SMSA ecom API validation (checked against the API on 2026-09-28).
SMSA_NAME_LENGTH = (2, 200)
SMSA_CITY_LENGTH = (3, 50)
SMSA_ORDER_NUMBER_MAX = 50
SMSA_MIN_DECLARED_VALUE = 0.1
SMSA_CONTENT_DESCRIPTION_MAX = 100
SMSA_WEIGHT_UNITS = ('KG', 'LB')
PHONE_SEPARATORS = re.compile(r'[\s().-]')
PHONE_PATTERN = re.compile(r'^\+?\d{7,15}$')


class SmsaExpressAPI():
    """Thin HTTP client: the carrier builds the payload and turns failures into messages."""

    def __init__(self, *args, **kwargs):
        self.prod_environment = kwargs.get('prod_environment')
        self.smsa_passkey = kwargs.get('smsa_passkey')

    def _request_header(self):
        return {
            "apikey": self.smsa_passkey,
            "Content-Type": "application/json"
        }

    def _smsa_send_request(self, request_body, path):
        """Return a dict with `success` and either `root` (the response) or `error_type`."""
        api_end = prod_base_url if self.prod_environment else test_base_url
        order_number = request_body.get('OrderNumber')
        # Never log the headers: they carry the API key.
        _logger.info("SMSA request %s for %s", path, order_number)
        _logger.debug("SMSA request body: %s", request_body)
        try:
            response = requests.post(
                url=api_end + path, data=json.dumps(request_body),
                headers=self._request_header(), timeout=SMSA_TIMEOUT)
        except requests.Timeout:
            _logger.warning("SMSA request %s for %s timed out", path, order_number)
            return dict(success=False, error_type='timeout')
        except requests.RequestException as error:
            _logger.warning("SMSA request %s for %s failed: %s", path, order_number, error)
            return dict(success=False, error_type='connection')
        _logger.info("SMSA response %s for %s", response.status_code, order_number)
        _logger.debug("SMSA response body: %s", response.text)
        return dict(success=200 <= response.status_code < 300, error_type='http', root=response)


class SmsaDeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    @api.model
    def smsa_rate_shipment(self, order):
        return {
            'success': True,
            'price': self.fixed_price,
            'error_message': False,
            'warning_message': False,
        }

    def _compute_can_generate_return(self):
        for carrier in self:
            carrier.can_generate_return = True

    # ------------------------------------------------------------------
    # Data sent to SMSA
    # ------------------------------------------------------------------

    def _smsa_passkey(self):
        return self.smsa_prod_passkey if self.prod_environment else self.smsa_test_passkey

    @api.model
    def _smsa_partner_value(self, partner, field_name):
        """Delivery addresses often leave name or phone to their parent contact."""
        return (partner[field_name] or partner.parent_id[field_name] or '').strip()

    @api.model
    def _smsa_clean_phone(self, phone):
        return PHONE_SEPARATORS.sub('', phone or '')

    def _smsa_address(self, partner):
        return {
            "ContactName": self._smsa_partner_value(partner, 'name')[:SMSA_NAME_LENGTH[1]],
            "ContactPhoneNumber": self._smsa_clean_phone(self._smsa_partner_value(partner, 'phone')),
            "Country": partner.country_id.code or "",
            "City": (partner.city or "").strip(),
            "AddressLine1": (partner.street or "").strip(),
            "AddressLine2": (partner.street2 or "").strip(),
        }

    def _smsa_warehouse_partner(self, picking):
        return picking.picking_type_id.warehouse_id.partner_id

    def _smsa_content_description(self, picking):
        description = (picking.wk_content_description or "").strip()
        if not description:
            description = ", ".join(picking.move_ids.product_id.mapped('name'))
        return description[:SMSA_CONTENT_DESCRIPTION_MAX]

    def _smsa_parcels_and_weight(self, picking, is_return=False):
        packages = picking.move_line_ids.result_package_id
        weight = sum(packages.mapped('shipping_weight'))
        if is_return and not packages:
            # Return pickings are rarely packed: one parcel weighing what the products weigh.
            weight = sum(move.product_uom_qty * move.product_id.weight for move in picking.move_ids)
            return 1, weight or self.default_product_weight
        return len(packages), weight

    def _smsa_get_declared_value(self, picking):
        order = picking.sale_id
        if order:
            return order.amount_total
        return sum(line.quantity * line.product_id.lst_price for line in picking.move_line_ids)

    def _smsa_get_cod_amount(self, picking):
        """What the courier must collect: nothing unless the order is cash on delivery,
        and never the part already paid online."""
        order = picking.sale_id
        if not order:
            return self._smsa_get_declared_value(picking) if self.is_cod else 0.0
        # sudo: payment transactions are only readable by administrators, and the amount
        # must be right whoever validates the delivery. Read-only.
        order_sudo = order.sudo()
        cash_on_delivery = self.is_cod or any(
            'custom_mode' in tx.provider_id._fields and tx.provider_id.custom_mode == 'cash_on_delivery'
            for tx in order_sudo.transaction_ids
        )
        if not cash_on_delivery:
            return 0.0
        return max(order.currency_id.round(order.amount_total - order_sudo.amount_paid), 0.0)

    def _smsa_prepare_shipment(self, picking, is_return=False):
        customer_address = self._smsa_address(picking.partner_id)
        warehouse_address = self._smsa_address(self._smsa_warehouse_partner(picking))
        parcels, weight = self._smsa_parcels_and_weight(picking, is_return=is_return)
        service = self.smsa_return_service_type if is_return else self.smsa_service_type
        payload = {
            "PickupAddress" if is_return else "ConsigneeAddress": customer_address,
            "ReturnToAddress" if is_return else "ShipperAddress": warehouse_address,
            "OrderNumber": (picking.name or "")[:SMSA_ORDER_NUMBER_MAX],
            "Parcels": parcels,
            "ShipDate": picking.scheduled_date.strftime('%Y-%m-%dT%H:%M:%S'),
            "ShipmentCurrency": self.get_shipment_currency_id(pickings=picking).name,
            "WaybillType": self.smsa_label_type,
            "Weight": weight,
            "WeightUnit": self.delivery_uom,
            "ContentDescription": self._smsa_content_description(picking),
            "ServiceCode": service.code,
            "DeclaredValue": self._smsa_get_declared_value(picking),
        }
        if not is_return:
            # Required by SMSA even when nothing is collected.
            payload["CODAmount"] = self._smsa_get_cod_amount(picking)
        return payload

    # ------------------------------------------------------------------
    # Checks and readable messages
    # ------------------------------------------------------------------

    def _smsa_error_message(self, picking, lines, is_return=False):
        if is_return:
            title = self.env._("SMSA cannot create the return waybill for %(picking)s:", picking=picking.name)
        else:
            title = self.env._("SMSA cannot create the waybill for %(picking)s:", picking=picking.name)
        return "\n".join([title] + ["• " + line for line in lines])

    def _smsa_check_partner(self, partner, who, errors):
        if not self._smsa_partner_value(partner, 'name'):
            errors.append(self.env._("%(who)s: the name is missing.", who=who))
        phone = self._smsa_clean_phone(self._smsa_partner_value(partner, 'phone'))
        if not phone:
            errors.append(self.env._("%(who)s: the phone number is missing.", who=who))
        elif not PHONE_PATTERN.match(phone):
            errors.append(self.env._(
                "%(who)s: the phone number %(phone)s is not valid.",
                who=who, phone=self._smsa_partner_value(partner, 'phone'),
            ))
        if not (partner.street or "").strip():
            errors.append(self.env._("%(who)s: the street address is missing.", who=who))
        city = (partner.city or "").strip()
        if not city:
            errors.append(self.env._("%(who)s: the city is missing.", who=who))
        elif not SMSA_CITY_LENGTH[0] <= len(city) <= SMSA_CITY_LENGTH[1]:
            errors.append(self.env._("%(who)s: the city must be between 3 and 50 characters.", who=who))
        if not partner.country_id:
            errors.append(self.env._("%(who)s: the country is missing.", who=who))

    def _smsa_check_shipment(self, picking, is_return=False):
        """Check everything SMSA requires before calling it, and report all problems at once."""
        errors = []
        environment = self.env._("Production") if self.prod_environment else self.env._("Test")
        if not self._smsa_passkey():
            errors.append(self.env._(
                "Delivery method %(carrier)s: the SMSA %(environment)s passkey is missing.",
                carrier=self.name, environment=environment,
            ))
        service = self.smsa_return_service_type if is_return else self.smsa_service_type
        if not service.code:
            errors.append(self.env._(
                "Delivery method %(carrier)s: the SMSA service type is missing.", carrier=self.name))
        if self.delivery_uom not in SMSA_WEIGHT_UNITS:
            errors.append(self.env._(
                "Delivery method %(carrier)s: the weight unit must be KG or LB.", carrier=self.name))

        warehouse = picking.picking_type_id.warehouse_id
        warehouse_partner = self._smsa_warehouse_partner(picking)
        if not warehouse_partner:
            errors.append(self.env._(
                "Warehouse %(warehouse)s has no address. Set it in Inventory > Configuration > Warehouses.",
                warehouse=warehouse.name or "",
            ))
        else:
            self._smsa_check_partner(
                warehouse_partner, self.env._("Warehouse %(name)s", name=warehouse.name), errors)
        if not picking.partner_id:
            errors.append(self.env._("The delivery has no customer address."))
        else:
            self._smsa_check_partner(
                picking.partner_id, self.env._("Customer %(name)s", name=picking.partner_id.display_name), errors)

        packages = picking.move_line_ids.result_package_id
        if not is_return:
            if not packages:
                errors.append(self.env._(
                    "Put the products in a package (Put in Pack in the Operations tab) and enter its weight."))
            for package in packages.filtered(lambda package: package.shipping_weight <= 0):
                errors.append(self.env._(
                    "Package %(package)s: the shipping weight is missing.", package=package.name))
        if self._smsa_get_declared_value(picking) < SMSA_MIN_DECLARED_VALUE:
            errors.append(self.env._("The declared value of the shipment must be at least 0.1."))
        if errors:
            raise UserError(self._smsa_error_message(picking, errors, is_return=is_return))

    def _smsa_field_labels(self):
        return {
            'ConsigneeAddress': self.env._("Customer address"),
            'PickupAddress': self.env._("Customer address"),
            'ShipperAddress': self.env._("Warehouse address"),
            'ReturnToAddress': self.env._("Warehouse address"),
            'ContactName': self.env._("Name"),
            'ContactPhoneNumber': self.env._("Phone"),
            'City': self.env._("City"),
            'Country': self.env._("Country"),
            'AddressLine1': self.env._("Street"),
            'AddressLine2': self.env._("Street 2"),
            'Weight': self.env._("Weight"),
            'Parcels': self.env._("Number of packages"),
            'CODAmount': self.env._("Cash on delivery amount"),
            'DeclaredValue': self.env._("Declared value"),
            'ContentDescription': self.env._("Content description"),
            'ShipmentCurrency': self.env._("Currency"),
            'WeightUnit': self.env._("Weight unit"),
            'OrderNumber': self.env._("Order number"),
            'ShipDate': self.env._("Shipping date"),
            'ServiceCode': self.env._("Service type"),
            'WaybillType': self.env._("Label type"),
        }

    @api.model
    def _smsa_response_json(self, response):
        try:
            return response.json()
        except ValueError:
            return None

    def _smsa_api_error(self, picking, result, is_return=False):
        """Turn a failed SMSA call into a message people can act on."""
        error_type = result.get('error_type')
        if error_type == 'timeout':
            lines = [self.env._(
                "SMSA did not answer within %(seconds)s seconds. Please try again.", seconds=SMSA_TIMEOUT)]
        elif error_type == 'connection':
            lines = [self.env._(
                "Could not connect to SMSA. Check the server's internet connection and try again.")]
        else:
            response = result['root']
            status = response.status_code
            data = self._smsa_response_json(response)
            errors = data.get('errors') if isinstance(data, dict) else None
            if status in (401, 403):
                environment = self.env._("Production") if self.prod_environment else self.env._("Test")
                lines = [self.env._(
                    "SMSA rejected the %(environment)s passkey of delivery method %(carrier)s. "
                    "Check the passkey, and that Production Environment matches the kind of key.",
                    environment=environment, carrier=self.name,
                )]
            elif status >= 500:
                lines = [self.env._(
                    "The SMSA service is not available right now (HTTP %(status)s). Please try again later.",
                    status=status,
                )]
            elif isinstance(errors, dict) and errors:
                labels = self._smsa_field_labels()
                lines = []
                for key, messages in errors.items():
                    label = " - ".join(labels.get(part, part) for part in str(key).split('.'))
                    messages = messages if isinstance(messages, list) else [messages]
                    lines.append("%s: %s" % (label, " ".join(str(message) for message in messages)))
            else:
                detail = ""
                if isinstance(data, dict):
                    detail = data.get('message') or data.get('title') or ""
                elif isinstance(errors, list):
                    detail = " ".join(str(error) for error in errors)
                detail = detail or (response.text or "")[:300]
                lines = [self.env._(
                    "SMSA returned an error (HTTP %(status)s): %(detail)s", status=status, detail=detail)]
        return UserError(self._smsa_error_message(picking, lines, is_return=is_return))

    # ------------------------------------------------------------------
    # Shipment, return label, tracking
    # ------------------------------------------------------------------

    def _smsa_create_shipment(self, picking, is_return=False):
        """Validate, call SMSA and return the delivery.carrier result dict."""
        self._smsa_check_shipment(picking, is_return=is_return)
        payload = self._smsa_prepare_shipment(picking, is_return=is_return)
        api = SmsaExpressAPI(prod_environment=self.prod_environment, smsa_passkey=self._smsa_passkey())
        response = api._smsa_send_request(payload, path="/api/c2b/new" if is_return else "/api/shipment/b2c/new")
        if not response.get('success'):
            raise self._smsa_api_error(picking, response, is_return=is_return)

        data = self._smsa_response_json(response['root'])
        if not isinstance(data, dict):
            raise UserError(self._smsa_error_message(
                picking, [self.env._("SMSA sent an answer that could not be read.")], is_return=is_return))

        # From here on the shipment exists at SMSA: never fail, or Odoo would forget it.
        picking.smsa_sawb = data.get('sawb')
        if not picking.wk_content_description:
            picking.wk_content_description = payload['ContentDescription']
        file_ext = self.smsa_label_type
        tracking_numbers, attachments = [], []
        for item in data.get('waybills') or []:
            awb = item.get('awb')
            if awb:
                tracking_numbers.append(str(awb))
            label = item.get('awbFile')
            if label:
                label_data = base64.b64decode(label) if file_ext == "PDF" else label.encode('utf-8')
                attachments.append(('SMSA_%s.%s' % (awb or data.get('sawb'), file_ext.lower()), label_data))
        if not tracking_numbers and data.get('sawb'):
            tracking_numbers.append(str(data['sawb']))
        if not attachments:
            picking.message_post(body=self.env._(
                "SMSA created shipment %(reference)s but did not send the waybill file. "
                "Download it from the SMSA portal.", reference=", ".join(tracking_numbers) or "-"))
        return {'exact_price': 0, 'weight': 0, "date_delivery": None,
                'tracking_number': ",".join(tracking_numbers), 'attachments': attachments}

    @api.model
    def smsa_send_shipping(self, pickings):
        return self._smsa_create_shipment(pickings)

    @api.model
    def smsa_cancel_shipment(self, pickings):
        raise UserError(self.env._(
            "SMSA shipments cannot be cancelled from Odoo. Cancel the shipment on the SMSA portal."))

    @api.model
    def smsa_get_tracking_link(self, pickings):
        for obj in self:
            base_tracking_link = 'https://www.smsaexpress.com/trackingdetails?'
            tracking_numbers = pickings.carrier_tracking_ref.split(',')
            query_params = '&'.join(
                [f'tracknumbers%5B{i}%5D={num}' for i, num in enumerate(tracking_numbers)]
            )
            smsa_tracking_link = base_tracking_link + query_params
            return smsa_tracking_link

    @api.model
    def smsa_get_return_label(self, pickings, tracking_number, origin_date):
        result = self._smsa_create_shipment(pickings, is_return=True)

        pickings.carrier_tracking_ref = result.get(
            'tracking_number') and result.get('tracking_number').strip(',')
        pickings.label_genrated = True
        pickings.date_delivery = result.get('date_delivery')
        pickings.weight_shipment = float(result.get('weight'))
        msg = self.env._(
            "Return shipment sent to carrier %(carrier)s with tracking number %(reference)s",
            carrier=pickings.carrier_id.name, reference=pickings.carrier_tracking_ref,
        )

        my_attachments_ids = []

        for i in range(len(result['attachments'])):
            my_attachment = self.env['ir.attachment'].create({
                'datas': base64.b64encode(result['attachments'][i][1]),
                'name': self.get_return_label_prefix() + "-stock_picking_id-" + str(pickings.id),
                'res_model': 'stock.picking',
                'res_id': pickings.id
            })
            my_attachments_ids.append(my_attachment.id)

        pickings.return_label_ids = my_attachments_ids
        pickings.message_post(
            body=msg,
            subject="Attachments of tracking",
            attachment_ids=my_attachments_ids
        )
