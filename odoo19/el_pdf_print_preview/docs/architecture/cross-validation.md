# Cross-Validation — el_pdf_print_preview

## PRE-A: Fields in Views → Model ✅
- preview_print: exists in res.users ✓
- automatic_printing: exists in res.users ✓

## PRE-B: Buttons → Methods ✅
- action_preview_reload: method exists ✓

## PRE-C: __init__.py Import Chain ✅
- __init__.py → models + controllers ✓
- models/__init__.py → res_users + ir_http + ir_actions_report ✓
- controllers/__init__.py → main ✓

## PRE-D: Manifest Paths on Disk ✅
- security/ir.model.access.csv ✓
- views/res_users_views.xml ✓
- report/ir_actions_report_templates.xml ✓
- report/ir_actions_report.xml ✓

## PRE-E: OWL Component Wiring ✅
- pdf_preview_dialog.js: Component + template + props ✓
- pdf_preview_dialog.xml: template registered ✓
