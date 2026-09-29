# Alignment Decision — el_hospital

## Alignment with Odoo Philosophy

This module follows Odoo's modular philosophy:
1. **Reuse, don't rebuild**: leverage res.partner, hr.employee, product.product, account.move
2. **Conventions over configuration**: sequence codes, state machines, smart buttons
3. **Security first**: 7 role-based groups + record rules + field-level ACL
4. **User experience**: kanban for physicians, calendar for appointments, dashboard

## Key Design Decisions

### D1: Patient = res.partner wrapper (not inheriting)
**Decision**: `hospital.patient` has `partner_id` (M2O res.partner) and uses
related fields for contact info.
**Rationale**: Decouples medical data from contact data. A partner can be both
patient and supplier (e.g., insurance company) without conflicts.
**Alternative rejected**: `_inherit = 'res.partner'` — pollutes res.partner
with medical fields, breaks if partner has multiple roles.

### D2: Physician = separate model linked to hr.employee
**Decision**: `hospital.physician` is a standalone model with optional
`employee_id` link to hr.employee.
**Rationale**: Not all physicians are employees (visiting consultants).
Keeps medical-specific data (license, specialization) separate from HR.

### D3: Billing wraps account.move (not inherits)
**Decision**: `hospital.invoice.billing` has `move_id` (M2O account.move).
The `action_create_invoice` method creates a draft account.move and links it.
**Rationale**: Follows Odoo's pattern (like sale.order → invoice). Allows
flexibility in invoice management via standard accounting.

### D4: Dashboard as OWL client action (not form view)
**Decision**: Dashboard is an OWL component fetching data via JSON controller.
**Rationale**: Follows LAW 21-25 (dashboard design system). Chart.js
lazy-loaded, memory-safe.

### D5: Bed state managed by admission (not free-form)
**Decision**: `action_admit` sets bed to occupied; `action_discharge` frees it.
**Rationale**: Prevents inconsistent states (occupied bed with no patient).

### D6: Sequences for all operational models
**Decision**: All operational models use `ir.sequence` for readable codes.
**Rationale**: Professional appearance, easier reference in communication.

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Stock dispensing not in v1 | High | Low | Documented as v2 feature; billing captures cost |
| Insurance workflow complex | Medium | Medium | Deferred to v2; billing supports manual insurance field |
| Performance with many patients | Low | Medium | Stored computed fields + read_group for dashboard |
| Multi-company edge cases | Low | Low | Record rules + company_id on all models |
