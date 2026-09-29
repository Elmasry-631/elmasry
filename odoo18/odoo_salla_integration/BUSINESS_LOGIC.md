# odoo_salla_integration — Business Logic & Functionality

**Author:** Webkul Software Pvt. Ltd.  
**Version:** 2.0.0  
**Category:** eCommerce  
**Dependencies:** `odoo_multi_channel_sale`

---

## Purpose

`odoo_salla_integration` is the **Salla-specific connector** that plugs into the `odoo_multi_channel_sale` framework. It handles OAuth authentication with Salla, API communication, data transformation between Salla and Odoo formats, and real-time webhooks for orders, products, customers, categories, taxes, and shipping.

**Salla** is a Saudi Arabian e-commerce platform. This module lets a merchant run their Salla store and Odoo ERP as one integrated system.

---

## Architecture

```
┌──────────────┐     OAuth / API      ┌─────────────────────┐
│  Salla Store │◄────────────────────►│  odoo_salla_        │
│  (api.salla  │     Webhooks         │  integration        │
│   .dev)      │─────────────────────►│                     │
└──────────────┘                      └──────────┬──────────┘
                                                 │ extends
                                      ┌──────────▼──────────┐
                                      │ odoo_multi_channel_  │
                                      │ sale (framework)     │
                                      └──────────┬──────────┘
                                                 │
                                      ┌──────────▼──────────┐
                                      │   Odoo ERP Records   │
                                      │ (orders, products…)  │
                                      └─────────────────────┘
```

### Key classes

| Class / Model | Role |
|---------------|------|
| `multi.channel.sale` (inherit) | Salla credentials, OAuth, import/export dispatch |
| `SallaApi` | HTTP client for Salla Admin API v2 |
| `FetchData` | Transforms Salla JSON → feed-compatible dicts |
| `multi.channel.sale` webhook inherit | Real-time event handlers |

---

## Authentication (OAuth 2.0)

Salla uses OAuth. Credentials are stored on the channel instance:

| Field | Description |
|-------|-------------|
| `salla_client_id` | App client ID from Salla developer portal |
| `salla_client_secret` | App secret key |
| `salla_redirect_url` | Callback URL: `{odoo_base_url}/salla/authenticate` |
| `salla_verification_key` | Unique 16-char key linking Odoo instance to Webkul auth proxy |
| `access_token` / `refresh_token` | OAuth tokens |
| `salla_store_name` / `salla_store_id` | Connected store identity |

### Connection flow

```
1. User configures Client ID + Secret on channel instance
2. User clicks "Connect to Salla"
3. Odoo calls Webkul proxy (salla-connector.webkul.in/salla)
4. User is redirected to Salla OAuth consent
5. Salla redirects to /salla/authenticate with tokens
6. Controller writes tokens → channel state = validate
```

Token refresh also goes through the Webkul proxy (`getAccessToken()`), not directly to Salla from Odoo.

> **Note:** Authentication relies on Webkul's external callback service (`salla-connector.webkul.in`), not purely on-premises OAuth.

---

## Default Order State Mappings

Pre-configured on install (`data/data.xml`):

| Salla Status (`slug`) | Odoo State | Actions |
|-----------------------|------------|---------|
| `under_review` | Quotation (draft) | Default state |
| `payment_pending` | Sale Order | Confirm |
| `completed` | Done | Create paid invoice + shipment |
| `shipped` | Sale Order | — |
| `delivering` | Sale Order | — |
| `delivered` | Done | — |
| `canceled` | Cancelled | Cancel order |

---

## Import Capabilities

Dispatched via `import_salla(object, **kw)`:

| Object | Salla API Endpoint | Supported |
|--------|-------------------|-----------|
| `product.category` | `GET /categories` | ✅ Manual + Cron |
| `sale.order` | `GET /orders` | ✅ Manual + Cron |
| `product.template` | `GET /products` | ✅ Manual only |
| `res.partner` | `GET /customers` | ✅ Manual only |
| `delivery.carrier` | `GET /shipping/companies` | ✅ Manual only |

### Not supported via cron (Salla-specific)

- Product import cron → logs "not supported"
- Partner import cron → logs "not supported"

### Order import details

Orders are fetched with expanded data. For each order, the connector:

1. Fetches order header (`/orders` or `/orders/{id}`)
2. Fetches shipments (`/shipments?order_id=`)
3. Fetches line items (`/orders/items?order_id=`)
4. Transforms via `FetchData.process_order()`

**Order line construction:**

| Line Type | Source | Odoo Product |
|-----------|--------|--------------|
| Product | `items[]` | Mapped product/variant |
| Discount | `amounts.discounts[]` | Discount service product |
| Delivery | `amounts.shipping_cost` | Delivery service product |
| COD | `amounts.cash_on_delivery` | Other charge service product |

**Customer & address:** Built from `customer` object and `shipping` / `shipments` data (billing + shipping contacts).

**Taxes:** Mapped via store tax percentage → `channel.account.mappings` → Odoo `account.tax`.

**Auto product import:** If an order line references an unmapped product, a product feed is created on the fly during order processing.

### Product import details

- Basic fields: name, SKU, price, cost, weight, quantity, description, image URL, categories.
- Variants: Salla `options` + `skus` → Odoo attributes and variant mappings.
- Pagination: up to 65 products per page.

### Category import

- Recursive tree from Salla nested `items` structure.
- Parent/child relationships preserved via `parent_id` and `leaf_category` flag.

---

## Export Capabilities

Dispatched via `export_salla(record, **kw)` and `update_salla(record, remote_id)`:

