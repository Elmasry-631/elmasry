from odoo import models


class TraceabilityMovementReport(models.AbstractModel):
    _name = "report.el_product_traceability_dashboard.movement_pdf"
    _description = "Traceability Movement PDF"

    def _get_report_values(self, docids, data=None):
        docs = self.env["el.product.traceability.report"].browse(docids)
        return {"doc_ids": docids, "doc_model": docs._name, "docs": docs}


class TraceabilityManufacturingReport(models.AbstractModel):
    _name = "report.el_product_traceability_dashboard.manufacturing_pdf"
    _description = "Traceability Manufacturing PDF"

    def _get_report_values(self, docids, data=None):
        docs = self.env["el.product.traceability.manufacturing"].browse(docids)
        return {"doc_ids": docids, "doc_model": docs._name, "docs": docs}
