# Configuration Guide

## Prerequisites

Before installing this module, ensure the following:
- Odoo 19.0 (or 18.0 with minor adjustments)
- `el_nmo_classification` module is installed and configured
- Customer classifications with credit policies are set up
- Sales teams are configured with team leaders (for supervisor discovery)

## Installation

1. Copy the `el_nmo_credit_approval` folder to your Odoo addons directory
2. Go to Settings > Apps > Update Apps List
3. Search for "Credit Limit Approval" and click Install
4. The module will automatically create security groups, default rejection reasons, and the sequence

## Post-Installation Configuration

### 1. Configure Sales Teams (Critical)

The supervisor lookup depends on sales teams having team leaders:

1. Go to Settings > Sales > Sales Teams
2. Open each sales team
3. Set the "Team Leader" field (`user_id`) to the supervisor user
4. Add salespersons as team members

If no team leader is configured, the system falls back to the salesperson's "Manager" field (`parent_id` on the user). If neither is set, the current user is used (which means the salesperson would be their own supervisor — not ideal).

### 2. Customize Rejection Reasons

1. Go to Sales > Configuration > Credit Approval > Rejection Reasons
2. Review the 8 default reasons
3. Edit existing reasons: change the name, description, or sequence
4. Add new reasons specific to your business
5. Deactivate unused reasons using the toggle (do not delete — they may be referenced in historical records)

### 3. Assign Security Groups

1. Go to Settings > Users & Companies > Users
2. Open a salesperson user
3. In the "Sales" tab, check "Credit Approval — Salesperson"
4. Open a supervisor user
5. In the "Sales" tab, check "Credit Approval — Supervisor"
6. Open a manager user
7. In the "Sales" tab, check "Credit Approval — Manager"

### 4. Customize Email Template (Optional)

The module creates a default email template at `email_template_credit_approval`:

1. Go to Settings > Technical > Email > Templates
2. Search for "Credit Approval — Notify Supervisor"
3. Edit the subject, body HTML, or styling to match your company branding
4. Do NOT change the model (`credit.approval.request`) or the field references

### 5. Verify Customer Setup

For the workflow to trigger, customers must have:
- `payment_type` = 'credit' (on the partner form, Sales tab)
- A `classification_id` assigned with `credit_policy` = 'block'
- A positive `effective_credit_limit` (set via classification or override)

### 6. Test the Workflow

1. Create a test customer with credit payment type
2. Assign a classification with block policy and a low credit limit (e.g., 1,000)
3. Create unpaid invoices for the customer to bring their outstanding close to the limit
4. Create a sale order that would push the total over the limit
5. Click "Confirm" — an approval request should be created
6. Log in as the supervisor and approve or reject the request

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|---------|
| SO confirms without approval | Customer has no classification | Assign a classification with block policy |
| No supervisor found | Sales team has no leader, user has no parent | Set team leader or user manager |
| Approval request not created | credit_policy is 'warning' not 'block' | Change classification credit policy |
| Email not sent | Mail server not configured | Configure outgoing mail server |
| Rejection reasons empty | Data not loaded | Check module data files, go to Rejection Reasons and create manually |