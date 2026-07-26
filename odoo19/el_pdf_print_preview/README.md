# el_pdf_print_preview

Preview PDF reports in-browser before printing — no download needed.
Built for Odoo 19 using PDF.js viewer.

## Features

- **In-browser PDF preview** via PDF.js viewer in an OWL Dialog
- **Per-user toggle**: preview on/off (default: on)
- **Per-user toggle**: automatic printing (default: off)
- **Error catcher**: if report fails, shows friendly error PDF
- **User menu entry**: quick settings access from top-right menu

## How It Works

1. Registers a handler in `ir.actions.report handlers` registry
2. When a qweb-pdf report is triggered:
   - Fetches the PDF via standard `/report/pdf/` endpoint
   - Opens it in PDF.js viewer inside an OWL Dialog
   - User can preview, print, or download
3. If automatic printing is on: opens print window with proper load delay

## Installation

1. Copy `el_pdf_print_preview` to your Odoo addons directory
2. Restart Odoo
3. Install via Apps menu

## Test Results

- **L1 (Install)**: ✅ PASS
- **L2 (Tests)**: ✅ 13/13 PASS

## Bug Fixes vs Original Module

| Bug | Original | Fixed |
|---|---|---|
| Action handler registration | Wrong registry key | `ir.actions.report handlers` (correct O19 pattern) |
| Dialog service call | `registry.get("dialog").add()` (broken) | `env.services.dialog.add()` (correct) |
| Dialog title | `title="props.title"` (literal string) | `t-att-title="dialogTitle"` (expression) |
| Print race condition | `window.open(url).print()` (fails) | `setTimeout` + `readyState` check |
| User menu action | `action_id: "xml.id"` (expects int) | `doAction({res_model, res_id})` directly |
| Mutable default arg | `data={}` | `data=None` |
| Security leak | Full traceback in error PDF | Generic message + server-side logging |
| Dead files | `assets.xml`, `content.xml`, `user_menu.xml`, `.less` | Deleted |
| PDF.js version | 2.2.0 (2018, security risk) | Kept (upgrade planned for v2.0) |
| O19 field names | `_get_self_readable_fields()` | `SELF_READABLE_FIELDS` property |

## Author

Ibrahim Elmasry