| Object | Action | Salla API |
|--------|--------|-----------|
| `product.category` | Create | `POST /categories` |
| `product.category` | Update | Update API with remote ID |
| `product.template` | Create | `POST /products` |
| `product.template` | Update | Update product + variant SKUs |

**Category export:** Recursively exports parent categories first if unmapped, then creates mapping.

**Product export:** Sends name, description, price, quantity, images (via Odoo-hosted image URL), and attribute options/values for variants.

**Stock sync:** `sync_quantity_salla()` → sets quantity on Salla product or variant via API.

---

## Reverse Sync (Odoo → Salla)

When enabled on the channel instance:

| Odoo Event | Salla Action | Status Slug |
|------------|--------------|-------------|
| Delivery validated (`salla_post_do_transfer`) | Update order status | `delivered` |
| Invoice paid (`salla_post_confirm_paid`) | Update order status | `completed` |
| Order cancelled (`salla_post_cancel_order`) | Update order status | `canceled` |

Requires matching entry in `channel.order.states` and enabled flags: `sync_shipment`, `sync_invoice`, `sync_cancel`.

---

## Webhooks (Real-Time — Salla → Odoo)

Webhook activation/deactivation goes through Webkul proxy (`/webhook/setup`).

### Order webhooks

| Event | Handler | Result |
|-------|---------|--------|
| `order.created` | `salla_order_webhook_data(type='create')` | Create order feed |
| `order.updated` | `salla_order_webhook_data(type='update')` | Update order feed |

Routes (from base module):

- `/multichannel/create/order/webhook/{channel_id}`
- `/multichannel/update/order/webhook/{channel_id}`

### Other webhooks (via generic route)

| Event | Handler | Result |
|-------|---------|--------|
| Product create/update | `salla_webhook_create/update_product_data` | Create/update product feed |
| Product delete | `salla_webhook_delete_product_data` | Remove template mapping |
| Customer create/update | `salla_webhook_create/update_customer_data` | Create/update partner feed |
| Category create/update | `salla_webhook_create/update_category_data` | Create/update category feed |
| Store tax create | `salla_webhook_create_storetax_data` | Create tax + mapping |
| Shipping company CRUD | `salla_webhook_*_shipping_company_data` | Create/update/delete carrier feed |

If `auto_evaluate_feed` is enabled, webhook feeds are immediately evaluated into Odoo records.

---

## Scheduled Jobs (Salla-Specific)

Enabled configs via `salla_available_configs()`:

| Cron Field | Salla Method | Status |
|------------|--------------|--------|
| `import_order_cron` | `salla_import_order_cron()` | ✅ Implemented |
| `import_category_cron` | `salla_import_category_cron()` | ✅ Implemented |
| `import_product_cron` | `salla_import_product_cron()` | ❌ Not supported |
| `import_partner_cron` | `salla_import_partner_cron()` | ❌ Not supported |

Order cron imports orders from `import_order_date` forward, then updates that date to the latest imported order.

---

## Data Transformation (`FetchData`)

Central class that converts Salla API responses into the dict format expected by feed models:

| Method | Transforms |
|--------|------------|
| `get_all_categories()` | Nested category tree → flat feed list |
| `import_product_vals()` | Salla product → product feed dict + variants |
| `process_customer()` | Salla customer → partner feed dict |
| `process_order()` | Salla order → order feed dict with lines |
| `process_address()` | Shipping/billing from order → contact fields |
| `get_shipping_vals()` | Shipping company → shipping feed dict |
| `process_tax()` | Tax amount → tax mapping lookup |

---

## API Client (`SallaApi`)

- Base URL: `https://api.salla.dev/admin/v2/`
- Auth: Bearer token in headers
- Pagination: Follows `pagination.links.next` for list endpoints
- Error handling: Logs failures; returns empty list on error

Key API groups used: categories, products, orders, customers, shipments, shipping companies, order statuses, webhooks, store info.

---

## Controllers

### `/salla/authenticate` (public, HTTP)

OAuth callback endpoint. Receives tokens from Webkul proxy, matches channel by `salla_verification_key`, writes credentials, sets state to `validate`, redirects to channel form.

---

## Configuration Checklist

1. Install `wk_wizard_messages` → `odoo_multi_channel_sale` → `odoo_salla_integration`
2. Create/configure Salla channel instance (Client ID, Secret, Verification Key)
3. Connect via OAuth ("Connect to Salla")
4. Set warehouse, pricelist, default category, sales team
5. Review/adjust order state mappings
6. Enable crons (orders, categories) if desired
7. Enable webhooks for real-time order/product sync
8. Enable reverse sync flags (invoice, shipment, cancel) as needed

---

## Limitations & Notes

- **Auth proxy dependency:** OAuth and webhook setup require Webkul's external service.
- **No product/partner cron:** Products and customers must be imported manually or via webhooks.
- **Single channel type:** One connector instance = one Salla store.
- **Image export:** Products export images via Odoo public URL (`/channel/image/...`).
- **Tax mapping:** Store taxes are mapped by percentage value, not by Salla tax ID.

---

## Summary

| Aspect | Detail |
|--------|--------|
| Role | Salla marketplace connector for Odoo Multichannel |
| Platform | Salla (Saudi e-commerce) |
| Auth | OAuth 2.0 via Webkul proxy |
| Import | Orders, products, categories, customers, shipping |
| Export | Categories, products, stock quantities |
| Real-time | Webhooks for orders, products, customers, categories, taxes, shipping |
| Reverse sync | Order status updates on invoice, delivery, cancellation |
| Depends on | `odoo_multi_channel_sale` framework |
