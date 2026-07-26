# Testing — el_pdf_print_preview

## Test Plan
| # | Test Method | What it Tests |
|---|-------------|---------------|
| 1 | test_01_preview_print_field_exists | Field exists |
| 2 | test_02_preview_print_default_true | Default value |
| 3 | test_03_automatic_printing_default_false | Default value |
| 4 | test_04_toggle_preview_print | Write works |
| 5 | test_05_readable_fields | SELF_READABLE_FIELDS |
| 6 | test_06_writeable_fields | SELF_WRITEABLE_FIELDS |
| 7 | test_07_preview_reload_action | Action returns reload |
| 8 | test_08_session_info_has_preview_fields | ir.http override |
| 9 | test_09_report_override_exists | _render_qweb_pdf override |
| 10 | test_10_controller_exists | Controller method |
| 11 | test_11_error_catcher_template | QWeb template |
| 12 | test_12_error_catcher_action | ir.actions.report record |
| 13 | test_13_module_installed | Module state |

## Test Results
- L1 (Install): ✅ PASS
- L2 (Tests): ✅ 13/13 PASS (0 failed, 0 errors)
