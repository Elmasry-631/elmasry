# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
{
	"name":"Sale Order Product Quantity Limit",
	"version":"19.0.0.0",
	"category":"Sales",
	"summary":"sale product quantity limit sales product limit sales order product maximum quantity limit product minimum quantity restrict product quantity limit sales order minimum product quantity max product quantity limit min product quantity limit",
	"description":"""
		
		This Odoo App helps users to restrict the sales order as per the minimum and maximum quantity limit given. User can set minimum and maximum quantity of each product, If user tries to order less than minimum quantity or more than maximum quantity, Warning will raise and not to save or confirm sales order.

	""",
    'author': 'BROWSEINFO',
    'website': 'https://www.browseinfo.com/demo-request?app=bi_so_product_quantity_limit&version=19&edition=Community',
	"depends":["base",
			   "sale",
			   "sale_management",
			  ],
	"data":[
			"views/product_template_view.xml",
			],
    'license':'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://www.browseinfo.com/demo-request?app=bi_so_product_quantity_limit&version=19&edition=Community',
    "images":['static/description/Sale-Order-Product-Quantity-Limit-Banner.gif'],
}
