# GAP Analysis — el_pdf_print_preview

## Requirement → Standard Module Mapping
| # | Requirement | Standard Module | Coverage | Custom Work? |
|---|-------------|-----------------|----------|--------------|
| 1 | PDF preview in browser | None (CE) | ❌ None | ✅ YES — PDF.js viewer + OWL dialog |
| 2 | Per-user toggle | base (res.users) | ⚠ Partial | ✅ YES — add fields + SELF_READABLE |
| 3 | Error catcher | None (CE) | ❌ None | ✅ YES — wrap _render_qweb_pdf |
| 4 | User menu entry | web (user_menuitems) | ✅ Full | ❌ NO — use registry |

## Build Scope
1. **Models to extend:** res.users, ir.http, ir.actions.report
2. **JS to build:** 3 files (handler, dialog, user menu)
3. **Reports to build:** 1 (error catcher)
4. **Standard modules to depend on:** base, web
