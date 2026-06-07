# Invoice Tracking Work Log

Date: 2026-04-30

## Changes Applied

- Added `readonly="status != 'draft'"` to editable fields in the `check.tracking` form view.
- Fields now readonly outside draft:
  - `partner_id`
  - `amount`
  - `currency_id`
  - `date_issue`
  - `date_due`
  - `bank_id`
  - `journal_id`
  - `attachment_ids`

## Files Changed

- `views/check_tracking_views.xml`

## Validation

Command:

```bash
python3 - <<'PY'
from lxml import etree
etree.parse('odoo/projects/magawish/invoice_tracking/views/check_tracking_views.xml')
print('XML OK')
PY
```

Result:

```text
XML OK
```

