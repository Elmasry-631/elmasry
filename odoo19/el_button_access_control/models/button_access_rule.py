"""Button Access Rule model — stores visibility rules for buttons."""

import json
import logging
from lxml import etree

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class ElButtonAccessRule(models.Model):
    _name = 'el.button.access.rule'
    _description = 'Button Access Control Rule'
    _order = 'sequence, model_id, id'

    name = fields.Char(
        string='Rule Name',
        required=True,
        translate=True,
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    model_id = fields.Many2one(
        comodel_name='ir.model',
        string='Target Model',
        required=True,
        ondelete='cascade',
    )
    model_name = fields.Char(
        related='model_id.model',
        string='Technical Model Name',
        store=True,
    )
    view_type = fields.Selection(
        selection=[
            ('form', 'Form View'),
            ('list', 'List View'),
            ('kanban', 'Kanban View'),
            ('all', 'All Views'),
        ],
        string='View Type',
        default='form',
        required=True,
    )

    button_name = fields.Selection(
        selection='_selection_button_name',
        string='Button Method',
        required=True,
    )
    button_string = fields.Char(
        string='Button Label',
        readonly=True,
    )

    mode = fields.Selection(
        selection=[
            ('show_only', 'Show Only to These Groups (Whitelist)'),
            ('hide_from', 'Hide from These Groups (Blacklist)'),
        ],
        string='Mode',
        default='show_only',
        required=True,
    )
    group_ids = fields.Many2many(
        comodel_name='res.groups',
        relation='el_button_access_rule_group_rel',
        column1='rule_id',
        column2='group_id',
        string='Groups',
    )

    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
        index=True,
    )

    _name_uniq = models.Constraint(
        'unique(model_id, view_type, button_name, mode, company_id)',
        'A rule with the same model, view type, button, and mode already exists for this company!',
    )

    @api.model
    def _selection_button_name(self):
        return []

    @api.onchange('model_id', 'view_type')
    def _onchange_model_view(self):
        if not self.model_id:
            self.button_name = ''
            self.button_string = ''
            return
        self.button_name = ''
        self.button_string = ''

    @api.onchange('button_name')
    def _onchange_button_name(self):
        if not self.button_name or not self.model_name:
            self.button_string = ''
            return
        buttons = self._scan_model_buttons()
        for name, label in buttons:
            if name == self.button_name:
                self.button_string = label
                return
        self.button_string = ''

    def action_scan_buttons(self):
        self.ensure_one()
        if not self.model_name:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Model Selected'),
                    'message': _('Please select a target model first.'),
                    'type': 'warning',
                    'sticky': False,
                },
            }
        buttons = self._scan_model_buttons()
        if not buttons:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('No Buttons Found'),
                    'message': _('No buttons found in %s %s views.') % (self.model_name, self.view_type),
                    'type': 'warning',
                    'sticky': False,
                },
            }
        lines = ['<b>%s</b> — %s' % (name, label or _('(no label)')) for name, label in buttons]
        message = '<br/>'.join(lines)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Available Buttons in %s (%s) — %d found') % (self.model_name, self.view_type, len(buttons)),
                'message': message,
                'type': 'info',
                'sticky': True,
                'next': {'type': 'ir.actions.client', 'tag': 'reload'},
            },
        }

    def _scan_model_buttons(self):
        self.ensure_one()
        model_name = self.model_name
        if not model_name:
            return []

        if self.view_type == 'all':
            view_types = ('form', 'list', 'kanban', 'tree')
        elif self.view_type == 'list':
            view_types = ('list', 'tree')
        else:
            view_types = (self.view_type,)

        domain = [
            ('model', '=', model_name),
            ('type', 'in', view_types),
            ('active', '=', True),
        ]

        views = self.env['ir.ui.view'].sudo().search(domain)
        button_map = {}

        for view in views:
            if not view.arch_db:
                continue
            try:
                arch = view.arch_db
                if isinstance(arch, dict):
                    arch = arch.get('en_US') or next(iter(arch.values()), '')
                if not arch:
                    continue
                root = etree.fromstring(arch.encode('utf-8') if isinstance(arch, str) else arch)
            except etree.XMLSyntaxError:
                continue

            for btn in root.iter('button'):
                btn_name = btn.get('name', '')
                if not btn_name:
                    continue
                btn_string = btn.get('string', '')
                if btn_name not in button_map:
                    button_map[btn_name] = btn_string

        return sorted(button_map.items())

    @api.model
    def rpc_get_available_buttons(self, model_id, view_type):
        if not model_id or not view_type:
            return []
        record = self.new({
            'model_id': model_id,
            'view_type': view_type,
        })
        buttons = record._scan_model_buttons()
        return [{'name': name, 'label': label or name} for name, label in buttons]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('button_name') and not vals.get('button_string'):
                vals['button_string'] = self._lookup_button_string(
                    vals.get('model_id'),
                    vals.get('view_type', 'form'),
                    vals['button_name'],
                )
        rules = super().create(vals_list)
        self.env.registry.clear_cache()
        return rules

    def write(self, vals):
        if 'button_name' in vals and 'button_string' not in vals:
            vals['button_string'] = self._lookup_button_string(
                self.model_id.id,
                vals.get('view_type', self.view_type),
                vals['button_name'],
            )
        result = super().write(vals)
        self.env.registry.clear_cache()
        return result

    def unlink(self):
        result = super().unlink()
        self.env.registry.clear_cache()
        return result

    def _lookup_button_string(self, model_id, view_type, button_name):
        if not model_id or not button_name:
            return ''
        rule = self.new({'model_id': model_id, 'view_type': view_type})
        buttons = rule._scan_model_buttons()
        for name, label in buttons:
            if name == button_name:
                return label
        return ''

    def action_test_rule(self):
        self.ensure_one()
        if not self.model_name:
            return
        target_model = self.env.get(self.model_name)
        if not target_model:
            return
        try:
            arch, view = target_model._get_view(
                view_type=self.view_type if self.view_type != 'all' else 'form',
            )
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Rule Test'),
                    'message': _('Rule "%s" is active. Check the %s view for %s.') % (
                        self.name, self.view_type, self.model_name,
                    ),
                    'type': 'success',
                    'sticky': False,
                },
            }
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Rule Test Failed'),
                    'message': str(e)[:200],
                    'type': 'danger',
                    'sticky': True,
                },
            }
