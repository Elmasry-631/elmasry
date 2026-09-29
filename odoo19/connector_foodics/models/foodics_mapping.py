from odoo import api, fields, models


class FoodicsMapping(models.Model):
    _name = "foodics.mapping"
    _description = "Foodics Field Mapping"
    _order = "connection_id, foodics_resource, sequence, id"

    sequence = fields.Integer(default=10)
    connection_id = fields.Many2one("foodics.connection", ondelete="cascade")
    name = fields.Char(compute="_compute_name", store=True)
    odoo_model = fields.Char(required=True)
    foodics_resource = fields.Char(required=True)
    odoo_field = fields.Char(required=True)
    foodics_field = fields.Char(required=True)
    mapping_type = fields.Selection(
        [
            ("direct", "Direct"),
            ("lookup", "Lookup"),
            ("default", "Default"),
            ("transform", "Transform"),
        ],
        default="direct",
        required=True,
    )
    default_value = fields.Char()
    transform_function = fields.Char()
    active = fields.Boolean(default=True)

    _field_mapping_unique = models.Constraint(
        "unique(connection_id, odoo_model, foodics_resource, odoo_field, foodics_field)",
        "This mapping already exists for the selected connection.",
    )

    @api.depends("odoo_field", "foodics_field")
    def _compute_name(self):
        for mapping in self:
            mapping.name = f"{mapping.odoo_field or ''} -> {mapping.foodics_field or ''}"


class FoodicsBranchMapping(models.Model):
    _name = "foodics.branch.mapping"
    _description = "Foodics Branch Mapping"
    _order = "connection_id, name"

    connection_id = fields.Many2one("foodics.connection", required=True, ondelete="cascade")
    name = fields.Char(required=True)
    foodics_branch_id = fields.Char(required=True)
    warehouse_id = fields.Many2one("stock.warehouse")
    location_id = fields.Many2one("stock.location")
    pos_config_id = fields.Many2one("pos.config")
    company_id = fields.Many2one(related="connection_id.company_id", store=True)
    active = fields.Boolean(default=True)
    notes = fields.Text()

    _branch_unique = models.Constraint(
        "unique(connection_id, foodics_branch_id)",
        "Foodics branch is already mapped.",
    )
