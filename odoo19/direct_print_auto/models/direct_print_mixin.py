# -*- coding: utf-8 -*-
import logging
from collections import defaultdict

from odoo import models, api, _

_logger = logging.getLogger(__name__)


class DirectPrintMixin(models.AbstractModel):
    """Shared direct-print logic for any business document model.

    Concrete models inheriting this mixin must implement
    ``_get_direct_print_report_ref`` and may override
    ``_should_direct_print_auto`` to add their own filtering logic
    (e.g. only customer invoices, only outgoing pickings).

    The mixin exposes:
        - ``action_direct_print()``  — manual button on the form view
        - ``_trigger_direct_print_after(action)`` — wrap an existing action
          dict with a client action that opens the browser print dialog
          before returning the original action.
    """

    _name = "direct.print.mixin"
    _description = "Direct Print Mixin"

    # ------------------------------------------------------------------
    # API to be implemented / overridden by concrete models
    # ------------------------------------------------------------------
    def _get_direct_print_report_ref(self):
        """Return the XML ID of the report to print (e.g. 'account.account_invoices').

        Concrete models MUST override this method.
        """
        raise NotImplementedError(
            "_get_direct_print_report_ref() must be implemented by the model "
            "that inherits direct.print.mixin"
        )

    def _should_direct_print_auto(self):
        """Return True when auto-print should fire for the current record(s).

        Default behaviour: read the matching toggle on res.config.settings.
        Concrete models may override to add domain filtering (e.g. only
        outgoing pickings). Returning False aborts the auto-print flow.
        """
        return False

    # ------------------------------------------------------------------
    # Manual button entry point
    # ------------------------------------------------------------------
    def action_direct_print(self):
        """Entry point for the "Direct Print" button on the form view.

        Returns a client action (tag=direct_print_auto) carrying the
        report ref and the record ids to print. The OWL client action
        loads the report HTML into a hidden iframe and calls
        ``iframe.contentWindow.print()``.
        """
        self.ensure_one()
        report_ref = self._get_direct_print_report_ref()
        return {
            "type": "ir.actions.client",
            "tag": "direct_print_auto",
            "name": _("Direct Print"),
            "params": {
                "report_ref": report_ref,
                "res_model": self._name,
                "res_ids": self.ids,
                "next_action": False,
            },
        }

    # ------------------------------------------------------------------
    # Auto-print helper used by confirm/post/validate overrides
    # ------------------------------------------------------------------
    def _trigger_direct_print_after(self, original_action):
        """Wrap ``original_action`` so that the browser print dialog opens
        after Odoo's standard flow, then the original action (form reload,
        "return to list", etc.) is dispatched.

        ``original_action`` is the dict returned by ``super().<method>()``.
        If only one record is selected and the model allows auto-print
        for that record, returns a direct_print_auto client action that
        carries the original action as ``next_action``. Otherwise returns
        ``original_action`` untouched.
        """
        if not self:
            return original_action
        # Only auto-print single records (no mass multi-record confirm flow)
        if len(self) > 1:
            _logger.debug(
                "direct_print_auto: skipping auto-print for multi-record "
                "operation on %s (ids=%s)",
                self._name, self.ids,
            )
            return original_action
        record = self[0]
        if not record._should_direct_print_auto():
            return original_action
        report_ref = record._get_direct_print_report_ref()
        return {
            "type": "ir.actions.client",
            "tag": "direct_print_auto",
            "name": _("Direct Print"),
            "params": {
                "report_ref": report_ref,
                "res_model": record._name,
                "res_ids": [record.id],
                "next_action": original_action,
            },
        }
