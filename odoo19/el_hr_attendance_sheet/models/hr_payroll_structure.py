# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

ATTENDANCE_STRUCTURE_CODE = 'ATT'
ATTENDANCE_RULE_CODES = ('OVERT', 'LATE', 'ABS', 'DIFF')


class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'

    @api.model_create_multi
    def create(self, vals_list):
        """Create the attendance structure without the inherited rules.

        ``hr.payroll.structure.rule_ids`` defaults to a copy of every rule of
        ``hr_payroll.default_structure`` (BASIC, GROSS, NET, ...). Those copies
        double-count the employee's salary on any payslip using this
        structure, so it is created with an empty rule list. Its four
        attendance rules attach themselves through their ``struct_id`` field.
        """
        for vals in vals_list:
            if vals.get('code') == ATTENDANCE_STRUCTURE_CODE:
                vals['rule_ids'] = [fields.Command.clear()]
        return super().create(vals_list)

    def _is_attendance_structure(self):
        self.ensure_one()
        return self.code == ATTENDANCE_STRUCTURE_CODE

    def action_clean_inherited_rules(self):
        """Remove rules copied from the default structure, when safe to do so.

        Deleting a rule that a payslip line still references raises a foreign
        key violation, so such a rule is kept and logged instead. Used by the
        post-install hook, never from a data file.
        """
        structures = self.filtered(lambda s: s._is_attendance_structure())
        removed = self.env['hr.salary.rule'].browse()
        for structure in structures:
            inherited = structure.rule_ids.filtered(
                lambda r: r.code not in ATTENDANCE_RULE_CODES)
            if not inherited:
                continue
            used_rule_ids = self.env['hr.payslip.line'].search([
                ('salary_rule_id', 'in', inherited.ids),
            ]).mapped('salary_rule_id')
            blocked = inherited.filtered(lambda r: r in used_rule_ids)
            if blocked:
                _logger.warning(
                    "Attendance structure '%s': kept inherited rule(s) %s "
                    "because payslip lines still reference them. Delete the "
                    "related draft payslips and upgrade again to clean them up.",
                    structure.code, ', '.join(blocked.mapped('code')),
                )
            removable = inherited - blocked
            if removable:
                _logger.info(
                    "Attendance structure '%s': removed inherited rule(s) %s.",
                    structure.code, ', '.join(removable.mapped('code')),
                )
                removable.unlink()
                removed |= removable
        return removed

    def action_propagate_attendance_rules(self):
        """Copy the attendance rules into the other payroll structures.

        A payslip applies a single structure, so an employee cannot get the
        overtime / lateness / absence lines from a separate "Attendance
        Structure" — those rules have to sit in the same structure as the
        basic salary. This copies them into every other structure, skipping
        the ones that already carry the code so the action is idempotent.
        """
        source = self.env.ref(
            'el_hr_attendance_sheet.structure_attendance',
            raise_if_not_found=False,
        )
        if not source:
            return self.browse()
        codes = ['OVERT', 'LATE', 'ABS']
        targets = self.search([('id', '!=', source.id)])
        added = self.env['hr.salary.rule'].browse()
        for structure in targets:
            for code in codes:
                if structure.rule_ids.filtered(
                        lambda r, c=code: r.code == c):
                    continue
                model = source.rule_ids.filtered(
                    lambda r, c=code: r.code == c)[:1]
                if not model:
                    _logger.warning(
                        "No source '%s' rule to propagate.", code)
                    continue
                rule = model.copy({'struct_id': structure.id})
                added |= rule
                _logger.info(
                    "Propagated '%s' to structure '%s'.", code, structure.name)
        return added