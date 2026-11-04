"""Others = other allowances (allowances except housing) on existing payslips.

Version 19.0.1.0.0 computed Allowances - Deductions (deductions are negative,
so they were added) and only on payslips computed after the installation.
"""
from odoo import SUPERUSER_ID, api


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for slip in env['hr.payslip'].search([('line_ids', '!=', False)]):
        others = slip._wps_amounts()['others']
        if slip.x_others != others:
            cr.execute("UPDATE hr_payslip SET x_others = %s WHERE id = %s", (others, slip.id))
