# -*- coding: utf-8 -*-
{
    "name": "Sales Order Contract Terms (AR/EN) - 4 Pages",
    "version": "18.0.1.0.0",
    "category": "Sales",
    "summary": "Separate Sales Order report with bilingual contract terms (4 pages, AR/EN).",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/report_actions.xml",
        "views/report_templates.xml",
        "views/product_template_view.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
