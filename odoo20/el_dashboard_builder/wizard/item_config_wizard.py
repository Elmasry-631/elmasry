# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DashboardItemConfigWizard(models.TransientModel):
    _name = 'dashboard.builder.item.config.wizard'
    _description = 'Dashboard Item Configuration Wizard'

    item_id = fields.Many2one(
        'dashboard.builder.item',
        string='Dashboard Item',
        required=True,
        ondelete='cascade',
    )
    widget_id = fields.Many2one(
        'dashboard.builder.widget',
        string='Widget',
        related='item_id.widget_id',
        readonly=True,
    )
    config_schema = fields.Json(
        string='Configuration Schema',
        related='widget_id.config_schema',
        readonly=True,
    )
    config = fields.Json(
        string='Configuration',
        default=lambda self: {},
    )
    config_fields = fields.Json(
        string='Form Fields',
        compute='_compute_config_fields',
    )

    @api.depends('widget_id', 'config_schema')
    def _compute_config_fields(self):
        for wizard in self:
            if wizard.widget_id and wizard.config_schema:
                wizard.config_fields = wizard.config_schema
            else:
                wizard.config_fields = {}

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if 'item_id' in res:
            item = self.env['dashboard.builder.item'].browse(res['item_id'])
            if item.exists():
                res['config'] = item.config or {}
        return res

    def action_save(self):
        """Save configuration to the dashboard item."""
        self.ensure_one()
        if self.item_id:
            self.item_id.write({'config': self.config})
        return {'type': 'ir.actions.act_window_close'}

    def action_reset(self):
        """Reset configuration to widget defaults."""
        self.ensure_one()
        if self.widget_id:
            self.config = self.widget_id.default_config.copy()
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }