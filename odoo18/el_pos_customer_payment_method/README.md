# POS Customer Payment Method (el_pos_customer_payment_method)

Odoo 18 · LGPL-3 · Community

Restrict the payment methods a customer may use in the Point of Sale, with
POS-level defaults for everyone else.

## Behaviour

| Situation in the POS payment screen | Buttons shown |
|---|---|
| Order partner (or its commercial partner) has *Allowed POS Payment Methods* | Only those methods (clipped to the methods enabled on this POS) |
| Partner without a list, POS has *Default Payment Methods* | Only the default methods |
| No partner selected, or nothing configured anywhere | All payment methods of this POS |

The button list is **live**: it refreshes the moment the order partner
changes (or is removed) — no need to close and reopen the payment screen.

## Configuration

1. **Per customer** — Contacts > open a customer > *Sales & Purchase* tab >
   *Allowed POS Payment Methods*. Multiple methods are allowed. Set it on
   the main contact record: the screen falls back to the commercial partner
   when the order is set to a child (invoice) address, but not the reverse.
2. **Per POS** — Point of Sale > Configuration > Settings > *Payment*
   section > *Default Payment Methods*. These apply to customers without a
   specific list. Leave empty to allow all methods.

## Technical notes

- `res.partner.el_allowed_pos_payment_method_ids` (many2many to
  `pos.payment.method`), exposed to the POS frontend via
  `_load_pos_data_fields`, together with `commercial_partner_id` so the
  payment screen can fall back to the parent when the order partner is a
  child address.
- `pos.config.el_pos_default_payment_method_ids` — loaded automatically with
  the other config fields.
- `static/src/js/payment_screen.js` patches `PaymentScreen`: a reactive
  `payment_methods_from_config` getter applies the rules above on every
  render, and a matching setter keeps the assignments done by the base
  `setup()` (and by modules such as `pos_urban_piper`) working.
- No new models, no new security rules; depends only on `point_of_sale`.

## Testing

```bash
odoo-bin -d <db> -i el_pos_customer_payment_method --test-tags \
    /el_pos_customer_payment_method --stop-after-init
```

Six post-install tests lock the data contract: field persistence, POS
field exposure for partners, the child-address/commercial-partner pair, data
read content, config defaults loading and the settings related-field
round-trip.

## Compatibility

Odoo 18.0 Community and Enterprise (POS front-end patch targets the
community `point_of_sale` app shared by both editions).
