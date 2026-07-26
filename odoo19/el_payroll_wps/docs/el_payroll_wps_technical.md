# El Payroll Wps — Technical Reference

> Generated: 2026-07-26 07:11

## Architecture

```

el_payroll_wps/
├── __init__.py
├── __manifest__.py
├── docs/
│   ├── architecture
│   ├── architecture.md
│   ├── build-report.md
│   ├── configuration-guide.md
│   ├── el_payroll_wps_technical.md
│   └── ... (18 files)
├── i18n/
│   ├── ar.po
├── models/
│   ├── __init__.py
│   ├── hr_payslip.py
├── security/
│   ├── ir.model.access.csv
├── static/
│   ├── description
├── tests/
│   ├── __init__.py
│   ├── test_wps_export.py
├── views/
│   ├── hr_payslip_views.xml
├── wizard/
│   ├── __init__.py
│   ├── wps_export_wizard.py
│   ├── wps_export_wizard_views.xml
```

## View Reference

| View ID | Type | Model | Fields | File |
|---|---|---|---|---|
| `view_hr_payslip_form_inherit_wps` | form | `hr.payslip` | - | hr_payslip_views.xml |

## Security Reference

### Access Rules

| ID | Model | R | W | C | U |
|---|---|---|---|---|---|
| `access_wps_export_wizard_user` | `wps.export.wizard` | Y | Y | Y | Y |
| `access_wps_export_wizard_admin` | `wps.export.wizard` | Y | Y | Y | Y |
