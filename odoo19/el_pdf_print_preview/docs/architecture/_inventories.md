# Inventories — el_pdf_print_preview

## 1. Model Inventory
| # | Model | Type | Key Fields | Key Methods |
|---|-------|------|------------|-------------|
| 1 | res.users | _inherit | preview_print, automatic_printing | SELF_READABLE_FIELDS, SELF_WRITEABLE_FIELDS, action_preview_reload |
| 2 | ir.http | _inherit | (none) | session_info |
| 3 | ir.actions.report | _inherit | (none) | _render_qweb_pdf (error catcher) |

## 2. View Inventory
| View ID | Type | Model | Purpose |
|---------|------|-------|---------|
| view_users_pdf_preview_form | form inherit | res.users | Add preview toggles |

## 3. Controller Inventory
| Route | Method | Auth | Purpose |
|-------|--------|------|---------|
| /pdf_print_preview/get_report_name | jsonrpc | user | Get printable file name |

## 4. JS/OWL Inventory
| File | Purpose |
|------|---------|
| pdf_preview_handler.js | ir.actions.report handlers registry |
| pdf_preview_dialog.js | OWL Dialog component (PDF.js iframe) |
| user_menu.js | user_menuitems registry entry |
| pdf_preview_dialog.xml | OWL template for dialog |

## 5. Report Inventory
| Report | Type | Purpose |
|--------|------|---------|
| report_error_catcher | qweb-pdf | Fallback error PDF |
