{
    'name': 'Sale Payment Gateway',
    "version": "19.0.1.2.0",
    'summary': 'Payment Gateway on Sales/Invoice/Delivery + auto-sync Receivable & Payable accounts from gateway to partner',
    'description': """
Sale Payment Gateway
====================

Adds a Payment Gateway master record (`sale.payment.gateway`) and
propagates the selected gateway from a Sales Order to its Invoice and
Delivery (stock.picking).

Each payment gateway can be configured with default Receivable and
Payable accounts (`property_account_receivable_id` and
`property_account_payable_id`).

Partner-side auto-sync
----------------------
On the partner form, a new `payment_gateway_id` field is added in the
Accounting group. Selecting a gateway **automatically fills** the
partner's `property_account_receivable_id` and
`property_account_payable_id` from the gateway defaults.

The two account fields on `res.partner` are kept READ-ONLY — the
canonical configuration lives on `sale.payment.gateway`, and the
partner-side values are always derived from the selected gateway.

Propagation is enforced at three layers:
1. UI `@api.onchange` — instant fill when the user picks a gateway
2. `create()` override — server-side fill for API callers / imports
3. `write()` override — server-side re-fill when the gateway is changed
4. `sale.payment.gateway.write()` — when a gateway's accounts are
   changed, all linked partners are updated to mirror the new values

Features
--------
* New master: `sale.payment.gateway` (Sales → Configuration → Payment Gateways)
* Each gateway has: name, active flag, receivable account, payable account
* `res.partner` gets `payment_gateway_id` — selecting it auto-fills
  the partner's receivable & payable accounts from the gateway defaults
* `res.partner`'s `property_account_receivable_id` and
  `property_account_payable_id` become read-only (derived from gateway)
* `sale.order` gets `payment_gateway_id` (read-only on the form)
* `account.move` gets `payment_gateway_id` + `carrier_id` (both read-only)
* `stock.picking` gets `payment_gateway_id` (read-only)
* `stock.move` gets `payment_gateway_id` (propagated from the sale order)

The carrier (`carrier_id`) is also synced bidirectionally between
`sale.order` and `stock.picking` so changing it on either side keeps
both records aligned.
    """,
    'category': 'Sales',
    'author': 'Zelal Alhayek',
    'linkedin': 'https://www.linkedin.com/in/zelal-alhaeyk-077631193',
    'depends': ['sale_management', 'account', 'stock', 'delivery'],
    'data': [
        'security/ir.model.access.csv',
        'views/payment_gateway_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
