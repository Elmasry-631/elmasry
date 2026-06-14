# Customer Classification & Credit Control

![Odoo 19](https://img.shields.io/badge/Odoo-19.0-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green)

## Purpose

Classify customers into tiers (A, B, C, D, E) where each tier defines a default price list, credit limit, and payment term. Customers inherit these values automatically, with individual override support. Credit checks are enforced on sale order confirmation with configurable block or warning policies.

## Key Features

- **Tier Management**: Create classification tiers (A-E) with code, description, and sequence
- **Price List Inheritance**: Changing a tier's price list automatically updates all assigned customers
- **Credit Limit Enforcement**: Block or warn on sale order confirmation when credit is exceeded
- **Payment Term Inheritance**: Default payment terms flow from classification to customers
- **Individual Overrides**: Per-customer override for price list, credit limit, and payment term
- **Effective Values Display**: See exactly what values are applied (classification vs. override)
- **Auto-Classification**: Optional criteria-based auto-assignment via cron job (disabled by default)
- **Multi-Company**: Each classification belongs to a single company with isolation
- **Role-Based Access**: Sales Manager gets full CRUD; Sales User gets read-only access

## Installation

1. Go to **Apps** > **Upload Module**
2. Upload the `customer_classification` ZIP file
3. Click **Activate**
4. 5 default classifications (A-E) are created automatically
5. Menu appears: **Sales** > **Configuration** > **Customer Classification** > **Classifications**

## Configuration

### Step 1: Set Up Classifications
1. Go to **Sales** > **Configuration** > **Customer Classification** > **Classifications**
2. Open each classification (A-E) and configure:
   - **Price List**: Select a product price list
   - **Credit Limit**: Set the default credit limit (e.g., A = 1,000,000)
   - **Payment Term**: Select default payment terms (e.g., 30 Days)
   - **Credit Policy**: Choose **Block Sale** or **Warning Only**

### Step 2: Assign Customers
1. Open a customer form
2. Go to the **Classification & Credit** tab
3. Select a classification
4. The customer inherits price list, credit limit, and payment term automatically
5. Enable **Override** toggles to set individual values

### Step 3: (Optional) Set Up Auto-Classification
1. Open a classification and go to **Auto-Classification Criteria** tab
2. Add criteria (e.g., Total Sales >= 1,000,000 AND Overdue Balance < 50,000)
3. Go to **Settings** > **Technical** > **Scheduled Actions**
4. Find **"Customer Classification: Evaluate Auto-Classification"**
5. Set **Active = True** and adjust the interval

## Usage

### Daily Workflow (Sales Manager)
1. Review customer count per classification in the list view
2. Adjust credit limits or price lists per classification (seasonal changes)
3. Monitor credit warnings in sale order chatters
4. Review and update auto-classification criteria

### Order Creation (Salesperson)
1. Create/Select customer
2. System shows classification info and effective credit limit in the order
3. On Confirm:
   - **Block Policy**: Order is blocked if credit exceeded (detailed error message)
   - **Warning Policy**: Warning posted to chatter, order proceeds

### Cascade Update Example
Change price list on Classification "A" from "Retail" to "VIP" → All customers in A (without override) automatically get "VIP" price list.

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-06-13 | 19.0.1.0.0 | Initial release: Classification CRUD, price list inheritance, credit check, auto-classification, multi-company |

## License

LGPL-3

## Author

Ibrahim Elmasry — Odoo Master Skill v7.8