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

{
    'name':       "SMSA Express Shipping Integration",
    'summary':      """The module allows the user to Integrate SMSA Web Services with Client Application (SECOM) with Odoo. Once integrated, the shipping method can be used on Odoo website by customers to get their orders delivered and in the Odoo backend by the user.
                    SMSA | SMSA Express | SMSA Express Odoo integration | SMSA shipping | SMSA tracking | SMSA lable generation |
                    SMSA Express API integration | SMSA shipping solution | SMSA Express Odoo | SMSA API | Odoo SMSA module |
                    SMSA Odoo | SMSA integration | Shipping | Delivery | Shipping integration | Smsa shipping extension.
                """,
    'description':  """
                    This is SMSA Express Shipping Integration.
                """,
    'live_test_url':  'https://odoodemo.webkul.in/?module=smsa_express_delivery_carrier',
    'author':       "Webkul Software Pvt. Ltd.",
    'website':       "https://store.webkul.com/smsa-express-shipping-integration.html",
    "license":       "Other proprietary",
    'category':       'Warehouse',
    'version':       '1.0.3',
    'depends':       ['odoo_shipping_service_apps'],
    'data':       [
        'security/ir.model.access.csv',
        'views/smsa_shipping_service.xml',
        'data/data.xml',
        'data/delivery_demo.xml',
    ],
    'images':       ['static/description/Banner.png'],
    'application':       True,
    'installable':       True,
    "price":  149,
    'currency':       'USD',
    'pre_init_hook':       'pre_init_check',
}
