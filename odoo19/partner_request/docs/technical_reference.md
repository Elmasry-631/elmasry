# Technical Reference — Partner Request Module

## Models

### 1. partner.request (New)

**Table:** `partner_request`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | Char | Yes | Customer name |
| customer_code | Char | No | Manual code |
| customer_category | Char | No | Business category |
| contact_person | Char | No | Contact person name |
| partner_id | Many2one → res.partner | No (auto) | Created customer |
| sequence | Char (readonly) | Auto | PRQ-YYYY-NNNNN |
| country_id | Many2one → res.country | No | Country |
| state_id | Many2one → res.country.state | No | State (filtered by country) |
| city | Char | No | City |
| area | Char | No | Area/neighborhood |
| street | Char | No | Street address |
| zip | Char | No | ZIP code |
| pobox | Char | No | P.O. Box |
| phone | Char | No | Phone number |
| email | Char | No | Email |
| vat | Char | No | Tax ID / VAT |
| sales_supervisor_id | Many2one → res.users | No | Supervisor |
| salesperson_id | Many2one → res.users | Auto | Requester (current user) |
| state | Selection | Yes (default: draft) | Workflow status |
| rejection_reason | Text | No | Reason for rejection |
| send_back_reason | Text | No | Reason for send back |

**Inherits:** mail.thread, mail.activity.mixin

### 2. res.partner (Extended)

**Override:** `create()` — restricts company-type partner creation for users in `partner_request.group_partner_request_user` (non-managers). Bypassed via context key `partner_request_bypass`.

## Methods

| Method | Model | Description |
|--------|-------|-------------|
| `create()` | partner.request | Override: generates sequence number |
| `_validate_state(allowed)` | partner.request | Validates state before transitions |
| `action_submit()` | partner.request | draft/sent_back → pending + activity on supervisor |
| `action_create_partner()` | partner.request | pending → approved + creates res.partner + notifies |
| `action_send_back()` | partner.request | pending → sent_back + activity on salesperson |
| `action_reject()` | partner.request | pending → rejected + notifies salesperson |
| `action_open_partner()` | partner.request | Smart button: opens created partner |
| `create()` | res.partner | Restricts direct company creation for users |

## Security Matrix

| Model | Request Manager | Request User |
|-------|:---------------:|:-----------:|
| partner.request | CRUD | CR (no delete) |
| res.partner (company create) | Allowed | Blocked |

## Groups Hierarchy

```
sales_team.group_sale_manager
  └── partner_request.group_partner_request_manager
        └── partner_request.group_partner_request_user

sales_team.group_sale_user
  └── partner_request.group_partner_request_user
```