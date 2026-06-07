{
    "name": "POS Receipt: Price Before Discount",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Show product list price (before discount) under each receipt line when discounted",
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_receipt_price_before_discount/static/src/js/price_before_discount.js",
            "pos_receipt_price_before_discount/static/src/xml/receipt_price_before_discount.xml",
        ]
    },
    "license": "LGPL-3",
    "installable": True,
    "application": False,
}
