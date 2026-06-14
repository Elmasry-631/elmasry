# Technical Reference — Customer Classification Module

## Models Overview

### 1. customer.classification (New)

**Table:** `customer_classification`

| Field | Type | Description |
|-------|------|-------------|
| `name` | Char (required) | Classification code (A, B, C...) |
| `description` | Text | Optional description |
| `sequence` | Integer (default: 10) | Sort order + auto-class priority |
| `active` | Boolean (default: True) | Soft delete |
| `pricelist_id` | Many2one → product.pricelist | Inherited price list |
| `credit_limit` | Float(16,2) (default: 0) | Inherited credit limit |
| `payment_term_id` | Many2one → account.payment.term | Inherited payment term |
| `credit_policy` | Selection (block/warning) | Credit enforcement policy |
| `company_id` | Many2one → res.company (required) | Multi-company isolation |
| `partner_ids` | One2many → res.partner | Customers in this tier |
| `partner_count` | Integer (compute) | Count of customers |
| `criteria_ids` | One2many → classification.criteria | Auto-class conditions |
| `has_active_criteria` | Boolean (compute) | Has active criteria? |

**Constraint:** `UNIQUE(name, company_id)`

**Methods:**
- `action_apply_pricelist()` — Manual pricelist push to non-override customers
- `_auto_classify_partners()` — Cron entry point for auto-classification
- `_evaluate_for_partner(partner, classifications)` — Evaluate criteria for one customer
- `_get_partner_metrics(partner)` — Compute all 6 evaluation metrics

---

### 2. classification.criteria (New)

**Table:** `classification_criteria`

| Field | Type | Description |
|-------|------|-------------|
| `classification_id` | Many2one → customer.classification (CASCADE) | Parent classification |
| `sequence` | Integer (default: 10) | Evaluation order within classification |
| `model_field` | Selection (6 options) | Metric to evaluate |
| `operator` | Selection (6 options) | Comparison operator |
| `value` | Float(16,2) (required) | Primary comparison value |
| `value_to` | Float(16,2) | Upper bound (only for 'between') |
| `active` | Boolean (default: True) | Enable/disable |

**Available Metrics:**
- `total_sales` — Current year sales sum
- `total_sales_last_year` — Previous year sales sum
- `outstanding_balance` — Partner receivable balance
- `overdue_balance` — Unpaid invoices past due
- `number_of_orders` — Current year order count
- `customer_age_days` — Days since partner creation

---

### 3. res.partner (Extended)

**New Fields (11):**

| Field | Type | Purpose |
|-------|------|---------|
| `classification_id` | Many2one → customer.classification | Main link |
| `override_pricelist` | Boolean | Toggle manual PL |
| `manual_pricelist_id` | Many2one → product.pricelist | Manual PL value |
| `override_credit_limit` | Boolean | Toggle manual CL |
| `override_payment_term` | Boolean | Toggle manual PT |
| `classification_pricelist_id` | Related (read-only) | Show classif. PL |
| `classification_credit_limit` | Related (store) | Show classif. CL |
| `classification_payment_term_id` | Related (read-only) | Show classif. PT |
| `credit_policy` | Related (store) | Show classif. policy |
| `effective_credit_limit` | Compute | Actual CL applied |
| `effective_payment_term_id` | Compute | Actual PT applied |

**Overridden Methods:**
- `_compute_product_pricelist()` — Adds classification + override chain

**Onchange Methods:**
- `_onchange_classification_id()` — Clears overrides when classification removed
- `_onchange_override_pricelist()` — Clears manual PL when toggle off
- `_onchange_override_credit_limit()` — Clears CL when toggle off
- `_onchange_override_payment_term()` — Clears PT when toggle off

---

### 4. sale.order (Extended)

**New Fields (3):**

| Field | Type | Purpose |
|-------|------|---------|
| `partner_classification_id` | Related (store) | For search/group on orders |
| `partner_effective_credit_limit` | Related | Display on order |
| `partner_credit_policy` | Related | Display on order |

**Overridden Methods:**
- `action_confirm()` — Pre-hook credit check before super()
- `_check_classification_credit()` — Evaluate credit limit vs. projected total

---

## Override Priority Chain

```
1. override=True + manual value set  →  USE manual value
2. classification default set       →  USE classification value
3. partner's own value              →  USE as-is
4. 0 / empty                        →  NONE (no constraint)
```

## Security Matrix

| Model | Sales Manager | Sales User |
|-------|:------------:|:---------:|
| customer.classification | CRUD | Read |
| classification.criteria | CRUD | Read |