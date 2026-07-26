# Requirements Specification — el_pdf_print_preview

## 1. Overview
- **Module Name:** el_pdf_print_preview
- **Target Odoo Version:** 19
- **Category:** Extra Tools/Usability
- **Summary:** Preview PDF reports in-browser via PDF.js viewer — no download needed
- **Author:** Ibrahim Elmasry

## 2. Business Problem
When users click Print in Odoo, the PDF downloads to their device. They must
manually open the file and use Ctrl+P to print. This is slow and confusing,
especially for non-technical users.

## 3. Functional Requirements

### 3.1 Models
| # | Model | Purpose | Inherits | Key Fields |
|---|-------|---------|----------|------------|
| 1 | res.users (ext) | Add preview toggles | _inherit='res.users' | preview_print, automatic_printing |
| 2 | ir.http (ext) | Inject session_info | _inherit='ir.http' | (no new fields) |
| 3 | ir.actions.report (ext) | Error catcher | _inherit='ir.actions.report' | (no new fields) |

### 3.2 Views
| View ID | Type | Model | Purpose |
|---------|------|-------|---------|
| view_users_pdf_preview_form | form inherit | res.users | Add preview toggles |

### 3.3 Security
No new groups — all users can configure their own preview settings.
SELF_READABLE_FIELDS + SELF_WRITEABLE_FIELDS expose the toggles.

### 3.4 Reports
| Report | Model | Type | Purpose |
|--------|-------|------|---------|
| report_error_catcher | res.users | PDF | Fallback error PDF |

### 3.5 Client-side (JS/OWL)
| File | Purpose |
|------|---------|
| pdf_preview_handler.js | Registers in ir.actions.report handlers registry |
| pdf_preview_dialog.js | OWL Dialog component with PDF.js iframe |
| user_menu.js | User menu entry for settings |

## 4. Non-Functional Requirements
- **Performance:** PDF.js loads in <2s, dialog opens in <500ms
- **Multi-company:** Not applicable (per-user setting)
- **i18n:** Arabic + English
- **Security:** No stack traces in error PDFs; user can only read/write own settings

## 5. Dependencies
| Module | Reason |
|--------|--------|
| base | Required |
| web | Required for OWL/Dialog/action service |

## 6. Constraints
- NO Enterprise dependencies (CE compatible)
- NO deprecated patterns (Odoo 19+)
- Author: Ibrahim Elmasry (LAW 18)
- PDF.js viewer bundled (v2.2.0 — upgrade planned for v2.0)

## 7. Acceptance Criteria
- [x] Module installs without errors on Odoo 19
- [x] All 13 tests pass
- [x] Pre-flight validation: 0 errors
- [x] Documentation: 7+ files in docs/
- [x] Arabic translations: 10+ entries
- [x] Module icon: 256×256 PNG < 100KB

## 8. Requirements Traceability Matrix
| # | Requirement | Model.Field | View | Test Method |
|---|-------------|-------------|------|-------------|
| 1 | preview_print field | res.users.preview_print | form inherit | test_01 |
| 2 | Default True | res.users.preview_print | — | test_02 |
| 3 | automatic_printing field | res.users.automatic_printing | form inherit | test_03 |
| 4 | Default False | res.users.automatic_printing | — | test_04 (implicit) |
| 5 | Toggle works | res.users.preview_print | — | test_04 |
| 6 | SELF_READABLE_FIELDS | res.users property | — | test_05 |
| 7 | SELF_WRITEABLE_FIELDS | res.users property | — | test_06 |
| 8 | Reload action | res.users.action_preview_reload | — | test_07 |
| 9 | session_info override | ir.http.session_info | — | test_08 |
| 10 | Error catcher | ir.actions.report._render_qweb_pdf | — | test_09 |
| 11 | Controller | PrintPreviewController | — | test_10 |
| 12 | Error template | report_error_catcher | XML | test_11 |
| 13 | Error action | action_report_error_catcher | XML | test_12 |
