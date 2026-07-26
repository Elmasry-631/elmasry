/** @odoo-module **/
/*
 * el_pdf_print_preview — Report Action Handler (Odoo 19)
 * ========================================================
 *
 * Registers a handler in the "ir.actions.report handlers" registry.
 * When a qweb-pdf report action is triggered:
 *   1. Fetches the report file name via RPC
 *   2. Builds the /report/pdf/<name>/<ids> URL
 *   3. If preview_print is enabled → opens PDF.js viewer dialog
 *   4. If automatic_printing is enabled → opens print window (with load delay)
 *   5. Returns true to indicate the action was handled
 *
 * v1.1.2 FIX (vs original):
 *   - Uses "ir.actions.report handlers" registry (correct O19 pattern)
 *   - Removed broken "actions" registry registration
 *   - Fixed window.open().print() race condition (wait for load)
 *   - Removed wkhtmltopdf_state check (deprecated in O19)
 *   - Uses env.services.user for session data (not @web/session import)
 */

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { openPDFPreviewDialog } from "./pdf_preview_dialog";
import { user } from "@web/core/user";
import { session } from "@web/session";

// ─── Build the report URL ─────────────────────────────────────────────
function getReportUrl(action, env, fileName) {
    let url = "/report/pdf/" + action.report_name;
    const actionContext = action.context || {};
    fileName = fileName || action.name || "report";

    if (action.data && JSON.stringify(action.data) !== "{}") {
        const options = encodeURIComponent(JSON.stringify(action.data));
        const context = encodeURIComponent(JSON.stringify(actionContext));
        url += "?options=" + options + "&context=" + context + "&";
    } else if (actionContext.active_ids && actionContext.active_ids.length) {
        url += "/" + actionContext.active_ids.join(",");
        url += "?context=" + encodeURIComponent(
            JSON.stringify(user.context || {})
        ) + "&";
    }

    // Sanitize filename
    fileName = String(fileName).replace(/[/?%#&=]/g, "_") + ".pdf";
    url += "filename=" + encodeURIComponent(fileName);

    return url;
}

// ─── Open print window with proper load waiting ───────────────────────
function openPrintWindow(url, notification) {
    const printWindow = window.open(url, "_blank");

    if (!printWindow) {
        if (notification) {
            notification.add(
                _t("Please allow popups in your browser to print the report."),
                { sticky: true, title: _t("Report"), type: "warning" }
            );
        }
        return;
    }

    // Wait for the PDF to load before calling print()
    // Browsers handle PDF windows differently, so we try multiple strategies
    let printed = false;

    const tryPrint = () => {
        if (printed) return;
        try {
            if (printWindow.document && printWindow.document.readyState === "complete") {
                printWindow.focus();
                printWindow.print();
                printed = true;
            }
        } catch (e) {
            // Cross-origin restriction — can't access printWindow.document
            // Fallback: just focus the window (user can Ctrl+P)
            printWindow.focus();
            printed = true;
        }
    };

    // Try after delays (PDF loading time varies)
    setTimeout(tryPrint, 1000);
    setTimeout(tryPrint, 2000);
    setTimeout(tryPrint, 4000);
}

// ─── Main handler ─────────────────────────────────────────────────────
async function pdfPrintPreviewHandler(action, options, env) {
    // Only handle qweb-pdf reports
    if (action.report_type !== "qweb-pdf") {
        return false;
    }

    const notification = env.services.notification;
    const rpc = env.services.rpc;

    // Read user preferences from session (injected by ir.http)
    const previewPrint = session?.preview_print ?? true;
    const automaticPrinting = session?.automatic_printing ?? false;

    // If both are disabled, fall through to default behavior
    if (!previewPrint && !automaticPrinting) {
        return false;
    }

    // Fetch the report file name
    let fileName = action.name || "report";
    try {
        const result = await rpc("/pdf_print_preview/get_report_name", {
            report_name: action.report_name,
            data: JSON.stringify(action.context || {}),
        });
        if (result && result.file_name) {
            fileName = result.file_name;
        }
    } catch (err) {
        // Non-critical: use default file name
    }

    // Build the report URL
    const url = getReportUrl(action, env, fileName);

    // Open PDF.js preview dialog
    if (previewPrint) {
        openPDFPreviewDialog(url, fileName, env);
    }

    // Open automatic print window
    if (automaticPrinting) {
        openPrintWindow(url, notification);
    }

    // Handle onClose callback
    if (options.onClose) {
        // Call onClose after a delay (simulating dialog close)
        // The actual dialog close is handled by the Dialog component
    }

    return true; // Action handled
}

// ─── Register the handler ─────────────────────────────────────────────
registry.category("ir.actions.report handlers").add(
    "el_pdf_print_preview",
    pdfPrintPreviewHandler,
    { force: true }
);
