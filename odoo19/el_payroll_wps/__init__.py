from . import models
from . import wizard


def post_init_hook(env):
    """Re-parent the 'WPS Export' menu under the actual Payroll app root
    menu. Done at runtime instead of a hardcoded XML id because the exact
    external id of the Payroll root menu differs between Odoo editions and
    versions, and guessing it wrong breaks module installation entirely."""
    our_menu = env.ref('el_payroll_wps.menu_wps_export', raise_if_not_found=False)
    if not our_menu:
        return

    Menu = env['ir.ui.menu']
    payroll_root = Menu.search([('parent_id', '=', False), ('name', '=', 'Payroll')], limit=1)
    if not payroll_root:
        payroll_root = Menu.search([('parent_id', '=', False), ('name', 'ilike', 'payroll')], limit=1)

    if payroll_root:
        our_menu.write({'parent_id': payroll_root.id})
