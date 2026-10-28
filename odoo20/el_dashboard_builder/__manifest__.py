# -*- coding: utf-8 -*-
{
    'name': 'Dashboard Builder',
    'version': '20.0.1.0.0',
    'category': 'Tools',
    'summary': 'Drag-and-drop dashboard builder with customizable widgets',
    'description': """
Dashboard Builder for Odoo 20 Enterprise
=========================================

A powerful, user-friendly dashboard builder that allows users to create
custom dashboards with drag-and-drop widgets.

Features:
- Visual drag-and-drop dashboard designer
- Pre-built widgets: KPI cards, Charts, Tables, Pivot tables, Graphs
- Custom widget support
- Responsive grid layout (12-column)
- Dashboard sharing and permissions
- Real-time preview
- Export to PDF/Excel
- Multi-company support
- RTL support for Arabic

Widgets Included:
- KPI / Metric Cards
- Bar/Line/Pie Charts (Chart.js)
- Pivot Tables
- List/Table Views
- Gauge/Progress Indicators
- Custom HTML/Markdown
- Action Buttons
- Calendar/Schedule View
""",
    'author': 'Elmasry',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'mail',
        'base_setup',
    ],
    'data': [
        'security/dashboard_security.xml',
        'views/dashboard_views.xml',
        'views/dashboard_menu.xml',
        'views/dashboard_templates.xml',
        'wizard/item_config_wizard_views.xml',
        'report/dashboard_report_templates.xml',
        'data/ir_sequence_data.xml',
        'data/dashboard_default_widgets.xml',
    ],
    'demo': [
        'data/dashboard_demo.xml',
    ],
    'assets': {
        'el_dashboard_builder.dashboard_assets': [
            'web/static/src/module_loader.js',
            '/web/static/lib/luxon/luxon.js',
            ('include', 'web.chartjs_lib'),
            'el_dashboard_builder/static/src/scss/dashboard_builder.scss',
            'el_dashboard_builder/static/src/js/dashboard.js',
            'el_dashboard_builder/static/src/js/dashboard_builder.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
    'sequence': 100,
}