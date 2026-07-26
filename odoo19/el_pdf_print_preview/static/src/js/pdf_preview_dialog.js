/** @odoo-module **/
/*
 * el_pdf_print_preview — PDF Preview Dialog (OWL Component)
 * ==========================================================
 *
 * An OWL Dialog component that embeds the PDF.js viewer in an iframe.
 * The viewer URL is: /el_pdf_print_preview/static/lib/pdfjs/web/viewer.html?file=<pdf_url>
 *
 * v1.1.2 FIX (vs original):
 *   - Uses env.services.dialog.add() (correct O19 pattern)
 *   - Fixed title="props.title" bug (was passing literal string)
 *   - Proper OWL component with useService("dialog")
 *   - Exported function openPDFPreviewDialog() for non-component callers
 */

import { Component, useRef, onMounted, onWillUnmount } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { _t } from "@web/core/l10n/translation";

// ─── PDF Preview Dialog Component ──────────────────────────────────────
export class PDFPreviewDialog extends Component {
    static template = "el_pdf_print_preview.PDFPreviewDialog";
    static components = { Dialog };
    static props = {
        pdfUrl: String,
        title: { type: String, optional: true },
        close: Function,
    };

    setup() {
        this.iframe = useRef("iframe");

        // Build the PDF.js viewer URL
        this.viewerUrl =
            "/el_pdf_print_preview/static/lib/pdfjs/web/viewer.html?file=" +
            encodeURIComponent(this.props.pdfUrl);

        onMounted(() => {
            if (this.iframe.el) {
                this.iframe.el.src = this.viewerUrl;
            }
        });

        onWillUnmount(() => {
            // Clean up iframe to prevent memory leaks
            if (this.iframe.el) {
                this.iframe.el.src = "about:blank";
            }
        });
    }

    get dialogTitle() {
        return this.props.title || _t("PDF Preview");
    }

    onClose() {
        this.props.close();
    }
}

// ─── Exported function to open the dialog from anywhere ───────────────
/**
 * Open the PDF preview dialog.
 *
 * @param {string} pdfUrl - The URL of the PDF to preview
 * @param {string} title - Dialog title
 * @param {Object} env - The Odoo environment (with services)
 */
export function openPDFPreviewDialog(pdfUrl, title, env) {
    if (!env || !env.services || !env.services.dialog) {
        console.error("[el_pdf_print_preview] Dialog service not available");
        // Fallback: open in new tab
        const viewerUrl =
            "/el_pdf_print_preview/static/lib/pdfjs/web/viewer.html?file=" +
            encodeURIComponent(pdfUrl);
        window.open(viewerUrl, "_blank");
        return;
    }

    env.services.dialog.add(PDFPreviewDialog, {
        pdfUrl: pdfUrl,
        title: title || _t("PDF Preview"),
    });
}
