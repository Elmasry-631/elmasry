{
    "name": "All in one add custom fields -Global Custom Fields",
    "version": "18.0.0.5",
    "category": "Extra Tools",
    'summary': "Add custom fields global custom field add dynamic fields custom dynamic fields all in one add new fields all in one custom add fields update view update custom fields update fields assign custom fields update global custom fields easy to add custom field",
    "description": """
	
				add custom fields,
				global field,
				global tabs,
				gubal custome fields and tabs,
	
	""",
    "author": "BROWSEINFO",
    "website": "https://www.browseinfo.com/demo-request?app=bi_global_custom_fields&version=18&edition=Community",
    "price": 89,
    'license': 'OPL-1',
    "currency": "EUR",
    "depends": ['base'],
    "data": [
        'security/global_custom_fields_security.xml',
        'security/ir.model.access.csv',
        'views/global_custom_fields.xml',
        'views/custom_fields_view.xml',
        'views/global_custom_tabs_view.xml',
        'views/global_custom_fields_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'bi_global_custom_fields/static/src/js/dyanmic_form_controller.js',
        ],
    },
    "qweb": [],
    "auto_install": False,
    "installable": True,
    "live_test_url": 'https://www.browseinfo.com/demo-request?app=bi_global_custom_fields&version=18&edition=Community',
    "images": ["static/description/Banner.gif"],
}
