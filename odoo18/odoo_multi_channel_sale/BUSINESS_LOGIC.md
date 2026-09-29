# odoo_multi_channel_sale — Business Logic & Functionality

**Author:** Webkul Software Pvt. Ltd.  
**Version:** 2.8.19  
**Category:** eCommerce  
**Dependencies:** `stock_delivery`, `wk_wizard_messages`

---

## Purpose

`odoo_multi_channel_sale` is the **core bridge framework** that connects Odoo to external e-commerce platforms. It is not tied to a single marketplace — channel-specific connectors (e.g. Salla, Shopify, Magento) extend this module and plug in their API logic.

It solves one central problem: **keep Odoo and an online store in sync** for products, categories, customers, orders, shipping, taxes, and inventory — in both directions where supported.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Channel Connector                         │
│         (e.g. odoo_salla_integration extends this)           │
│   import_salla() / export_salla() / connect_salla() / etc.   │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                  multi.channel.sale                          │
│            (Channel Instance / Configuration)                │
└──────────────────────────┬──────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   ┌──────────┐     ┌────────────┐    ┌─────────────┐
   │  Feeds   │     │  Mappings  │    │  Odoo Core  │
   │ (staging)│────▶│ (ID links) │───▶│  Records    │
   └──────────┘     └────────────┘    └─────────────┘
```

### Design pattern: Feed → Evaluate → Map → Create/Update

1. **Fetch** data from the external channel via channel-specific API methods.
2. **Store** raw data in **Feed** records (staging layer).
3. **Evaluate** feeds to create or update real Odoo records.
4. **Maintain Mappings** linking store IDs to Odoo record IDs for future sync.

---

## Core Model: `multi.channel.sale`

The channel **instance** — one record per connected store/marketplace.

### Connection & State

| Field / Concept | Description |
|-----------------|-------------|
| `channel` | Platform type (extended by connectors, e.g. `salla`) |
| `state` | `draft` → `validate` → `error` |
| `environment` | `sandbox` or `production` |
| `test_connection()` | Calls `connect_{channel}()` on the instance |

### Business Configuration

| Setting | Purpose |
|---------|---------|
| `warehouse_id` / `location_id` | Stock source for imported products and quantity sync |
| `pricelist_name` | Currency/pricing alignment with the store |
| `default_category_id` | Fallback internal category for imported products |
| `delivery_product_id` | Service product used for shipping order lines |
| `discount_product_id` | Service product used for discount order lines |
| `other_charge_product_id` | Service product for COD / misc charges |
| `crm_team_id`, `sales_person_id` | Defaults applied to imported sale orders |
| `payment_term_id` | Default payment terms on orders |
| `utm_*` fields | Marketing attribution defaults |
| `channel_stock_action` | Which stock metric to sync: QOH, free qty, or forecast |
| `auto_evaluate_feed` | Process feeds immediately after import |
| `auto_sync_stock` | Push stock changes to the channel in real time |
| `sync_invoice` / `sync_shipment` / `sync_cancel` | Push status back to the store when Odoo actions occur |

### Order State Mapping (`channel.order.states`)

Maps external order statuses to Odoo workflow actions:

| Channel State (example) | Odoo State | Actions |
|-------------------------|------------|---------|
| `payment_pending` | `sale` | Confirm order |
| `completed` | `done` | Create invoice (paid), create shipment |
| `canceled` | `cancelled` | Cancel order |
| `delivered` | `done` | Mark done |

Each mapping can trigger: order confirmation, invoice creation, invoice payment state, and delivery/shipment.

---

## Feed Layer (Staging)

All imported data lands in feed models before becoming Odoo records:

| Feed Model | Imports Into |
|------------|--------------|
| `category.feed` | `product.category` |
| `product.feed` | `product.template` / `product.product` |
| `partner.feed` | `res.partner` |
| `order.feed` | `sale.order` |
| `shipping.feed` | `delivery.carrier` |
| `variant.feed` | Product variants (via product feed) |

### Feed lifecycle

```
draft → (evaluate) → done | error | cancel
```

- Feeds hold store-side field values (names, prices, addresses, line items).
- `import_items()` on a feed evaluates it and creates/updates Odoo records.
- Messages and timestamps are appended to the feed's `message` field for audit.

---

## Mapping Layer (ID Linking)

Mappings persist the relationship between store IDs and Odoo IDs:

| Mapping Model | Links |
|---------------|-------|
| `channel.category.mappings` | Store category ↔ Odoo category |
| `channel.template.mappings` | Store product ↔ Odoo template |
| `channel.product.mappings` | Store variant ↔ Odoo product variant |
| `channel.partner.mappings` | Store customer ↔ Odoo partner |
| `channel.order.mappings` | Store order ↔ Odoo sale order |
| `channel.account.mappings` | Store tax ↔ Odoo tax |
| `channel.account.journal.mappings` | Payment method ↔ Odoo journal |
| `channel.shipping.mappings` | Shipping carrier ↔ Odoo delivery carrier |
| `channel.pricelist.mappings` | Store pricelist ↔ Odoo pricelist |

**`need_sync` flag:** When an Odoo record changes (e.g. product stock/price), related mappings are marked `need_sync = yes` so the channel can push updates.

---

## Import Flow

```
User / Cron triggers Import Operation
        │
        ▼
import.operation wizard (select object + filters)
        │
        ▼
ApiTransaction.import_data()
        │
        ▼
Calls import_{channel}(object) on channel instance
        │  (implemented by connector, e.g. import_salla)
        ▼
