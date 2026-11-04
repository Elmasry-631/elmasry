{
    'name': 'Hospital Management System',
    'version': '19.0.1.0.0',
    'category': 'Services/Hospital',
    'summary': 'Complete hospital management: patients, appointments, EMR, wards, lab, pharmacy, billing',
    'description': """
Hospital Management System
==========================

Complete hospital management system covering:
- Patient registration and management
- Appointment scheduling with calendar view
- Electronic Medical Records (EMR)
- Prescriptions with PDF printing
- Department, ward, and bed management with occupancy tracking
- Patient admission/discharge workflow
- Laboratory tests and radiology orders
- Pharmacy: medicaments with stock integration
- Medical billing integrated with Accounting
- Dashboard with KPIs and Chart.js visualizations
- 7 role-based security groups
- PDF reports (prescription, medical record, invoice)
- Email notifications via mail templates

Author: Ibrahim Elmasry
    """,
    'author': 'Ibrahim Elmasry',
    'website': 'https://github.com/Elmasry-631',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'hr',
        'stock',
        'account',
        'sale_management',
        'web',
    ],
    'data': [
        # O19-03: correct load order = security → data → reports → views → menus

        # Security first (groups before views — LAW 3)
        'security/el_hospital_groups.xml',
        'security/ir.model.access.csv',

        # Data: sequences + mail templates + module category
        'data/hospital_sequences.xml',
        'data/hospital_mail_templates.xml',
        'data/hospital_data.xml',

        # Reports (before views — views may reference report actions)
        'reports/hospital_prescription_report.xml',
        'reports/hospital_medical_record_report.xml',
        'reports/hospital_billing_report.xml',

        # Views in dependency order
        'views/hospital_department_views.xml',
        'views/hospital_physician_views.xml',
        'views/hospital_patient_views.xml',
        'views/hospital_appointment_views.xml',
        'views/hospital_medical_record_views.xml',
        'views/hospital_prescription_views.xml',
        'views/hospital_ward_views.xml',
        'views/hospital_bed_views.xml',
        'views/hospital_admission_views.xml',
        'views/hospital_lab_test_views.xml',
        'views/hospital_radiology_views.xml',
        'views/hospital_medicament_views.xml',
        'views/hospital_billing_views.xml',
        'views/hospital_dashboard_views.xml',

        # Menus last (reference everything above)
        'views/hospital_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'el_hospital/static/src/js/hospital_dashboard.js',
            'el_hospital/static/src/xml/hospital_dashboard_templates.xml',
            'el_hospital/static/src/css/hospital_dashboard.css',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'external_dependencies': {
        'python': ['lxml'],
        'bin': [],
    },
}
