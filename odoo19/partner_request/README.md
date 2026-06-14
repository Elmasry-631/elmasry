# Partner Request

![Odoo 19](https://img.shields.io/badge/Odoo-19.0-blue)
![License](https://img.shields.io/badge/License-LGPL--3-green)

## Purpose

Provides an approval workflow for creating new customers. Sales users submit partner creation requests, and managers review, approve, reject, or send them back for revision. This prevents data entry errors and ensures all new customers go through proper review.

## Key Features

- **5-State Workflow**: Draft → Pending → Approved / Rejected / Sent Back
- **Auto-Generated Numbers**: PRQ-YYYY-NNNNN format with yearly reset
- **Role-Based Buttons**: Submit (all users), Approve/Reject/Send Back (managers only)
- **Activities & Notifications**: Automatic activity scheduling on supervisors and notifications to salespeople
- **Duplicate Detection**: Email duplicate check before partner creation
- **Direct Creation Restriction**: Sales users cannot create company-type partners directly
- **Smart Button**: Quick access to the created customer from approved requests
- **Chatter & Attachments**: Full discussion and document exchange on each request

## Installation

1. Go to **Apps** > **Upload Module**
2. Upload the `partner_request` ZIP file
3. Click **Activate**
4. Menu appears: **Sales** > **Customers** > **Partner Requests**
5. Two security groups are auto-assigned to existing sales users and managers

## Configuration

No additional configuration is required. The module works out of the box with:
- Sales Users automatically get the "Partner Request User" group
- Sales Managers automatically get the "Partner Request Manager" group
- Sequence is pre-configured with PRQ-YYYY-NNNNN format

## Usage

### Sales User Workflow

1. Go to **Sales** > **Customers** > **Partner Requests**
2. Click **New** and fill in customer details
3. Click **Submit** — an activity is sent to your supervisor
4. If sent back: edit the request and resubmit

### Sales Manager Workflow

1. Open a **Pending** request from the list
2. Review the customer information
3. Choose one of:
   - **Create Partner**: Creates the customer and links it to the request
   - **Send Back**: Returns to the salesperson with a reason (they can resubmit)
   - **Reject**: Permanently rejects the request with a reason

## State Machine

```
Draft ──Submit──► Pending ──Create Partner──► Approved
                     │  ▲
                Send Back │
                     │  │
                     ▼  │
                  Sent Back ──Submit──► Pending
                     │
               Reject │
                     ▼
                  Rejected
```

## Changelog

| Date | Version | Changes |
|------|---------|---------|
| 2026-06-13 | 19.0.1.0.0 | Initial release |

## License

LGPL-3

## Author

Ibrahim Elmasry