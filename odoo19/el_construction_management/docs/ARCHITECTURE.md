# Technical Architecture

## Application layers
- Models: business rules, workflows, computed values, integrations.
- Views: list/form/search/Gantt and navigation.
- Security: ACLs, record rules, manager controls.
- Data: sequences and configuration defaults.
- Reports: QWeb reporting and report wizard.
- Static assets: dashboard and lightweight form UX styling.
- Tests: Python transactional/unit coverage where provided.

## Extension strategy
The module uses Odoo ORM inheritance and avoids modifications to Odoo core. Odoo 19 compatibility requires current APIs such as `models.Constraint` and the `list` view architecture.

## Inventory integration
Construction records reference Odoo stock locations/moves/pickings/scraps and valuation layers. No second stock engine is introduced.

## UX strategy
Navigation is organized by user job-to-be-done. Forms are organized into semantic sections and notebooks so users see context first, operational data second, and detailed lines/evidence in dedicated tabs.
