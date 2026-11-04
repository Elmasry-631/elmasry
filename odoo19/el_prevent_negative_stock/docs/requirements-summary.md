# Requirements Summary — el_prevent_negative_stock

## Target Odoo Version
19

## Module Name
el_prevent_negative_stock

## Description
Module that prevents negative stock quantities by rejecting any stock move
that would result in a negative quantity for a product in a given location.
Applies to ALL types of stock operations (delivery, internal transfers,
manufacturing). No exceptions — even managers cannot override.

## Models Needed
1. **stock.move (extension)** — Override `_action_done` to check available
   quantity before confirming. If insufficient → raise UserError + create
   alert record + send email notification.
2. **el.stock.alert** — Log of all rejected negative stock attempts.

## Features
- **Reject negative stock** — Any move that would result in negative qty
  is rejected with a clear error message.
- **Applies to ALL stock types** — Delivery orders, internal transfers,
  manufacturing orders, receipts.
- **No exceptions** — Even warehouse managers cannot override. This is a
  hard business rule.
- **Email notification** — When a move is rejected, an email is sent to
  the warehouse manager.
- **Alert log** — All rejected attempts are logged in `el.stock.alert`
  model with product, location, requested qty, available qty, user, timestamp.

## User Roles (no exceptions for anyone)
| Role | Stock Group | Access to alerts |
|------|-------------|-----------------|
| Warehouse User | stock.group_stock_user | Read own |
| Warehouse Manager | stock.group_stock_manager | Read all |

## Dependencies
- base
- stock
- mail

## Open Questions
None — all clarified with user.
