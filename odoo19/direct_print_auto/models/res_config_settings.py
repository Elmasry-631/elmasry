# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Adds Direct Print toggles to the Sales settings tab.

    One boolean per supported document type controls whether auto-print
    fires on confirm/post/validate/approve. A final boolean controls the
    global behaviour of the manual button: open the browser print dialog
    (True, default) or simply download the PDF (False).
    """

    _inherit = "res.config.settings"

    # Auto-print toggles — one per supported doc type
    direct_print_invoice_auto = fields.Boolean(
        string="Auto-print Customer Invoices",
        config_parameter="direct_print_auto.invoice_auto",
        help="When a customer invoice or refund is posted, automatically "
             "open the browser print dialog for the invoice report.",
    )
    direct_print_so_auto = fields.Boolean(
        string="Auto-print Sales Orders",
        config_parameter="direct_print_auto.so_auto",
        help="When a sales order is confirmed, automatically open the "
             "browser print dialog for the order report.",
    )
    direct_print_picking_auto = fields.Boolean(
        string="Auto-print Delivery Slips",
        config_parameter="direct_print_auto.picking_auto",
        help="When an outgoing delivery picking is validated, automatically "
             "open the browser print dialog for the delivery slip.",
    )
    direct_print_po_auto = fields.Boolean(
        string="Auto-print Purchase Orders",
        config_parameter="direct_print_auto.po_auto",
        help="When a purchase order is approved, automatically open the "
             "browser print dialog for the PO report.",
    )
    direct_print_open_dialog = fields.Boolean(
        string="Open Print Dialog for Manual Button",
        config_parameter="direct_print_auto.open_dialog",
        default=True,
        help="If set, the Direct Print button on the form view opens the "
             "browser's print dialog. If not set, the button simply "
             "downloads the PDF.",
    )
