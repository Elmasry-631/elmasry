# EL Cheque Tracking — Implementation Report

**Date:** 2026-07-09
**Module:** `el_cheque_tracking`
**Version:** 19.0.1.0.0
**Odoo:** 19
**Author:** Ibrahim Elmasry

## Build summary

The `el_cheque_tracking` module was rebuilt from scratch (not copied from the
original `cheque_tracking` dump) using the Odoo Master Skill v10.30.32 BUILD
MODE workflow, with `examples/ie_sale_workflow` as the structural template.

## Models built

1. `cheque.cheque` — core model, 446 lines, 11 lifecycle methods.
2. `cheque.deposit` — batch deposit model.
3. `cheque.return` — return record model.
4. `cheque.return.reason` — config model.
5. `res.partner` extension — 5 computed fields via `read_group`.
6. `res.company` extension — 5 accounts + 4 thresholds.
7. `res.config.settings` extension — exposes all company cheque fields.
8. `account.move` extension — `cheque_id` + `cheque_stage`.
9. `account.payment` extension — `cheque_id` + consistency check.
10. `account.payment.register` extension.
11. `account.payment.method` extension.

## Accounting cycle implemented

### Received cheques
- Draft → Holding: posts receipt entry (Dr Cheques Received / Cr Receivable).
- Holding → Deposited: posts deposit entry (Dr Under Collection / Cr Cheques Received).
- Deposited → Cleared: posts clearance entry (Dr Bank / Cr Under Collection).
- Deposited/Cleared → Returned: reverses latest move + optional bank charges + penalty.
- Returned → Deposited (re-deposit): via batch deposit wizard, max-attempt validation.

### Issued cheques
- Draft → Approved: posts issue entry (Dr Payable / Cr Cheques Issued).
- Approved → Handed Over: records physical delivery (no entry).
- Handed Over → Cashed: posts cashing entry (Dr Cheques Issued / Cr Bank).
- Handed Over → Returned: reverses issued cheque liability.
- Draft/Approved/Handed-Over → Void: voiding path.

## Functional coverage

- Cheque lifecycle states, chatter tracking, activities, 3 SQL constraints,
  multi-company rules via record rules.
- Received & issued cheque list / form / kanban / calendar / pivot / graph views.
- Batch deposit wizard, return wizard (with bank charges + penalty), print wizard.
- Return reason configuration with 4 default records.
- Partner cheque stat buttons (received count, issued count, bounced count, totals).
- PDC maturity + stale-cheque scheduled actions.
- Cheque print, deposit slip, cheque register QWeb PDF reports.
- Settings page for required accounting accounts + 4 lifecycle thresholds.
- 25 comprehensive tests covering lifecycle, accounting, wizards, security,
  multi-company, cron jobs, and reports.

## Validation

- Python syntax check: PASS (all 20 .py files compile cleanly).
- XML parse check: PASS (all 21 .xml files parse cleanly).
- Manifest `ast.literal_eval`: PASS.
- Skill validator (`validate_module.py --odoo-version 19`): see `build-report.md`.
- Tests: see `testing.md` + `build-report.md` for Docker runtime results.

## Notes

- Bank-specific cheque layout coordinates are represented by a standard QWeb
  cheque template; per-bank coordinate configuration can be added as a future
  extension model.
- The `cheque.*` namespace is used for all custom models (intentional design
  decision — see `alignment-decision.md`).
