# Dependencies Map — el_cheque_tracking

## Module dependencies (declared in `__manifest__.py`)

| Module | Required for |
|---|---|
| `base` | Base model classes, res.partner, res.company, ir.sequence, ir.cron |
| `mail` | `mail.thread` mixin (chatter), `mail.activity.mixin`, mail activities |
| `account` | `account.move`, `account.payment`, `account.payment.register`, `account.payment.method`, `account.journal`, `account.account`, chart of accounts |

## Why these dependencies (and not others)

| Considered | Decision | Reason |
|---|---|---|
| `base` | ✅ depend | Required for every Odoo module |
| `mail` | ✅ depend | Chatter + activities are core UX for cheques |
| `account` | ✅ depend | Cheque lifecycle posts account.move entries; needs chart of accounts |
| `sale` | ❌ skip | Cheques are not sale-specific; sale module would be unnecessary coupling |
| `purchase` | ❌ skip | Same — cheques apply to any payable, not just purchase bills |
| `stock` | ❌ skip | No inventory interaction |
| `web` | (auto) | Available transitively via `account` → `base` → `web` |
| `l10n_*` | ❌ skip | Module is country-agnostic; users install their own localization |

## Optional integrations (not declared, but compatible)

- **`account_payment_method`**: the module creates 2 cheque payment methods
  via data XML. If a user installs `account_payment_method`, the cheque
  methods will appear in the payment method configuration UI.
- **`base_multi_company`**: not required — multi-company is handled via
  standard `company_id` + record rules.
