/** @odoo-module **/

import { Component, useRef, onMounted } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

export class PDFPreviewDialog extends Component {
    static template = "pdf_print_preview.PDFPreviewDialog";
    static components = { Dialog };
    static props = {
        viewerUrl: String,
        title: { type: String, optional: true },
        close: Function,
    };

    setup() {
        this.iframe = useRef("iframe");
        onMounted(() => {
            if (this.iframe.el) {
                this.iframe.el.src = this.props.viewerUrl;
            }
        });
    }

    get title() {
        return this.props.title || _t("Preview");
    }
}

/**
 * Open PDF preview using the dialog service
 */
export function openPDFPreview(url, title = _t("Preview")) {
    const viewerUrl = `/pdf_print_preview/static/lib/pdfjs/web/viewer.html?file=${encodeURIComponent(url)}`;
    const dialogService = registry.category("services").get("dialog");
    
    if (dialogService) {
        // في أودو الحديث، نستخدم خدمة الحوار لإضافة المكون
        const addDialog = registry.category("services").get("dialog").add;
        addDialog(PDFPreviewDialog, { viewerUrl, title });
    } else {
        // احتياطي في حال عدم توفر الخدمة (نادراً في أودو 18)
        console.error("Dialog service not found");
    }
}

// تسجيل الخدمة
registry.category("services").add("pdf_preview", {
    start() {
        return { openPDFPreview };
    },
});
