# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import json


class Dashboard(models.Model):
    _name = 'dashboard.builder'
    _description = 'Dashboard Builder'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(
        string='Dashboard Name',
        required=True,
        tracking=True,
        translate=True,
    )
    description = fields.Html(
        string='Description',
        translate=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Owner',
        default=lambda self: self.env.user,
        required=True,
        tracking=True,
    )
    is_public = fields.Boolean(
        string='Public Dashboard',
        default=False,
        tracking=True,
        help='If checked, this dashboard is visible to all users with access rights.',
    )
    group_ids = fields.Many2many(
        'res.groups',
        'dashboard_builder_group_rel',
        'dashboard_id', 'group_id',
        string='Allowed Groups',
        help='Groups that can view this dashboard. Empty means all users with dashboard access.',
    )
    layout_config = fields.Json(
        string='Layout Configuration',
        default=lambda self: {
            'columns': 12,
            'rowHeight': 100,
            'margin': [10, 10],
            'containerPadding': [10, 10],
            'breakpoints': {
                'lg': 1200,
                'md': 996,
                'sm': 768,
                'xs': 480,
                'xxs': 0,
            },
            'cols': {
                'lg': 12,
                'md': 10,
                'sm': 6,
                'xs': 4,
                'xxs': 2,
            },
        },
        help='Grid layout configuration for the dashboard.',
    )
    item_ids = fields.One2many(
        'dashboard.builder.item',
        'dashboard_id',
        string='Dashboard Items',
        copy=True,
    )
    item_count = fields.Integer(
        string='Item Count',
        compute='_compute_item_count',
        store=True,
    )
    last_viewed = fields.Datetime(
        string='Last Viewed',
        readonly=True,
    )
    view_count = fields.Integer(
        string='View Count',
        default=0,
        readonly=True,
    )
    background_color = fields.Char(
        string='Background Color',
        default='#f5f6f8',
        help='CSS color for dashboard background.',
    )
    background_image = fields.Binary(
        string='Background Image',
        attachment=True,
    )
    custom_css = fields.Text(
        string='Custom CSS',
        help='Custom CSS for dashboard styling.',
    )
    refresh_interval = fields.Integer(
        string='Auto Refresh (seconds)',
        default=0,
        help='Auto refresh interval in seconds. 0 means disabled.',
    )
    filter_domain = fields.Char(
        string='Global Filter Domain',
        help='Global domain filter applied to all widgets. Example: [("state", "=", "active")]',
    )
    filter_context = fields.Json(
        string='Global Filter Context',
        default=lambda self: {},
        help='Global context applied to all widgets.',
    )
    tag_ids = fields.Many2many(
        'dashboard.builder.tag',
        string='Tags',
    )
    is_favorite = fields.Boolean(
        string='Favorite',
        compute='_compute_is_favorite',
        search='_search_is_favorite',
    )
    favorite_user_ids = fields.Many2many(
        'res.users',
        'dashboard_builder_favorite_rel',
        'dashboard_id', 'user_id',
        string='Favorited By',
    )
    share_ids = fields.One2many(
        'dashboard.builder.share',
        'dashboard_id',
        string='Shares',
    )

    @api.depends('item_ids')
    def _compute_item_count(self):
        for dashboard in self:
            dashboard.item_count = len(dashboard.item_ids)

    @api.depends('favorite_user_ids')
    def _compute_is_favorite(self):
        current_user = self.env.user
        for dashboard in self:
            dashboard.is_favorite = current_user in dashboard.favorite_user_ids

    def _search_is_favorite(self, operator, value):
        if operator not in ('=', '!=') or not isinstance(value, bool):
            raise UserError(_('Invalid search operation for favorites'))
        current_user = self.env.user
        if (operator == '=' and value) or (operator == '!=' and not value):
            return [('favorite_user_ids', 'in', current_user.ids)]
        return [('favorite_user_ids', 'not in', current_user.ids)]

    @api.constrains('layout_config')
    def _check_layout_config(self):
        for record in self:
            if record.layout_config:
                required_keys = ['columns', 'rowHeight', 'margin', 'cols']
                for key in required_keys:
                    if key not in record.layout_config:
                        raise ValidationError(_('Layout config missing required key: %s') % key)

    def action_open_dashboard(self):
        """Open the dashboard in view mode."""
        self.ensure_one()
        self.write({
            'last_viewed': fields.Datetime.now(),
            'view_count': self.view_count + 1,
        })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/dashboard/builder/{self.id}',
            'target': 'self',
        }

    def action_edit_dashboard(self):
        """Open the dashboard in edit mode."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/dashboard/builder/{self.id}/edit',
            'target': 'self',
        }

    def action_duplicate(self):
        """Duplicate the dashboard with all items."""
        self.ensure_one()
        new_dashboard = self.copy({
            'name': _('%s (Copy)') % self.name,
            'is_public': False,
            'user_id': self.env.user.id,
        })
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'dashboard.builder',
            'res_id': new_dashboard.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_toggle_favorite(self):
        """Toggle favorite status for current user."""
        self.ensure_one()
        if self.env.user in self.favorite_user_ids:
            self.write({'favorite_user_ids': [(3, self.env.user.id)]})
        else:
            self.write({'favorite_user_ids': [(4, self.env.user.id)]})
        return True

    def action_export_config(self):
        """Export dashboard configuration as JSON."""
        self.ensure_one()
        config = {
            'name': self.name,
            'description': self.description,
            'layout_config': self.layout_config,
            'background_color': self.background_color,
            'custom_css': self.custom_css,
            'refresh_interval': self.refresh_interval,
            'filter_domain': self.filter_domain,
            'filter_context': self.filter_context,
            'items': [],
        }
        for item in self.item_ids:
            config['items'].append({
                'widget_id': item.widget_id.xml_id if item.widget_id else None,
                'widget_name': item.widget_id.name if item.widget_id else item.custom_widget_name,
                'position': {
                    'x': item.pos_x,
                    'y': item.pos_y,
                    'w': item.width,
                    'h': item.height,
                },
                'config': item.config,
                'filters': item.filters,
                'context': item.context,
            })
        return {
            'type': 'ir.actions.act_url',
            'url': f'/dashboard/builder/export/{self.id}',
            'target': 'self',
        }

    @api.model
    def import_dashboard_config(self, config_data):
        """Import dashboard from JSON configuration."""
        dashboard = self.create({
            'name': config_data.get('name', _('Imported Dashboard')),
            'description': config_data.get('description'),
            'layout_config': config_data.get('layout_config', {}),
            'background_color': config_data.get('background_color', '#f5f6f8'),
            'custom_css': config_data.get('custom_css'),
            'refresh_interval': config_data.get('refresh_interval', 0),
            'filter_domain': config_data.get('filter_domain'),
            'filter_context': config_data.get('filter_context', {}),
        })
        for item_data in config_data.get('items', []):
            widget = None
            if item_data.get('widget_id'):
                widget = self.env['dashboard.builder.widget'].search([
                    ('xml_id', '=', item_data['widget_id'])
                ], limit=1)
            self.env['dashboard.builder.item'].create({
                'dashboard_id': dashboard.id,
                'widget_id': widget.id if widget else False,
                'custom_widget_name': item_data.get('widget_name') if not widget else False,
                'pos_x': item_data.get('position', {}).get('x', 0),
                'pos_y': item_data.get('position', {}).get('y', 0),
                'width': item_data.get('position', {}).get('w', 6),
                'height': item_data.get('position', {}).get('h', 4),
                'config': item_data.get('config', {}),
                'filters': item_data.get('filters', []),
                'context': item_data.get('context', {}),
            })
        return dashboard


class DashboardTag(models.Model):
    _name = 'dashboard.builder.tag'
    _description = 'Dashboard Tag'
    _order = 'sequence, name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    color = fields.Integer(
        string='Color Index',
        default=0,
    )
    dashboard_count = fields.Integer(
        string='Dashboard Count',
        compute='_compute_dashboard_count',
    )

    def _compute_dashboard_count(self):
        for tag in self:
            tag.dashboard_count = self.env['dashboard.builder'].search_count([
                ('tag_ids', 'in', tag.ids)
            ])


class DashboardWidget(models.Model):
    _name = 'dashboard.builder.widget'
    _description = 'Dashboard Widget'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Widget Name',
        required=True,
        translate=True,
    )
    xml_id = fields.Char(
        string='XML ID',
        required=True,
        help='Unique XML identifier for the widget component.',
    )
    description = fields.Html(
        string='Description',
        translate=True,
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    category = fields.Selection([
        ('kpi', 'KPI / Metrics'),
        ('chart', 'Charts'),
        ('table', 'Tables / Lists'),
        ('pivot', 'Pivot Tables'),
        ('gauge', 'Gauges / Progress'),
        ('custom', 'Custom / HTML'),
        ('action', 'Action Buttons'),
        ('calendar', 'Calendar / Timeline'),
        ('map', 'Maps'),
        ('other', 'Other'),
    ], string='Category', required=True, default='other')
    icon = fields.Char(
        string='Icon',
        default='fa fa-square-o',
        help='FontAwesome icon class.',
    )
    color = fields.Char(
        string='Color',
        default='#3498db',
        help='Widget color for UI.',
    )
    component_name = fields.Char(
        string='Component Name',
        required=True,
        help='Owl component name (e.g., DashboardKpiCard).',
    )
    default_width = fields.Integer(
        string='Default Width',
        default=6,
        help='Default width in grid columns (1-12).',
    )
    default_height = fields.Integer(
        string='Default Height',
        default=4,
        help='Default height in grid rows.',
    )
    min_width = fields.Integer(
        string='Min Width',
        default=3,
    )
    min_height = fields.Integer(
        string='Min Height',
        default=2,
    )
    max_width = fields.Integer(
        string='Max Width',
        default=12,
    )
    max_height = fields.Integer(
        string='Max Height',
        default=20,
    )
    config_schema = fields.Json(
        string='Configuration Schema',
        default=lambda self: {},
        help='JSON schema for widget configuration form.',
    )
    default_config = fields.Json(
        string='Default Configuration',
        default=lambda self: {},
    )
    supports_filters = fields.Boolean(
        string='Supports Filters',
        default=True,
    )
    supports_drill_down = fields.Boolean(
        string='Supports Drill Down',
        default=False,
    )
    supports_real_time = fields.Boolean(
        string='Supports Real-time Updates',
        default=False,
    )
    js_module = fields.Char(
        string='JavaScript Module',
        help='Path to the widget JS module (relative to static/src/js/widgets/).',
    )
    css_module = fields.Char(
        string='CSS Module',
        help='Path to the widget CSS module.',
    )
    is_active = fields.Boolean(
        string='Active',
        default=True,
    )
    is_system = fields.Boolean(
        string='System Widget',
        default=False,
        help='System widgets cannot be deleted.',
    )
    preview_image = fields.Binary(
        string='Preview Image',
        attachment=True,
    )
    help_text = fields.Html(
        string='Help Text',
        translate=True,
    )

    _xml_id_uniq = models.Constraint(
        'UNIQUE(xml_id)',
        'XML ID must be unique!',
    )

    @api.model
    def get_widget_categories(self):
        """Return widget categories for UI grouping."""
        return dict(self._fields['category'].selection)

    def action_test_widget(self):
        """Open widget in test mode."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/dashboard/builder/widget/test/{self.id}',
            'target': 'new',
        }


