# Workflows — el_payroll_wps

## 1. Payslip Computation Workflow

```mermaid
sequenceDiagram
    actor HR as HR Officer
    participant PS as hr.payslip
    participant EP as el_payroll_wps (x_others)
    participant L as line_ids

    HR->>PS: Click "Compute Sheet"
    PS->>L: Populate payslip lines (NET/BASIC/HOUALLOW/ALW/DED)
    PS->>EP: super().compute_sheet() returns
    EP->>L: Read ALW total + DED total
    EP->>PS: Set x_others = ALW - DED
    PS->>HR: Form refreshed, x_others visible
    HR->>PS: (Optional) Manual edit x_others
    PS->>PS: Save — manual edit persists
```

## 2. Monthly WPS Export Workflow

```mermaid
sequenceDiagram
    actor HR as HR Officer
    participant M as Payroll menu
    participant W as wps.export.wizard
    participant PS as hr.payslip
    participant A as ir.attachment
    participant B as Browser

    HR->>M: Click "WPS Export"
    M->>W: Open wizard (modal)
    W->>HR: Form with month=today
    HR->>W: Pick month + click "Export CSV"
    W->>PS: search(date_from in month, state in validated/paid)
    alt no payslips
        PS-->>W: empty
        W-->>HR: UserError("No validated payslips for <Month Year>")
    else payslips exist
        PS-->>W: list of payslips
        loop for each slip
            W->>PS: _get_line_amount_by_code('NET'/'BASIC'/'HOUALLOW')
            W->>PS: _get_line_total_by_category('DED')
            W->>W: write CSV row
        end
        W->>A: create attachment (CSV bytes)
        W-->>B: ir.actions.act_url → /web/content/<id>?download=true
        B->>HR: File downloads as Salary_<Month>_<Year>.csv
    end
```

## 3. Module Installation Workflow

```mermaid
sequenceDiagram
    actor Admin as Administrator
    participant O as Odoo
    participant H as post_init_hook
    participant DB as ir.ui.menu

    Admin->>O: Install el_payroll_wps
    O->>O: Load manifest + create ACLs + create views
    O->>O: Static parent=hr_work_entry_enterprise.menu_hr_payroll_root
    O->>H: Run post_init_hook(env) [safety net]
    H->>DB: env.ref('el_payroll_wps.menu_wps_export')
    H->>DB: search parent_id=False, name='Payroll'
    alt found and current parent missing
        H->>DB: menu.write({parent_id: payroll_root.id})
    else static parent already worked
        H->>H: no-op
    end
    O-->>Admin: Installation complete
```

## 4. State Machines

**No state machines in this module.** `hr.payslip` has its own (`draft → verify → validated → paid → cancel`) but we don't modify it. The wizard is a single-step transient.
