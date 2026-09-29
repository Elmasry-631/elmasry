# Requirements Summary

- Target: Odoo 18 Enterprise.
- Module: `el_mobile_webhook` version `18.0.1.0.0`.
- Scope: queue and deliver outbound status webhooks for `sale.order`, `stock.picking`, customer invoices/refunds, and `account.payment`.
- Security: HTTPS endpoint, HMAC-SHA256, non-secret logs, idempotency event ID, manager-only configuration and queue access.
- Reliability: durable queue, bounded exponential retry, cron delivery.
- Explicit non-goals: inbound endpoint, arbitrary data synchronization, Odoo Core/Studio modifications.

## Lifecycle
Status transition -> queued immutable event -> scheduled delivery -> receiver de-duplicates by event ID.

## Assumptions
The mobile backend accepts JSON and verifies `X-Odoo-Webhook-Signature` against the raw JSON body. Its idempotency store is durable.