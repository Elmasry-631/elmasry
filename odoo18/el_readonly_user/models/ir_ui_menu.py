# -*- coding: utf-8 -*-
from odoo import api, models


_HIDDEN_MENU_NAMES = {
    'configuration',
    'settings',
    'الإعدادات',
    'التهيئة',
    'التكوين',
}

def _normalize(value):
    return (value or '').strip().casefold()


def _is_configuration_menu(menu):
    """Return True when a menu is a configuration/settings menu."""
    name = _normalize(menu.get('name')) if isinstance(menu, dict) else ''
    return (
        name in _HIDDEN_MENU_NAMES
        or 'configuration' in name
        or 'settings' in name
    )



class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def _el_readonly_hidden_menu_ids(self):
        menus = self.with_context(active_test=False).search([])
        hidden = menus.filtered(lambda menu: _is_configuration_menu({'name': menu.name}))
        hidden_ids = set(hidden.ids)
        all_menus = menus
        changed = True
        while changed:
            changed = False
            for menu in all_menus:
                if menu.id not in hidden_ids and menu.parent_id.id in hidden_ids:
                    hidden_ids.add(menu.id)
                    changed = True
        return hidden_ids

    @api.model
    def load_menus(self, debug):
        menus = super().load_menus(debug)
        if not self.env.user.has_group('el_readonly_user.group_users_readonly'):
            return menus

        hidden_ids = self._el_readonly_hidden_menu_ids()
        if not isinstance(menus, dict):
            return menus

        result = {key: dict(value) for key, value in menus.items() if key not in hidden_ids}
        for menu in result.values():
            children = menu.get('children')
            if isinstance(children, list):
                menu['children'] = [child for child in children if child not in hidden_ids]
        return result

    @api.model
    def load_web_menus(self, debug=False):
        parent = super()
        load_web_menus = getattr(parent, 'load_web_menus', None)
        if load_web_menus is None:
            return self.load_menus(debug)
        menus = load_web_menus(debug)
        if not self.env.user.has_group('el_readonly_user.group_users_readonly'):
            return menus
        hidden_ids = self._el_readonly_hidden_menu_ids()
        if isinstance(menus, dict):
            result = {key: dict(value) for key, value in menus.items() if key not in hidden_ids}
            for menu in result.values():
                children = menu.get('children')
                if isinstance(children, list):
                    menu['children'] = [child for child in children if child not in hidden_ids]
            return result
        return menus
