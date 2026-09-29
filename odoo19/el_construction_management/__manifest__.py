{
    'name': 'Construction Management',
    'version': '19.0.1.24.0',
    'summary': 'Construction Management | Job Costing | BOQ | Work Orders | RA Billing | Material Requisition | Subcontracting | Budget',
    'description': """
Construction Management
========================
Complete construction project management for Odoo 19. Manage projects,
sub-projects, BOQ, budgets, rate analysis, phases (WBS), work orders,
material requisitions with approvals, subcontracting, progress billing,
quality checks, tasks, extra expenses, and an advanced real-time dashboard.
Includes RA billing, consume orders, and completion certificates.

Developed by Ibrahim Elmasry — Senior Odoo Developer & Implementation Consultant.
    """,
    'category': 'Construction',
    'author': 'Ibrahim Elmasry',
    'author_id': 'base.module_author_default',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'contacts',
        'hr',
        'stock',
        'stock_account',
        'purchase',
        'account',
        'project',
        'web_gantt',
    ],
    'data': [
        # Security
        'security/construction_security.xml',
        'security/ir.model.access.csv',
        # Data
        'data/sequence_data.xml',
        'data/configuration_data.xml',
        'views/dashboard_views.xml',
        'views/construction_project_views.xml',
        'views/construction_sub_project_views.xml',
        'views/construction_boq_views.xml',
        'views/construction_rate_analysis_views.xml',
        'views/construction_budget_views.xml',
        'views/construction_phase_views.xml',
        'views/construction_work_order_views.xml',
        'views/construction_material_requisition_views.xml',
        'views/construction_material_inventory_views.xml',
        'views/construction_subcontract_views.xml',
        'views/construction_progress_billing_views.xml',
        'views/construction_quality_check_views.xml',
        'views/construction_quality_point_views.xml',
        'views/construction_task_views.xml',
        'views/construction_extra_expense_views.xml',
        'views/construction_configuration_views.xml',
        'reports/construction_reports.xml',
        'views/construction_report_menu_actions.xml',
        'views/construction_report_wizard_views.xml',
        'views/construction_controls_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'el_construction_management/static/src/js/dashboard.js',
            'el_construction_management/static/src/xml/dashboard.xml',
            'el_construction_management/static/src/css/dashboard.css',
            'el_construction_management/static/src/css/form_ux.css',
        ],
    },
    'tests': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
