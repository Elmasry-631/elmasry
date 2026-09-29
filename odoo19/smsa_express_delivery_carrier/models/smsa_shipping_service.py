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

from odoo import models, api, fields


LABEL_TYPE = [
    ('PDF', 'PDF'),
    ('ZPL', 'ZPL'),
]


class SmsaShippingService(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(
        selection_add=[('smsa', 'SMSA Express')], ondelete={'smsa': 'cascade'}
    )
    smsa_test_passkey = fields.Char(
        string="SMSA Test Passkey"
    )
    smsa_prod_passkey = fields.Char(
        string="SMSA Production Passkey"
    )
    is_cod = fields.Boolean(
        string="Is COD", default=False
    )
    smsa_service_type = fields.Many2one(
        comodel_name="delivery.smsa.service",
        string="SMSA Service Type"
    )
    smsa_return_service_type = fields.Many2one(
        comodel_name="delivery.smsa.return.service",
        string="SMSA Return Service Type"
    )
    smsa_label_type = fields.Selection(
        selection=LABEL_TYPE,
        string='SMSA Label Type',
        default='PDF',
        required=True
    )



class SMSAProductPackaging(models.Model):
    _inherit = "stock.package.type"

    package_carrier_type = fields.Selection(
        selection_add=[('smsa', 'SMSA Express')], ondelete={'smsa': 'cascade'})


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    smsa_sawb = fields.Char(string="SMSA sawb", help='SMSA Master Tracking Number')
    wk_content_description = fields.Char(string="Content Description", help="Shipment Content description")

    def get_all_wk_carriers(self):
        res = super(StockPicking, self).get_all_wk_carriers()
        res.append('smsa')
        return res

    def send_to_shipper(self):
        self.ensure_one()
        if self.carrier_id.delivery_type == 'smsa':
            # Report every missing field, packages included, in one readable message
            # before the generic checks of odoo_shipping_service_apps.
            self.carrier_id._smsa_check_shipment(self)
        return super().send_to_shipper()


class SMSAServices(models.Model):
    _name = "delivery.smsa.service"
    _description = "SMSA Service Types"

    name = fields.Char(
        string="Name"
    )
    code = fields.Char(
        string="Code"
    )


class SMSAReturnServices(models.Model):
    _name = "delivery.smsa.return.service"
    _description = "SMSA Return Service Types"


    name = fields.Char(
        string="Name"
    )
    code = fields.Char(
        string="Code"
    )
