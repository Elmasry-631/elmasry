"""Stock Movement Report — QWeb report handler.

This class is invoked by Odoo's report engine when the QWeb template
needs the actual data. It reads filters from the wizard's ``data`` dict,
calls the abstract model's ``get_report_data()``, and returns the
payload as ``docs`` (a list with one element — the payload dict).
"""

from __future__ import annotations
from types import SimpleNamespace

from odoo import api, fields, models, _


class StockMovementReportHandler(models.AbstractModel):
    """Glue layer between the wizard and the QWeb template."""

    _name = 'report.ie_stock_movement_report.report_stock_movement_document'
    _description = 'Stock Movement Report — QWeb data provider'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Return the payload the QWeb template iterates over."""
        data = data or {}
        if docids:
            wizards = self.env['stock.movement.report.wizard'].browse(docids)
            for wiz in wizards:
                data.setdefault('date_from', wiz.date_from)
                data.setdefault('date_to', wiz.date_to)
                data.setdefault('warehouse_id', wiz.warehouse_id.id if wiz.warehouse_id else False)
                data.setdefault('location_id', wiz.location_id.id if wiz.location_id else False)
                data.setdefault('product_id', wiz.product_id.id if wiz.product_id else False)
                data.setdefault('categ_id', wiz.categ_id.id if wiz.categ_id else False)

        warehouse_id = data.get('warehouse_id')
        location_id = data.get('location_id')

        # Pass scope into context so opening balance classifier can use it
        report_model = self.env['stock.movement.report'].with_context(
            _scope_location_ids=self.env['stock.movement.report']._scope_location_ids(
                warehouse_id, location_id
            ),
        )

        warehouse = self.env['stock.warehouse'].browse(warehouse_id) if warehouse_id else False
        location = self.env['stock.location'].browse(location_id) if location_id else False
        product = self.env['product.product'].browse(data.get('product_id')) if data.get('product_id') else False
        categ = self.env['product.category'].browse(data.get('categ_id')) if data.get('categ_id') else False

        payload = report_model.get_report_data(
            date_from=data['date_from'],
            date_to=data['date_to'],
            warehouse_id=warehouse,
            location_id=location,
            product_id=product,
            categ_id=categ,
        )

        # One doc per product → each becomes a separate HTML body for wkhtmltopdf
        docs = []
        for prod in payload['products']:
            doc_data = {
                'date_from': payload['date_from'],
                'date_to': payload['date_to'],
                'warehouse': payload.get('warehouse'),
                'location': payload.get('location'),
                'product': prod,
            }
            doc = self._dict_to_obj(doc_data)
            doc._name = 'stock.movement.report'
            doc.id = 0
            doc.env = self.env
            docs.append(doc)

        return {
            'docs': docs,
            'doc_model': 'stock.movement.report',
            'company': payload['company'],
            'currency_id': payload['company'].currency_id,
            'now': fields.Datetime.now,  # for print date in header
            '_': _,
        }

    @staticmethod
    def _dict_to_obj(val):
        """Recursively convert dicts/lists to SimpleNamespace for QWeb attr access."""
        if isinstance(val, dict):
            return SimpleNamespace(**{k: StockMovementReportHandler._dict_to_obj(v) for k, v in val.items()})
        if isinstance(val, list):
            return [StockMovementReportHandler._dict_to_obj(v) for v in val]
        return val
