"""Base model extension — overrides _get_view to apply button access rules."""

import logging
from lxml import etree

from odoo import api, models

_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    _inherit = 'base'
    _description = 'Base (Button Access Control Extension)'

    @api.model
    def _get_view(self, view_id=None, view_type='form', **options):
        arch, view = super()._get_view(view_id, view_type=view_type, **options)

        if view_type not in ('form', 'list', 'kanban', 'tree'):
            return arch, view

        try:
            arch = self._el_apply_button_access_rules(arch, view_type)
        except Exception as e:
            _logger.warning(
                'el_button_access_control: error applying rules to %s: %s',
                self._name, e,
            )

        return arch, view

    def _el_apply_button_access_rules(self, arch, view_type):
        rule_model = self.env.get('el.button.access.rule')
        if not rule_model:
            return arch

        try:
            rule_model.search([], limit=1)
        except Exception:
            return arch

        model_name = self._name

        domain = [
            ('model_name', '=', model_name),
            ('active', '=', True),
            '|', ('view_type', '=', view_type), ('view_type', '=', 'all'),
        ]
        rules = rule_model.search(domain)

        if not rules:
            return arch

        if not arch:
            return arch

        try:
            root = etree.fromstring(arch.encode('utf-8') if isinstance(arch, str) else arch)
        except etree.XMLSyntaxError:
            return arch

        modified = False

        for rule in rules:
            buttons = root.xpath(f"//button[@name='{rule.button_name}']")
            for button in buttons:
                if rule.mode == 'show_only':
                    new_groups = ','.join(rule.group_ids.mapped('xml_id'))
                    if not new_groups:
                        continue

                    existing_groups = button.get('groups', '')
                    if existing_groups:
                        existing_set = {g.strip() for g in existing_groups.split(',') if g.strip()}
                        new_set = {g.strip() for g in new_groups.split(',') if g.strip()}
                        combined = ','.join(sorted(existing_set & new_set))
                        button.set('groups', combined)
                    else:
                        button.set('groups', new_groups)

                    modified = True

                elif rule.mode == 'hide_from':
                    group_xml_ids = rule.group_ids.mapped('xml_id')
                    if not group_xml_ids:
                        continue

                    checks = [f"user.has_group('{gid}')" for gid in group_xml_ids]
                    invisible_expr = ' or '.join(checks)

                    existing_invisible = button.get('invisible', '')
                    if existing_invisible:
                        combined = f"({existing_invisible}) or ({invisible_expr})"
                        button.set('invisible', combined)
                    else:
                        button.set('invisible', invisible_expr)

                    modified = True

        if modified:
            return etree.tostring(root, encoding='unicode')
        return arch
