{
    "name": "MRP Lock Lines",
    "version": "19.0.1.0.0",
    "category": "Manufacturing/Manufacturing",
    "summary": "Lock all component lines in Manufacturing Order except the last one",
    "description": """
        This module locks all component lines (Components to Consume) in a
        Manufacturing Order, keeping only the last line editable. This prevents
        accidental modifications to raw material quantities, lots, and locations
        while still allowing adjustments on the final line.
    """,
    "author": "Masry",
    "website": "",
    "license": "LGPL-3",
    "depends": [
        "mrp",
        "stock",
    ],
    "data": [
        "views/mrp_production_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}