Returns list of dicts → _create_feeds()
        │
        ▼
If auto_evaluate_feed: feed.import_items()
        │
        ▼
Creates/updates Odoo records + mappings
        │
        ▼
display_message() → popup summary via wk_wizard_messages
```

### Importable objects

- Products (`product.template`)
- Orders (`sale.order`)
- Categories (`product.category`)
- Customers (`res.partner`)
- Shipping methods (`delivery.carrier`)

Pagination, API limits, and date filters are handled per channel.

---

## Export Flow

```
User triggers Export Operation (from channel or product list)
        │
        ▼
export.operation wizard
        │
        ▼
ApiTransaction.export_data()
        │
        ▼
For unmapped records: calls export_{channel}(record)
        │
        ▼
Creates mapping on success
        │
        ▼
For mapped records (update mode): calls update_{channel}(record)
```

Exportable objects (base): categories and product templates. Connectors implement the actual API calls.

---

## Order Import — Detailed Logic

When an order feed is evaluated:

1. **Customer** — find or create `res.partner` from store customer ID; handle billing/shipping addresses.
2. **Products** — resolve each line via mappings; auto-import product feed if unmapped.
3. **Order lines** — product lines, plus special lines:
   - **Delivery** → uses `delivery_product_id`
   - **Discount** → uses `discount_product_id` (negative price)
   - **Other charges** (e.g. COD) → uses `other_charge_product_id`
4. **Taxes** — mapped via `channel.account.mappings` from store tax rates.
5. **Payment method** — auto-creates bank journal + mapping if needed.
6. **Order state** — applies `channel.order.states` rules (confirm, invoice, ship).
7. **Mapping** — creates `channel.order.mappings` linking store order ID to Odoo sale order.

---

## Real-Time Sync (Odoo → Store)

When configured (`sync_invoice`, `sync_shipment`, `sync_cancel`), Odoo actions trigger callbacks on the channel instance:

| Odoo Action | Hook | Typical Store Action |
|-------------|------|----------------------|
| Invoice confirmed/paid | `{channel}_post_confirm_paid` | Mark order completed |
| Delivery validated | `{channel}_post_do_transfer` | Mark order delivered |
| Order cancelled | `{channel}_post_cancel_order` | Mark order canceled |
| Product stock/price change | `sync_quantity_{channel}` | Update store inventory |

Implemented by each connector (e.g. Salla updates order status via API).

---

## Webhooks (Inbound — Store → Odoo)

Generic webhook controller at:

- `/multichannel/create/order/webhook/{channel_id}`
- `/multichannel/update/order/webhook/{channel_id}`
- `/multichannel/{object}/webhook/{channel_id}`

Connectors implement handlers like `{channel}_order_webhook_data()` to parse payloads, create feeds, and optionally auto-evaluate.

---

## Scheduled Jobs (Crons)

| Cron | Default | Action |
|------|---------|--------|
| Import - Order | Inactive | `cron_import_all("order")` |
| Import - Category | Inactive | `cron_import_all("category")` |
| Import - Partner | Inactive | Inactive |
| Import - Product | Inactive | `cron_import_all("product")` |
| Feed Evaluation | Inactive | Process pending feeds |
| Auto-vacuum sync history | Inactive | Clean old sync logs |
| Order mapping status update | Active (3h) | Sync invoice/delivery flags on mappings |

Channel connectors enable specific crons via `salla_available_configs()` etc.

---

## Synchronization Audit

`channel.synchronization` records log every sync action (import/export, success/error, timestamps) for troubleshooting.

---

## Core Odoo Extensions

The module extends standard Odoo models with channel awareness:

| Model | Extension |
|-------|-----------|
| `sale.order` | Mapping relation; cancel/invoice hooks for reverse sync |
| `product.product` / `product.template` | Mapping relations; marks `need_sync` on write |
| `stock.picking` | Shipment sync hooks |
| `account.move` | Invoice sync hooks |
| `res.partner` | Customer mapping relation |
| `product.category` | Category mapping relation |
| `delivery.carrier` | Shipping mapping relation |

---

## Dashboard & UI

- Multi-channel dashboard (JS/XML assets) showing instance stats: products, categories, orders, customers synced.
- Per-instance configuration form with import/export buttons, cron toggles, webhook settings, and mapping views.
- Security groups restrict channel management to authorized users.

---

## Extension Points for Connectors

A channel connector must implement:

| Method | Purpose |
|--------|---------|
| `get_channel()` | Register channel name in selection |
| `connect_{channel}()` | Validate API credentials |
| `import_{channel}(object, **kw)` | Fetch data from store API |
| `export_{channel}(record, **kw)` | Push new records to store |
| `update_{channel}(record, remote_id)` | Update existing store records |
| `sync_quantity_{channel}(mapping, qty)` | Push stock to store |
| `{channel}_default_order_state()` | Default order state mappings |
| `{channel}_post_*` hooks | Reverse sync on invoice/ship/cancel |
| Webhook handlers | Real-time inbound events |

---

## Summary

| Aspect | Detail |
|--------|--------|
| Role | Core multichannel e-commerce bridge framework |
| Pattern | Feed → Evaluate → Map → Odoo record |
| Directions | Import (store→Odoo), Export (Odoo→store), Real-time both ways |
| Objects | Products, categories, customers, orders, shipping, taxes |
| Connectors | Installed separately; extend this base module |
| Key dependency | `wk_wizard_messages` for operation result popups |
