{
    "name": "Journal Entry base import",
    "version": "18.0.1.0.0",
    'author': "Ibrahim Elmasry",
    'website': "https://www.woledge.com",
    "category": "Finance",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "data/completion_rule_data.xml",
        "wizard/import_statement_view.xml",
        "views/account_move_view.xml",
        "views/journal_view.xml",
        "views/partner_view.xml",
    ],
    "external_dependencies": {"python": ["xlrd"]},
    "installable": True,
    "license": "AGPL-3",
}
