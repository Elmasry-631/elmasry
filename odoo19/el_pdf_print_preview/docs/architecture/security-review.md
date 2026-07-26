# Security Review — el_pdf_print_preview

## 1. User Groups
No new groups — all users can configure their own preview settings.

## 2. Access Rights
No new models created — only extensions of res.users, ir.http, ir.actions.report.

## 3. Field-Level Security
- preview_print: exposed via SELF_READABLE_FIELDS + SELF_WRITEABLE_FIELDS
- automatic_printing: same
- Users can only read/write their OWN settings (enforced by Odoo core)

## 4. Controller Security
- /pdf_print_preview/get_report_name: auth='user' (must be logged in)
- records.check_read() called on browsed records (prevents IDOR)
- safe_eval used for print_report_name (matches Odoo core pattern)

## 5. Error Catcher Security
- Full traceback logged server-side via _logger.exception()
- Generic message shown to user in error PDF (no stack traces)
- Prevents information leakage (paths, model names, SQL)

## 6. JS Security
- No eval() or innerHTML usage
- PDF.js viewer runs in sandboxed iframe
- Report URLs built from server-side action data (not user input)
