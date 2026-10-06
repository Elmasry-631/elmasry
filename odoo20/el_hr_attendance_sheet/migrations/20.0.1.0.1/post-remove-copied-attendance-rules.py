# -*- coding: utf-8 -*-
"""Remove the ``<CODE>_COPY`` attendance salary rules.

Odoo 20 renames ``hr.salary.rule.category_id`` to ``category_ids`` and suffixes
the code of every copied rule with ``_COPY`` (``hr.salary.rule.copy_data``).
The rule propagation therefore created ``OVERT_COPY`` / ``LATE_COPY`` /
``ABS_COPY`` rules in the other payroll structures instead of real ``OVERT`` /
``LATE`` / ``ABS`` ones, so attendance amounts were never computed. The
propagation is fixed on the Python side; this script drops the leftovers.

A rule still referenced by a payslip line cannot be deleted (foreign key), so
any such rule is kept and logged instead of failing the whole upgrade.
"""
import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

LEGACY_CODES = ('OVERT_COPY', 'LATE_COPY', 'ABS_COPY', 'DIFF_COPY')


def migrate(cr, version):
    if not version:
        return

    env = api.Environment(cr, SUPERUSER_ID, {})
    legacy = env['hr.salary.rule'].search([('code', 'in', LEGACY_CODES)])
    if not legacy:
        return

    used_rule_ids = env['hr.payslip.line'].search([
        ('salary_rule_id', 'in', legacy.ids),
    ]).mapped('salary_rule_id')
    blocked = legacy.filtered(lambda r: r in used_rule_ids)
    removable = legacy - blocked

    if removable:
        codes = ', '.join(removable.mapped('code'))
        removable.unlink()
        _logger.info(
            "Attendance rules: removed duplicated rules: %s. Run the "
            "'Add Attendance Rules' server action to add the real ones.", codes)

    if blocked:
        codes = ', '.join(blocked.mapped('code'))
        _logger.warning(
            "Attendance rules: kept duplicated rule(s) still referenced by "
            "payslip lines: %s. Delete those draft payslips and upgrade again "
            "to finish the cleanup.", codes)
