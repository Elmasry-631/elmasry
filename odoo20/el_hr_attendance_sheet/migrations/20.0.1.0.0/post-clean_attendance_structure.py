# -*- coding: utf-8 -*-
"""Drop the salary rules the attendance structure inherited from
hr_payroll.default_structure.

``hr.payroll.structure.rule_ids`` copies every rule of the default structure
when a structure is created, so the Attendance Structure used to also carry
BASIC, GROSS, NET and friends. Double-counting those on a payslip is wrong,
and this script removes them on upgrade.

A rule referenced by a payslip line cannot be deleted (foreign key), so any
such rule is kept and logged instead of failing the whole upgrade.
"""
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

ATTENDANCE_RULE_CODES = ('OVERT', 'LATE', 'ABS', 'DIFF')


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    structure = env.ref(
        'el_hr_attendance_sheet.structure_attendance', raise_if_not_found=False)
    if not structure or structure.code != 'ATT':
        return

    inherited = structure.rule_ids.filtered(
        lambda r: r.code not in ATTENDANCE_RULE_CODES)
    if not inherited:
        return

    used_rule_ids = env['hr.payslip.line'].search([
        ('salary_rule_id', 'in', inherited.ids),
    ]).mapped('salary_rule_id')
    blocked = inherited.filtered(lambda r: r in used_rule_ids)
    removable = inherited - blocked

    if removable:
        codes = ', '.join(removable.mapped('code'))
        removable.unlink()
        _logger.info(
            "Attendance Structure: removed inherited rules: %s.", codes)

    if blocked:
        codes = ', '.join(blocked.mapped('code'))
        _logger.warning(
            "Attendance Structure: kept inherited rule(s) still referenced by "
            "payslip lines: %s. Delete those draft payslips and upgrade again "
            "to finish the cleanup.", codes)