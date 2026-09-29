import json

from odoo import api, fields, models


class FoodicsBaseAdapter(models.AbstractModel):
    _name = "foodics.base.adapter"
    _description = "Foodics Base Adapter"

    sync_type = False
    resource = False
    odoo_model = False

    @api.model
    def run(self, connection, direction="pull", records=None):
        connection.ensure_one()
        if records is None and self.odoo_model:
            records = self.env[self.odoo_model].search(self._domain(connection), limit=100)
        if direction == "push":
            return self._push_records(connection, records or self.env[self.odoo_model])
        return self._pull_records(connection)

    def _domain(self, connection):
        return [("foodics_sync_enabled", "=", True)]

    def _pull_records(self, connection):
        payload = self.env["foodics.api.client"].call(connection, "GET", f"/{self.resource}")
        connection._log_operation(self.sync_type, "pull", self.resource, "success", response_data=payload)
        return payload

    def _push_records(self, connection, records):
        count = 0
        for record in records:
            payload = self._to_foodics_payload(connection, record)
            endpoint = f"/{self.resource}/{record.foodics_id}" if getattr(record, "foodics_id", False) else f"/{self.resource}"
            method = "PUT" if getattr(record, "foodics_id", False) else "POST"
            result = self.env["foodics.api.client"].call(connection, method, endpoint, payload=payload)
            foodics_id = result.get("data", {}).get("id") or result.get("id")
            values = {"foodics_last_sync_date": fields.Datetime.now()}
            if foodics_id and "foodics_id" in record._fields:
                values["foodics_id"] = foodics_id
            record.write(values)
            connection._log_operation(
                self.sync_type,
                "push",
                self.resource,
                "success",
                foodics_record_id=foodics_id or getattr(record, "foodics_id", False),
                odoo_model=record._name,
                odoo_record_id=record.id,
                request_payload=json.dumps(payload, indent=2, sort_keys=True),
                response_data=result,
            )
            count += 1
        return count

    def _to_foodics_payload(self, connection, record):
        payload = {}
        mappings = self.env["foodics.mapping"].search([
            ("connection_id", "=", connection.id),
            ("odoo_model", "=", record._name),
            ("foodics_resource", "=", self.resource),
            ("active", "=", True),
        ])
        for mapping in mappings:
            value = mapping.default_value if mapping.mapping_type == "default" else record[mapping.odoo_field]
            if hasattr(value, "id"):
                value = value.display_name
            payload[mapping.foodics_field] = value
        return payload


class FoodicsProductAdapter(models.AbstractModel):
    _name = "foodics.product.adapter"
    _inherit = "foodics.base.adapter"
    _description = "Foodics Product Adapter"

    sync_type = "product"
    resource = "products"
    odoo_model = "product.product"

    def _to_foodics_payload(self, connection, record):
        payload = super()._to_foodics_payload(connection, record)
        if not payload:
            payload = {
                "name": record.display_name,
                "sku": record.default_code,
                "price": record.lst_price,
                "cost": record.standard_price,
                "is_active": record.active,
                "description": record.product_tmpl_id.description_sale,
            }
        return payload


class FoodicsCategoryAdapter(models.AbstractModel):
    _name = "foodics.category.adapter"
    _inherit = "foodics.base.adapter"
    _description = "Foodics Category Adapter"

    sync_type = "category"
    resource = "categories"
    odoo_model = "product.category"


class FoodicsCustomerAdapter(models.AbstractModel):
    _name = "foodics.customer.adapter"
    _inherit = "foodics.base.adapter"
    _description = "Foodics Customer Adapter"

    sync_type = "customer"
    resource = "customers"
    odoo_model = "res.partner"


class FoodicsOrderAdapter(models.AbstractModel):
    _name = "foodics.order.adapter"
    _inherit = "foodics.base.adapter"
    _description = "Foodics Order Adapter"

    sync_type = "order"
    resource = "orders"
    odoo_model = "sale.order"

    def _domain(self, connection):
        return [("company_id", "=", connection.company_id.id)]


class FoodicsInventoryAdapter(models.AbstractModel):
    _name = "foodics.inventory.adapter"
    _inherit = "foodics.base.adapter"
    _description = "Foodics Inventory Adapter"

    sync_type = "inventory"
    resource = "inventory"
    odoo_model = "stock.quant"

    def _domain(self, connection):
        return [("company_id", "=", connection.company_id.id)]


class FoodicsTaxAdapter(models.AbstractModel):
    _name = "foodics.tax.adapter"
    _inherit = "foodics.base.adapter"
    _description = "Foodics Tax Adapter"

    sync_type = "tax"
    resource = "taxes"
    odoo_model = "account.tax"

    def _domain(self, connection):
        return [("company_id", "=", connection.company_id.id), ("foodics_sync_enabled", "=", True)]
