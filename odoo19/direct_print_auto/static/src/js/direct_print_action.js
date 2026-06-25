/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, xml, onWillStart, useRef, useState, onMounted } from "@odoo/owl";

const actionRegistry = registry.category("actions");

/**
 * Direct Print client action.
 *
 * Params received from the server-side action dict:
 *   - report_ref : string   (XML ID of the ir.actions.report, e.g. "account.account_invoices")
 *   - res_model  : string   (model name of the record, e.g. "account.move")
 *   - res_ids    : number[] (record IDs to print — typically one)
 *   - next_action: object|false (action dict to dispatch after the print dialog closes)
 *
 * Behaviour:
 *   1. Build the URL `/report/html/<report_ref>/<ids>` and set it as the
 *      hidden iframe's `src`.
 *   2. When the iframe finishes loading, call `iframe.contentWindow.print()`.
 *   3. After the print dialog is dismissed, dispatch `next_action`
 *      (typically the action returned by super().action_post()) or close
 *      the client action.
 *
 * Why an iframe instead of `window.print()` directly:
 *   The main Odoo window has its own DOM (toolbar, chatter, etc.). Printing
 *   it would print the UI chrome, not the report. A hidden iframe with the
 *   report HTML lets the browser's print engine print only the report.
 */

const DIRECT_PRINT_TEMPLATE = xml`
    <div class="o_direct_print_auto d-flex flex-column align-items-center justify-content-center"
         style="min-height: 60vh;">
        <t t-if="state.error">
            <div class="alert alert-danger" role="alert">
                <t t-esc="state.error" />
            </div>
            <button class="btn btn-secondary mt-3" t-on-click="onClose">Close</button>
        </t>
        <t t-elif="state.loading">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading…</span>
            </div>
            <p class="mt-3 text-muted">Preparing print preview…</p>
        </t>
        <t t-else="">
            <i class="fa fa-check-circle text-success" style="font-size: 3rem;"></i>
            <p class="mt-3 text-muted">Print dialog closed. Continuing…</p>
        </t>
        <iframe t-ref="printFrame"
                t-on-load="onFrameLoad"
                style="position: absolute; width: 0; height: 0; border: 0; left: -9999px; top: -9999px;"
                t-att-src="state.frameSrc" />
    </div>`;

export class DirectPrintAction extends Component {
    setup() {
        this.actionService = useService("action");
        this.state = useState({
            loading: true,
            error: false,
            frameSrc: "",
        });
        this.printFrame = useRef("printFrame");
        this._printed = false;

        onWillStart(async () => {
            this._preparePrint();
        });
    }

    /**
     * Build the /report/html/<ref>/<ids> URL and assign it as the iframe src.
     * The iframe's `load` event will fire `onFrameLoad` once the report HTML
     * has been fetched and rendered inside the iframe.
     */
    _preparePrint() {
        const params = this.props.action.params || {};
        const reportRef = params.report_ref;
        const resIds = params.res_ids || [];
        if (!reportRef || !resIds.length) {
            this.state.loading = false;
            this.state.error =
                "Direct Print: missing report_ref or res_ids in action params.";
            return;
        }
        const idsPath = Array.isArray(resIds) ? resIds.join(",") : String(resIds);
        // Same-origin request — the Odoo backend serves this route itself.
        // The report route handles access control (the user must have read
        // access on res_model/res_ids, otherwise the route returns 403).
        this.state.frameSrc = `/report/html/${encodeURIComponent(reportRef)}/${idsPath}`;
    }

    /**
     * Called when the hidden iframe finishes loading the report HTML.
     * Triggers the browser's native print dialog. After the dialog is
     * dismissed (either the user clicked Print or Cancel), we dispatch
     * the next_action.
     */
    onFrameLoad() {
        if (this._printed) {
            return;
        }
        const frame = this.printFrame.el;
        if (!frame || !frame.contentWindow) {
            this.state.loading = false;
            this.state.error = "Direct Print: could not access print frame.";
            return;
        }
        try {
            this._printed = true;
            // Small delay to let report CSS/fonts settle inside the iframe
            // before invoking the print dialog.
            setTimeout(() => {
                frame.focus();
                frame.contentWindow.print();
                this.state.loading = false;
                // Dispatch the follow-up action after the print dialog has
                // closed. The 400 ms delay gives the browser time to clean
                // up its print pipeline before we navigate away.
                setTimeout(() => this._dispatchNext(), 400);
            }, 350);
        } catch (err) {
            this.state.loading = false;
            this.state.error = `Direct Print: ${err.message}`;
        }
    }

    /**
     * Dispatch the next action (typically the original confirm/post action
     * returned by super()). If no next_action is provided, simply close
     * the client action.
     */
    _dispatchNext() {
        const params = this.props.action.params || {};
        const nextAction = params.next_action;
        if (nextAction && typeof nextAction === "object") {
            this.actionService.doAction(nextAction);
        } else {
            // No follow-up action: close the client action (returns user
            // to whatever view they were on before).
            this.actionService.doAction({ type: "ir.actions.act_window_close" });
        }
    }

    onClose() {
        this.actionService.doAction({ type: "ir.actions.act_window_close" });
    }
}

DirectPrintAction.template = DIRECT_PRINT_TEMPLATE;

actionRegistry.add("direct_print_auto", DirectPrintAction);
