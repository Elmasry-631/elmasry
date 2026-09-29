# el_mobile_webhook

Odoo 18 Enterprise add-on for durable outbound webhook events. It queues state changes for sales orders, deliveries, customer invoices/refunds, and payments.

## Install and configure

1. Copy `el_mobile_webhook` to an Odoo add-ons path and update Apps List.
2. Install **Mobile Webhook**.
3. Go to **Settings > Mobile Webhook** (System Administrator) and enter an HTTPS endpoint, shared secret, timeout, and retry limit.
4. Ensure the scheduled action **Mobile Webhook: Process Queue** is active.

## Receiver contract

Odoo posts the persisted JSON payload with `X-Odoo-Webhook-Id`, `X-Odoo-Webhook-Event`, and `X-Odoo-Webhook-Signature: sha256=<hex>` headers. Verify the HMAC over the exact request body and persist event IDs before acting, so retries are safe.

Retries are exponential: 1, 2, 4, 8… minutes, capped at one hour; after the configured limit, the event becomes Failed for manual retry.

## Security

Only HTTPS endpoints are allowed. The secret is never put in the queue payload or logs. The queue and configuration require System Administrator access. This is at-least-once delivery; receiver idempotency is mandatory.
