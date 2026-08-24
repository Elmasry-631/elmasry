# Testing Documentation

## Test Plan

The module includes 8 test cases in `tests/test_credit_approval.py` that cover the core workflow paths. All tests use `TransactionCase` for database isolation.

## Test Setup (setUpClass)

A shared test environment is created once per test class:
- **Partner**: A company contact with `payment_type='credit'` and `customer_rank=1`
- **Classification**: A test classification with `credit_limit=1000.0` and `credit_policy='block'`
- **Product**: A consumable product priced at 600.0
- **Sale Order**: A draft SO linked to the test partner with one order line (total: 600.0)
- **Rejection Reason**: A test rejection reason for use in rejection tests

The credit scenario is: limit=1000, outstanding=800, order=600, projected=1400, exceeded=400.

## Test Cases

### Test 01: Rejection Reason Creation
- **What:** Creates a new `credit.rejection.reason` record
- **Validates:** The reason is active by default, and the company is auto-set to the current company
- **Expected:** No errors, `active=True`, `company_id` matches

### Test 02: Approval Request Creation
- **What:** Calls `_create_from_sale_order()` with a credit-exceeded SO (partner.credit set to 800)
- **Validates:** Request is created in 'submitted' state, partner matches, SO is linked, exceeded_by > 0, name is auto-generated (not 'New')
- **Expected:** `state='submitted'`, `exceeded_by=400.0`, name like 'CR/00001'

### Test 03: Approval Confirms Sale Order
- **What:** Creates a request, then calls `action_approve()`
- **Validates:** Request state becomes 'approved', SO credit_approval_state becomes 'approved'
- **Note:** The actual SO confirmation may fail in test environment due to missing stock/routes, but the approval logic is verified
- **Expected:** `request.state='approved'`, `so.credit_approval_state='approved'`

### Test 04: Reject Without Reason Raises Error
- **What:** Creates a request and calls `action_reject()` without setting `rejection_reason_id`
- **Validates:** A `ValidationError` is raised
- **Expected:** `ValidationError` with message about selecting a reason

### Test 05: Reject With Predefined Reason
- **What:** Creates a request, sets `rejection_reason_id`, then calls `action_reject()`
- **Validates:** State becomes 'rejected', the reason is preserved, SO state becomes 'rejected'
- **Expected:** `state='rejected'`, `rejection_reason_id` matches, `so.credit_approval_state='rejected'`

### Test 06: Resubmit Rejected Request
- **What:** Rejects a request, then calls `action_resubmit()`
- **Validates:** State resets to 'draft', rejection_reason_id is cleared, rejection_notes is cleared
- **Expected:** `state='draft'`, `rejection_reason_id=False`, `rejection_notes=False`

### Test 07: Warning Policy Allows Confirm
- **What:** Changes classification credit_policy to 'warning' and verifies the logic path
- **Validates:** The partner's credit_policy is 'warning', meaning the SO should not be blocked
- **Expected:** `partner.credit_policy == 'warning'` — no block applied

### Test 08: Cash Customer Not Blocked
- **What:** Sets partner payment_type to 'cash' and checks `is_credit_blocked`
- **Validates:** Cash customers are never credit-blocked regardless of their outstanding balance
- **Expected:** `is_credit_blocked=False`

## Running Tests

```bash
# Full module test
odoo --test-enable --test-tags=/el_nmo_credit_approval \
    -i el_nmo_credit_approval --stop-after-init -d test_db

# Single test case
odoo --test-enable --test-tags=/el_nmo_credit_approval:test_credit_approval \
    -i el_nmo_credit_approval --stop-after-init -d test_db
```

## Testing Notes

- Tests depend on `el_nmo_classification` being installed (the `customer.classification` model)
- The test environment uses Odoo's test database with demo data
- Test 03 may produce a log about SO confirmation failure — this is expected in test isolation and does not indicate a module defect