class DashboardItem(models.Model):
    _name = 'dashboard.builder.item'
    _description = 'Dashboard Item'
    _order = 'pos_y, pos_x, sequence'

    dashboard_id = fields.Many2one(
        'dashboard.builder',
        string='Dashboard',
        required=True,
        ondelete='cascade',
    )
    widget_id = fields.Many2one(
        'dashboard.builder.widget',
        string='Widget',
        ondelete='restrict',
    )
    custom_widget_name = fields.Char(
        string='Custom Widget Name',
        help='Name for custom widgets without a widget definition.',
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10,
    )
    pos_x = fields.Integer(
        string='X Position',
        default=0,
        help='Horizontal position in grid (0-11).',
    )
    pos_y = fields.Integer(
        string='Y Position',
        default=0,
        help='Vertical position in grid.',
    )
    width = fields.Integer(
        string='Width',
        default=6,
        help='Width in grid columns (1-12).',
    )
    height = fields.Integer(
        string='Height',
        default=4,
        help='Height in grid rows.',
    )
    min_width = fields.Integer(
        string='Min Width',
        default=1,
    )
    min_height = fields.Integer(
        string='Min Height',
        default=1,
    )
    is_locked = fields.Boolean(
        string='Locked',
        default=False,
        help='Prevent moving/resizing this item.',
    )
    is_visible = fields.Boolean(
        string='Visible',
        default=True,
    )
    config = fields.Json(
        string='Widget Configuration',
        default=lambda self: {},
        help='Widget-specific configuration stored as JSON.',
    )
    filters = fields.Json(
        string='Filters',
        default=lambda self: [],
        help='Additional domain filters for this widget.',
    )
    context = fields.Json(
        string='Context',
        default=lambda self: {},
        help='Additional context for this widget.',
    )
    drill_down_action = fields.Char(
        string='Drill Down Action',
        help='Action to trigger on drill down (XML ID or URL).',
    )
    refresh_interval = fields.Integer(
        string='Refresh Interval (seconds)',
        default=0,
        help='Override dashboard refresh interval. 0 = use dashboard setting.',
    )
    last_refreshed = fields.Datetime(
        string='Last Refreshed',
        readonly=True,
    )
    error_message = fields.Text(
        string='Error Message',
        readonly=True,
    )
    loading = fields.Boolean(
        string='Loading',
        default=False,
    )

    @api.constrains('pos_x', 'width')
    def _check_position_bounds(self):
        for item in self:
            if item.pos_x < 0:
                raise ValidationError(_('X position cannot be negative.'))
            if item.pos_x + item.width > 12:
                raise ValidationError(_('Item exceeds grid width (max 12 columns).'))
            if item.width < 1 or item.width > 12:
                raise ValidationError(_('Width must be between 1 and 12.'))
            if item.height < 1:
                raise ValidationError(_('Height must be at least 1.'))

    @api.onchange('widget_id')
    def _onchange_widget_id(self):
        if self.widget_id:
            self.width = self.widget_id.default_width
            self.height = self.widget_id.default_height
            self.min_width = self.widget_id.min_width
            self.min_height = self.widget_id.min_height
            self.config = self.widget_id.default_config.copy()

    def write(self, vals):
        if 'pos_x' in vals or 'pos_y' in vals or 'width' in vals or 'height' in vals:
            # Check for overlapping items
            for item in self:
                new_x = vals.get('pos_x', item.pos_x)
                new_y = vals.get('pos_y', item.pos_y)
                new_w = vals.get('width', item.width)
                new_h = vals.get('height', item.height)
                overlapping = self.search([
                    ('id', '!=', item.id),
                    ('dashboard_id', '=', item.dashboard_id.id),
                    ('is_visible', '=', True),
                    '|',
                        '&', ('pos_x', '<', new_x + new_w), ('pos_x', '>=', new_x),
                        '&', ('pos_x', '<', new_x), ('pos_x', '>=', new_x - new_w),
                ])
                # Simplified overlap check
                for other in overlapping:
                    if not (new_x + new_w <= other.pos_x or
                            other.pos_x + other.width <= new_x or
                            new_y + new_h <= other.pos_y or
                            other.pos_y + other.height <= new_y):
                        # Items overlap - in a real implementation, you might want to
                        # auto-arrange or raise a warning
                        pass
        return super().write(vals)

    def action_configure(self):
        """Open widget configuration dialog."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Configure Widget'),
            'res_model': 'dashboard.builder.item.config.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_item_id': self.id},
        }

    def action_remove(self):
        """Remove item from dashboard."""
        self.ensure_one()
        self.unlink()
        return True

    def action_duplicate(self):
        """Duplicate this item."""
        self.ensure_one()
        new_item = self.copy({
            'pos_x': min(self.pos_x + 1, 12 - self.width),
            'pos_y': self.pos_y + 1,
        })
        return new_item


class DashboardShare(models.Model):
    _name = 'dashboard.builder.share'
    _description = 'Dashboard Share'
    _order = 'create_date desc'

    dashboard_id = fields.Many2one(
        'dashboard.builder',
        string='Dashboard',
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(
        string='Share Name',
        required=True,
    )
    share_type = fields.Selection([
        ('link', 'Public Link'),
        ('embed', 'Embed Code'),
        ('user', 'Specific Users'),
        ('group', 'User Groups'),
    ], string='Share Type', required=True, default='link')
    access_token = fields.Char(
        string='Access Token',
        readonly=True,
        copy=False,
    )
    password = fields.Char(
        string='Password',
        help='Optional password for protected access.',
    )
    user_ids = fields.Many2many(
        'res.users',
        'dashboard_builder_share_user_rel',
        'share_id', 'user_id',
        string='Users',
    )
    group_ids = fields.Many2many(
        'res.groups',
        'dashboard_builder_share_group_rel',
        'share_id', 'group_id',
        string='Groups',
    )
    expiry_date = fields.Date(
        string='Expiry Date',
    )
    is_active = fields.Boolean(
        string='Active',
        default=True,
    )
    allow_export = fields.Boolean(
        string='Allow Export',
        default=False,
    )
    view_count = fields.Integer(
        string='View Count',
        default=0,
        readonly=True,
    )
    last_accessed = fields.Datetime(
        string='Last Accessed',
        readonly=True,
    )
    embed_width = fields.Integer(
        string='Embed Width',
        default=1200,
    )
    embed_height = fields.Integer(
        string='Embed Height',
        default=800,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('access_token'):
                vals['access_token'] = self.env['ir.config_parameter'].sudo().get_str(
                    'dashboard.builder.token_secret', 'dashboard_builder'
                ) + '_' + str(fields.Datetime.now().timestamp()).replace('.', '')
        return super().create(vals_list)

    def action_regenerate_token(self):
        """Regenerate access token."""
        self.ensure_one()
        self.write({
            'access_token': self.env['ir.config_parameter'].sudo().get_str(
                'dashboard.builder.token_secret', 'dashboard_builder'
            ) + '_' + str(fields.Datetime.now().timestamp()).replace('.', '')
        })
        return True

    def get_share_url(self):
        """Get the public share URL."""
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_str('web.base.url')
        return f'{base_url}/dashboard/builder/shared/{self.access_token}'

    def get_embed_code(self):
        """Get iframe embed code."""
        self.ensure_one()
        url = self.get_share_url()
        return f'<iframe src="{url}" width="{self.embed_width}" height="{self.embed_height}" frameborder="0" allowfullscreen></iframe>'