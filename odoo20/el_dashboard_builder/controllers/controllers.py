# -*- coding: utf-8 -*-
import ast
import base64
import datetime
import decimal
import json
import logging

from odoo import _, fields, http
from odoo.exceptions import AccessError
from odoo.http import request

_logger = logging.getLogger(__name__)


class DashboardBuilderController(http.Controller):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _allowed(self, record, operation):
        try:
            return bool(record.has_access(operation))
        except (AccessError, Exception):
            return False

    def _json_safe(self, value):
        if isinstance(value, (datetime.datetime, datetime.date)):
            return value.isoformat()
        if isinstance(value, decimal.Decimal):
            return float(value)
        if isinstance(value, tuple):
            return [self._json_safe(v) for v in value]
        if isinstance(value, list):
            return [self._json_safe(v) for v in value]
        if isinstance(value, dict):
            return {k: self._json_safe(v) for k, v in value.items()}
        return value

    def _domain(self, item):
        config = item.config or {}
        domain = config.get('domain') or []
        filters = item.filters or []
        if isinstance(domain, dict):
            domain = []
        if isinstance(filters, dict):
            filters = []
        return list(domain) + list(filters)

    def _label(self, value):
        if isinstance(value, (list, tuple)):
            if len(value) > 1:
                return value[1] or ''
            return value[0] if value else ''
        if value is False or value is None:
            return ''
        return str(value)

    def _aggregate_spec(self, field_name, aggregation):
        aggregation = aggregation or 'sum'
        if aggregation == 'count':
            if not field_name or field_name in ('id', '__count'):
                return '__count'
            return f'{field_name}:count'
        if not field_name:
            return '__count'
        return f'{field_name}:{aggregation}'

    def _aggregate_value(self, model, domain, field_name, aggregation):
        aggregation = aggregation or 'sum'
        if aggregation == 'count':
            return model.search_count(domain)
        spec = self._aggregate_spec(field_name, aggregation)
        groups = model.formatted_read_group(domain, [], [spec], limit=1)
        if not groups:
            return 0
        return groups[0].get(spec, 0) or 0

    def _item_payload(self, item):
        widget = item.widget_id
        config = item.config or {}
        return {
            'id': item.id,
            'widget_id': widget.id if widget else False,
            'widget_name': widget.name if widget else (item.custom_widget_name or 'Widget'),
            'component_name': widget.component_name if widget else 'DashboardHtml',
            'widget_icon': widget.icon if widget else 'fa fa-square-o',
            'widget_color': widget.color if widget else '#3498db',
            'pos_x': item.pos_x,
            'pos_y': item.pos_y,
            'width': item.width,
            'height': item.height,
            'is_locked': item.is_locked,
            'is_visible': item.is_visible,
            'config': config,
            'filters': item.filters or [],
            'context': item.context or {},
        }

    # ------------------------------------------------------------------
    # Pages
    # ------------------------------------------------------------------
    def _get_dashboard_filters(self, dashboard, items):
        """Get global filters to apply to all widgets."""
        filters = []
        
        # Add filter_domain if set
        if dashboard.filter_domain:
            try:
                domain = ast.literal_eval(dashboard.filter_domain) if isinstance(dashboard.filter_domain, str) else dashboard.filter_domain
                filters.append({
                    'id': 'filter_domain',
                    'field_label': _('Global Domain Filter'),
                    'options': [{'value': str(domain), 'label': str(domain)}],
                })
            except Exception:
                pass
        
        # Add filter_context keys as filter options
        if dashboard.filter_context:
            for key, value in dashboard.filter_context.items():
                if isinstance(value, str) and value:
                    filters.append({
                        'id': key,
                        'field_label': key,
                        'options': [{'value': value, 'label': value}],
                    })
        
        return filters

    @http.route('/dashboard/builder/<int:dashboard_id>', type='http', auth='user', website=False)
    def dashboard_view(self, dashboard_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return request.not_found()

        if not self._allowed(dashboard, 'read'):
            return request.render('web.http_error', {'status_code': '403', 'status_message': 'Access Denied'})

        dashboard.sudo().write({
            'last_viewed': fields.Datetime.now(),
            'view_count': dashboard.view_count + 1,
        })

        items = dashboard.item_ids.filtered('is_visible').sorted(key=lambda i: (i.pos_y, i.pos_x))
        editable = (
            request.env.user.has_group('el_dashboard_builder.group_dashboard_manager')
            or dashboard.user_id == request.env.user
        )

        values = {
            'dashboard': dashboard,
            'items': [self._item_payload(item) for item in items],
            'filters': self._get_dashboard_filters(dashboard, items),
            'editable': editable,
            'layout_config': dashboard.layout_config,
        }
        return request.render('el_dashboard_builder.DashboardBuilderView', values)

    @http.route('/dashboard/builder/<int:dashboard_id>/edit', type='http', auth='user', website=False)
    def dashboard_edit(self, dashboard_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return request.not_found()

        if not self._allowed(dashboard, 'write'):
            return request.render('web.http_error', {'status_code': '403', 'status_message': 'Access Denied'})

        items = dashboard.item_ids.sorted(key=lambda i: (i.pos_y, i.pos_x))
        widgets = request.env['dashboard.builder.widget'].search([('is_active', '=', True)])
        widget_categories = [
            {'key': 'kpi', 'label': 'KPI / Metrics'},
            {'key': 'chart', 'label': 'Charts'},
            {'key': 'table', 'label': 'Tables / Lists'},
            {'key': 'pivot', 'label': 'Pivot Tables'},
            {'key': 'gauge', 'label': 'Gauges / Progress'},
            {'key': 'custom', 'label': 'Custom / HTML'},
            {'key': 'action', 'label': 'Action Buttons'},
            {'key': 'calendar', 'label': 'Calendar / Timeline'},
            {'key': 'other', 'label': 'Other'},
        ]
        widgets_by_category = {
            cat['key']: widgets.filtered(lambda w, key=cat['key']: w.category == key)
            for cat in widget_categories
        }

        values = {
            'dashboard': dashboard,
            'items': [self._item_payload(item) for item in items],
            'widget_categories': widget_categories,
            'widgets_by_category': widgets_by_category,
            'layout_config': dashboard.layout_config,
        }
        return request.render('el_dashboard_builder.DashboardBuilderEditor', values)

    @http.route('/dashboard/builder/shared/<string:token>', type='http', auth='public', website=False)
    def dashboard_shared(self, token, **kwargs):
        share = request.env['dashboard.builder.share'].sudo().search([
            ('access_token', '=', token),
            ('is_active', '=', True),
        ], limit=1)

        if not share:
            return request.not_found()

        if share.expiry_date and share.expiry_date < fields.Date.today():
            return request.render('el_dashboard_builder.DashboardSharedExpired', {'share': share})

        session_key = 'dashboard_share_%s' % token
        if share.password and not request.session.get(session_key) and kwargs.get('password') != share.password:
            return request.render('el_dashboard_builder.DashboardSharedPassword', {'share': share})
        if share.password and kwargs.get('password') == share.password:
            request.session[session_key] = True

        dashboard = share.dashboard_id
        if not dashboard.exists() or not dashboard.active:
            return request.not_found()

        share.sudo().write({
            'view_count': share.view_count + 1,
            'last_accessed': fields.Datetime.now(),
        })

        items = dashboard.item_ids.filtered('is_visible').sorted(key=lambda i: (i.pos_y, i.pos_x))
        values = {
            'dashboard': dashboard,
            'items': [self._item_payload(item) for item in items],
            'share': share,
            'embed_url': share.get_embed_code(),
            'layout_config': dashboard.layout_config,
        }
        return request.render('el_dashboard_builder.DashboardSharedView', values)

    @http.route('/dashboard/builder/widget/test/<int:widget_id>', type='http', auth='user', website=False)
    def widget_test(self, widget_id, **kwargs):
        widget = request.env['dashboard.builder.widget'].browse(widget_id)
        if not widget.exists():
            return request.not_found()

        if not self._allowed(widget, 'read'):
            return request.render('web.http_error', {'status_code': '403', 'status_message': 'Access Denied'})

        return request.render('el_dashboard_builder.WidgetTestView', {'widget': widget})

    # ------------------------------------------------------------------
    # Exports
    # ------------------------------------------------------------------
    @http.route('/dashboard/builder/export/<int:dashboard_id>', type='http', auth='user', website=False)
    def dashboard_export_json(self, dashboard_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return request.not_found()
        if not self._allowed(dashboard, 'read'):
            return request.render('web.http_error', {'status_code': '403', 'status_message': 'Access Denied'})

        config = {
            'name': dashboard.name,
            'description': dashboard.description,
            'layout_config': dashboard.layout_config,
            'background_color': dashboard.background_color,
            'custom_css': dashboard.custom_css,
            'refresh_interval': dashboard.refresh_interval,
            'filter_domain': dashboard.filter_domain,
            'filter_context': dashboard.filter_context,
            'items': [],
        }
        for item in dashboard.item_ids:
            config['items'].append({
                'widget_id': item.widget_id.xml_id if item.widget_id else None,
                'widget_name': item.widget_id.name if item.widget_id else item.custom_widget_name,
                'position': {'x': item.pos_x, 'y': item.pos_y, 'w': item.width, 'h': item.height},
                'config': item.config,
                'filters': item.filters,
                'context': item.context,
            })

        filename = 'dashboard_%s.json' % dashboard.name.replace(' ', '_')
        return request.make_response(
            json.dumps(config, indent=2, default=str),
            headers=[
                ('Content-Type', 'application/json'),
                ('Content-Disposition', 'attachment; filename="%s"' % filename),
            ],
        )

    @http.route('/dashboard/builder/export/pdf/<int:dashboard_id>', type='http', auth='user', website=False)
    def dashboard_export_pdf(self, dashboard_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return request.not_found()
        if not self._allowed(dashboard, 'read'):
            return request.render('web.http_error', {'status_code': '403', 'status_message': 'Access Denied'})
        try:
            pdf_content = request.env['report.el_dashboard_builder.dashboard_report'].generate_dashboard_pdf(
                dashboard.id
            )
        except Exception as error:  # noqa: BLE001 - surfaced to the user
            return request.make_response(
                'PDF export failed: %s' % error,
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=500,
            )
        filename = 'dashboard_%s.pdf' % dashboard.name.replace(' ', '_')
        return request.make_response(
            pdf_content,
            headers=[
                ('Content-Type', 'application/pdf'),
                ('Content-Disposition', 'attachment; filename="%s"' % filename),
            ],
        )

    @http.route('/dashboard/builder/export/excel/<int:dashboard_id>', type='http', auth='user', website=False)
    def dashboard_export_excel(self, dashboard_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return request.not_found()
        if not self._allowed(dashboard, 'read'):
            return request.render('web.http_error', {'status_code': '403', 'status_message': 'Access Denied'})
        try:
            content = request.env['report.el_dashboard_builder.dashboard_report'].generate_dashboard_excel(dashboard.id)
        except Exception as error:  # noqa: BLE001 - surfaced to the user
            return request.make_response(
                'Excel export failed: %s' % error,
                headers=[('Content-Type', 'text/plain; charset=utf-8')],
                status=500,
            )
        if not content:
            return request.not_found()
        filename = 'dashboard_%s.xlsx' % dashboard.name.replace(' ', '_')
        return request.make_response(
            content,
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="%s"' % filename),
            ],
        )

    # ------------------------------------------------------------------
    # JSON API
    # ------------------------------------------------------------------
    @http.route('/dashboard/builder/api/items/<int:item_id>/data', type='json', auth='public')
    def get_item_data(self, item_id, token=None, **kwargs):
        item = request.env['dashboard.builder.item'].browse(item_id)
        if not item.exists():
            return {'error': 'Item not found'}

        if token:
            share = request.env['dashboard.builder.share'].sudo().search([
                ('access_token', '=', token),
                ('is_active', '=', True),
            ], limit=1)
            if not share:
                return {'error': 'Access denied'}
            if share.expiry_date and share.expiry_date < fields.Date.today():
                return {'error': 'Share link expired'}
            if share.password and not request.session.get('dashboard_share_%s' % token) and kwargs.get('password') != share.password:
                return {'error': 'Access denied'}
            item = item.sudo()
            if item.dashboard_id != share.dashboard_id:
                return {'error': 'Access denied'}
        else:
            if not self._allowed(item, 'read'):
                return {'error': 'Access denied'}

        if not item.widget_id:
            return {'error': 'No widget configured'}

        try:
            data = self._fetch_widget_data(item)
            item.sudo().write({'last_refreshed': fields.Datetime.now(), 'error_message': False})
            return {
                'data': self._json_safe(data),
                'last_refreshed': fields.Datetime.now().isoformat(),
            }
        except Exception:
            _logger.exception(
                "Dashboard widget data retrieval failed (item_id=%s)", item.id
            )
            message = _('Unable to load dashboard data. Check the server logs.')
            item.sudo().write({'error_message': message})
            return {'error': message}

    @http.route('/dashboard/builder/api/widgets/<int:widget_id>/data', type='json', auth='user')
    def get_widget_preview_data(self, widget_id, **kwargs):
        widget = request.env['dashboard.builder.widget'].browse(widget_id)
        if not widget.exists() or not self._allowed(widget, 'read'):
            return {'error': 'Widget not found'}

        class _PreviewItem:
            def __init__(self, widget):
                self.id = False
                self.widget_id = widget
                self.custom_widget_name = widget.name
                self.config = dict(widget.default_config or {})
                self.filters = []
                self.context = {}
                self.env = widget.env

        try:
            data = self._fetch_widget_data(_PreviewItem(widget))
            return {'data': self._json_safe(data)}
        except Exception:
            _logger.exception(
                "Dashboard widget preview failed (widget_id=%s)", widget.id
            )
            return {
                'error': _('Unable to preview this widget. Check the server logs.')
            }

    @http.route('/dashboard/builder/api/items/<int:item_id>/configure', type='json', auth='user')
    def configure_item(self, item_id, config, **kwargs):
        item = request.env['dashboard.builder.item'].browse(item_id)
        if not item.exists():
            return {'error': 'Item not found'}
        if not self._allowed(item, 'write'):
            return {'error': 'Access denied'}
        item.write({'config': config})
        return {'success': True}

    @http.route('/dashboard/builder/api/items/<int:item_id>/update', type='json', auth='user')
    def update_item(self, item_id, values, **kwargs):
        item = request.env['dashboard.builder.item'].browse(item_id)
        if not item.exists():
            return {'error': 'Item not found'}
        if not self._allowed(item, 'write'):
            return {'error': 'Access denied'}
        allowed = {'config', 'is_locked', 'is_visible', 'pos_x', 'pos_y', 'width', 'height', 'filters', 'context'}
        vals = {k: v for k, v in (values or {}).items() if k in allowed}
        if vals:
            item.write(vals)
        return {'success': True}

    @http.route('/dashboard/builder/api/items/<int:item_id>/duplicate', type='json', auth='user')
    def duplicate_item(self, item_id, **kwargs):
        item = request.env['dashboard.builder.item'].browse(item_id)
        if not item.exists():
            return {'error': 'Item not found'}
        if not self._allowed(item, 'write'):
            return {'error': 'Access denied'}
        new_item = item.copy({
            'pos_x': min(item.pos_x + 1, 12 - item.width),
            'pos_y': item.pos_y + 1,
        })
        return {'success': True, 'id': new_item.id}

    @http.route('/dashboard/builder/api/items/<int:item_id>/delete', type='json', auth='user')
    def delete_item(self, item_id, **kwargs):
        item = request.env['dashboard.builder.item'].browse(item_id)
        if not item.exists():
            return {'error': 'Item not found'}
        if not self._allowed(item, 'unlink'):
            return {'error': 'Access denied'}
        item.unlink()
        return {'success': True}

    @http.route('/dashboard/builder/api/items/create', type='json', auth='user')
    def create_item(self, dashboard_id, widget_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(int(dashboard_id))
        widget = request.env['dashboard.builder.widget'].browse(int(widget_id))
        if not dashboard.exists() or not widget.exists():
            return {'error': 'Dashboard or widget not found'}
        if not self._allowed(dashboard, 'write'):
            return {'error': 'Access denied'}
        width = int(kwargs.get('w') or widget.default_width or 6)
        height = int(kwargs.get('h') or widget.default_height or 4)
        item = request.env['dashboard.builder.item'].create({
            'dashboard_id': dashboard.id,
            'widget_id': widget.id,
            'pos_x': int(kwargs.get('x') or 0),
            'pos_y': int(kwargs.get('y') or 0),
            'width': max(1, min(12, width)),
            'height': max(1, height),
            'config': dict(widget.default_config or {}),
        })
        return {'success': True, 'id': item.id, 'redirect': '/dashboard/builder/%s/edit' % dashboard.id}

    @http.route('/dashboard/builder/api/items/reorder', type='json', auth='user')
    def reorder_items(self, items, **kwargs):
        for item_data in items or []:
            item = request.env['dashboard.builder.item'].browse(int(item_data.get('id')))
            if item.exists() and self._allowed(item, 'write'):
                try:
                    values = {}
                    for key, field, current in (
                        ('x', 'pos_x', item.pos_x),
                        ('y', 'pos_y', item.pos_y),
                        ('w', 'width', item.width),
                        ('h', 'height', item.height),
                    ):
                        value = item_data.get(key)
                        values[field] = int(value) if value is not None else current
                    item.write(values)
                except AccessError:
                    continue
        return {'success': True}

    @http.route('/dashboard/builder/api/dashboard/<int:dashboard_id>/layout', type='json', auth='user')
    def save_layout(self, dashboard_id, layout_config, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return {'error': 'Dashboard not found'}
        if not self._allowed(dashboard, 'write'):
            return {'error': 'Access denied'}
        dashboard.write({'layout_config': layout_config})
        return {'success': True}

    @http.route('/dashboard/builder/api/dashboard/<int:dashboard_id>/duplicate', type='json', auth='user')
    def duplicate_dashboard(self, dashboard_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return {'error': 'Dashboard not found'}
        if not self._allowed(dashboard, 'read'):
            return {'error': 'Access denied'}
        new_dashboard = dashboard.copy({'name': '%s (copy)' % dashboard.name})
        return {'success': True, 'id': new_dashboard.id, 'redirect': '/dashboard/builder/%s' % new_dashboard.id}

    @http.route('/dashboard/builder/api/dashboard/<int:dashboard_id>/delete', type='json', auth='user')
    def delete_dashboard(self, dashboard_id, **kwargs):
        dashboard = request.env['dashboard.builder'].browse(dashboard_id)
        if not dashboard.exists():
            return {'error': 'Dashboard not found'}
        if not self._allowed(dashboard, 'unlink'):
            return {'error': 'Access denied'}
        dashboard.unlink()
        return {'success': True, 'redirect': '/web#action=el_dashboard_builder.action_dashboard_builder_list'}

    # ------------------------------------------------------------------
    # Data providers
    # ------------------------------------------------------------------
    def _fetch_widget_data(self, item):
        component = item.widget_id.component_name if item.widget_id else 'DashboardHtml'
        handler = getattr(self, '_data_%s' % component, None)
        if not handler:
            return {'component': component, 'message': 'No renderer for %s' % component}
        return handler(item)

    def _data_DashboardKpiCard(self, item):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        field_name = config.get('field')
        aggregation = config.get('aggregation') or 'sum'
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        value = self._aggregate_value(model, domain, field_name, aggregation)
        precision = int(config.get('precision') or 0)
        try:
            value = float(value)
            formatted = '{:,.{precision}f}'.format(value, precision=precision)
        except (TypeError, ValueError):
            formatted = str(value)
        prefix = config.get('prefix') or ''
        suffix = config.get('suffix') or ''
        target = config.get('target_value')
        target_progress = None
        if target:
            try:
                target_progress = (float(value) / float(target)) * 100
            except (TypeError, ValueError, ZeroDivisionError):
                target_progress = None
        return {
            'component': 'DashboardKpiCard',
            'value': value,
            'formatted_value': '%s%s%s' % (prefix, formatted, suffix),
            'label': config.get('label') or (item.widget_id.name if item.widget_id else ''),
            'prefix': prefix,
            'suffix': suffix,
            'target_value': target,
            'target_label': config.get('target_label') or 'Target',
            'target_progress': target_progress,
            'color': (config.get('color') or (item.widget_id.color if item.widget_id else '#3498db')),
        }

    def _group_rows(self, model, domain, groupby, spec, limit=None):
        groups = model.formatted_read_group(domain, groupby, [spec], limit=limit)
        return groups

    def _chart_payload(self, item, chart_type):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        aggregation = config.get('aggregation') or 'sum'
        y_field = config.get('y_field') or config.get('value_field')
        spec = self._aggregate_spec(y_field, aggregation)
        palette = [
            '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
            '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
        ]

        if chart_type == 'line':
            x_field = config.get('x_field') or 'create_date'
            granularity = config.get('time_granularity') or 'month'
            x_spec = '%s:%s' % (x_field, granularity)
            group_by = config.get('group_by')
            groupby = [x_spec] + ([group_by] if group_by else [])
            limit = int(config.get('limit') or 100)
        else:
            x_field = config.get('x_field') or config.get('label_field') or 'create_date'
            x_spec = x_field
            groupby = [x_spec]
            limit = int(config.get('limit') or 10)

        groups = model.formatted_read_group(domain, groupby, [spec], limit=limit)

        if chart_type == 'line' and config.get('group_by'):
            labels = []
            series = {}
            for group in groups:
                label = self._label(group.get(x_spec))
                if label not in labels:
                    labels.append(label)
                series_name = self._label(group.get(config['group_by'])) or 'Other'
                series.setdefault(series_name, {})
                series[series_name][label] = group.get(spec) or 0
            datasets = []
            for index, (series_name, values) in enumerate(series.items()):
                color = palette[index % len(palette)]
                datasets.append({
                    'label': series_name,
                    'data': [values.get(label, 0) for label in labels],
                    'borderColor': color,
                    'backgroundColor': color,
                    'fill': bool(config.get('fill_area')),
                    'tension': 0.3,
                })
        else:
            labels = [self._label(group.get(x_spec)) for group in groups]
            values = [group.get(spec) or 0 for group in groups]
            if chart_type in ('bar',) and config.get('order') == 'desc':
                pairs = sorted(zip(labels, values), key=lambda p: p[1], reverse=True)
                labels = [p[0] for p in pairs]
                values = [p[1] for p in pairs]
            color = (item.widget_id.color if item.widget_id else '#3498db')
            datasets = [{
                'label': config.get('y_axis_label') or (item.widget_id.name if item.widget_id else ''),
                'data': values,
                'backgroundColor': color,
                'borderColor': color,
                'fill': bool(config.get('fill_area')),
                'tension': 0.3,
            }]

        return {
            'component': 'DashboardBarChart' if chart_type == 'bar' else 'DashboardLineChart',
            'chart_type': chart_type,
            'labels': labels,
            'datasets': datasets,
            'orientation': config.get('orientation') or 'vertical',
            'show_legend': config.get('show_legend', True),
            'y_axis_label': config.get('y_axis_label') or '',
        }

    def _data_DashboardBarChart(self, item):
        return self._chart_payload(item, 'bar')

    def _data_DashboardLineChart(self, item):
        return self._chart_payload(item, 'line')

    def _data_DashboardPieChart(self, item):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        aggregation = config.get('aggregation') or 'sum'
        label_field = config.get('label_field') or config.get('x_field') or 'create_date'
        value_field = config.get('value_field') or config.get('y_field')
        spec = self._aggregate_spec(value_field, aggregation)
        limit = int(config.get('limit') or 8)
        groups = model.formatted_read_group(domain, [label_field], [spec], limit=limit)

        pairs = [
            (self._label(group.get(label_field)), group.get(spec) or 0)
            for group in groups
        ]
        pairs.sort(key=lambda p: p[1], reverse=True)
        if config.get('group_others') and len(pairs) > limit:
            head = pairs[:limit - 1]
            others = sum(p[1] for p in pairs[limit - 1:])
            pairs = head + [('Others', others)]
        else:
            pairs = pairs[:limit]

        labels = [p[0] for p in pairs]
        values = [p[1] for p in pairs]
        palette = [
            '#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6',
            '#1abc9c', '#e67e22', '#34495e', '#16a085', '#c0392b',
        ]
        total = sum(values) or 1
        return {
            'component': 'DashboardPieChart',
            'chart_type': config.get('chart_type') or 'doughnut',
            'labels': labels,
            'datasets': [{
                'data': values,
                'backgroundColor': [palette[i % len(palette)] for i in range(len(values))],
                'borderColor': '#ffffff',
                'borderWidth': 2,
            }],
            'percentages': [round((v / total) * 100, 1) for v in values],
            'label_format': config.get('label_format') or 'both',
            'show_legend': config.get('show_legend', True),
        }

    def _data_DashboardTable(self, item):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        fields_config = config.get('fields') or []
        if not fields_config:
            fields_config = [
                {'name': 'display_name', 'label': 'Name', 'format': 'text'},
            ]
        field_names = [f.get('name') for f in fields_config if f.get('name')]
        limit = int(config.get('limit') or 10)
        order = config.get('order') or 'id desc'
        try:
            records = model.search_read(domain, field_names, limit=limit, order=order)
        except Exception:
            records = model.search_read(domain, field_names, limit=limit)
        total = model.search_count(domain)
        columns = [
            {
                'name': f.get('name'),
                'label': f.get('label') or f.get('name'),
                'format': f.get('format') or 'text',
            }
            for f in fields_config if f.get('name')
        ]
        rows = []
        for record in records:
            row = {'id': record.get('id')}
            for column in columns:
                row[column['name']] = record.get(column['name'])
            rows.append(row)
        return {
            'component': 'DashboardTable',
            'columns': columns,
            'rows': rows,
            'total': total,
            'limit': limit,
        }

    def _data_DashboardPivotTable(self, item):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        aggregation = config.get('aggregation') or 'sum'
        row_field = config.get('row_field') or 'create_date'
        col_field = config.get('col_field')
        value_field = config.get('value_field') or config.get('y_field')
        spec = self._aggregate_spec(value_field, aggregation)
        groupby = [row_field] + ([col_field] if col_field else [])
        groups = model.formatted_read_group(domain, groupby, [spec])

        row_labels = []
        col_labels = []
        cells = {}
        for group in groups:
            row_label = self._label(group.get(row_field))
            col_label = self._label(group.get(col_field)) if col_field else 'Value'
            if row_label not in row_labels:
                row_labels.append(row_label)
            if col_label not in col_labels:
                col_labels.append(col_label)
            cells[(row_label, col_label)] = group.get(spec) or 0

        rows = []
        for row_label in row_labels:
            row = {'label': row_label, 'values': []}
            for col_label in col_labels:
                row['values'].append(cells.get((row_label, col_label), 0))
            rows.append(row)

        return {
            'component': 'DashboardPivotTable',
            'row_labels': row_labels,
            'col_labels': col_labels,
            'rows': rows,
        }

    def _data_DashboardGauge(self, item):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        aggregation = config.get('aggregation') or 'sum'
        field_name = config.get('field') or config.get('value_field')
        value = self._aggregate_value(model, domain, field_name, aggregation)
        precision = int(config.get('precision') or 0)
        try:
            value = float(value)
            formatted = '{:,.{precision}f}'.format(value, precision=precision)
        except (TypeError, ValueError):
            formatted = str(value)
        return {
            'component': 'DashboardGauge',
            'value': value,
            'formatted_value': '%s%s' % (formatted, config.get('suffix') or ''),
            'min_value': float(config.get('min_value') or 0),
            'max_value': float(config.get('max_value') or 100),
            'label': config.get('label') or (item.widget_id.name if item.widget_id else ''),
            'color': item.widget_id.color if item.widget_id else '#f39c12',
        }

    def _data_DashboardProgressBar(self, item):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        aggregation = config.get('aggregation') or 'sum'
        value_field = config.get('value_field')
        value = self._aggregate_value(model, domain, value_field, aggregation)
        target_field = config.get('target_field')
        if target_field:
            target = self._aggregate_value(model, domain, target_field, aggregation)
        else:
            target = config.get('target_value') or 0
        try:
            percentage = (float(value) / float(target)) * 100 if target else 0
        except (TypeError, ValueError, ZeroDivisionError):
            percentage = 0
        return {
            'component': 'DashboardProgressBar',
            'value': value,
            'target': target,
            'percentage': max(0, min(100, percentage)),
            'label': config.get('label') or (item.widget_id.name if item.widget_id else ''),
            'color': config.get('color') or '#2ecc71',
        }

    def _data_DashboardHtml(self, item):
        config = item.config or {}
        return {
            'component': 'DashboardHtml',
            'content': config.get('content') or '',
            'format': config.get('format') or 'html',
        }

    def _data_DashboardActionButtons(self, item):
        config = item.config or {}
        return {
            'component': 'DashboardActionButtons',
            'buttons': config.get('buttons') or [],
        }

    def _data_DashboardCalendar(self, item):
        config = item.config or {}
        env = item.env
        model_name = config.get('model')
        if not model_name:
            return {'error': 'No model configured'}
        model = env[model_name]
        domain = self._domain(item)
        date_field = config.get('date_field') or 'create_date'
        title_field = config.get('title_field') or 'display_name'
        limit = int(config.get('limit') or 20)
        try:
            records = model.search_read(domain, [date_field, title_field], limit=limit, order='%s asc' % date_field)
        except Exception:
            records = model.search_read(domain, [date_field, title_field], limit=limit)
        events = []
        for record in records:
            events.append({
                'id': record.get('id'),
                'date': record.get(date_field),
                'title': record.get(title_field) or '',
            })
        return {
            'component': 'DashboardCalendar',
            'model': model_name,
            'date_field': date_field,
            'events': events,
        }
