/** @odoo-module **/

import { registry } from "@web/core/registry";
import { openPDFPreview } from "./dialog";
import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";

async function getReportUrl(action, env, filename) {
    let url = "/report/pdf/" + action.report_name;
    const actionContext = action.context || {};
    filename = filename || action.name;

    if (action.data && JSON.stringify(action.data) !== "{}") {
        url += "?options=" + encodeURIComponent(JSON.stringify(action.data)) +
               "&context=" + encodeURIComponent(JSON.stringify(actionContext)) + "&";
    } else if (actionContext.active_ids) {
        url += "/" + actionContext.active_ids.join(",") +
               "?context=" + encodeURIComponent(JSON.stringify(env.services.user.context)) + "&";
    }

    if (filename) {
        filename = filename.replace(/[/?%#&=]/g, "_") + ".pdf";
        url += "filename=" + filename;
    }
    return url;
}

export async function PdfPrintPreview(action, options, env) {
    if (action.report_type !== "qweb-pdf") return;

    const notification = env.services.notification;
    const menu = env.services.menu;
    const rpc = env.services.rpc;

    if (!menu.getCurrentApp()) return;

    let result;
    try {
        if (typeof rpc === 'function') {
            result = await rpc('/pdf_print_preview/get_report_name', {
                report_name: action.report_name,
                data: JSON.stringify(action.context)
            });
        } else if (rpc && typeof rpc.call === 'function') {
            result = await rpc.call('/pdf_print_preview/get_report_name', {
                report_name: action.report_name,
                data: JSON.stringify(action.context)
            });
        } else {
            // Fallback if RPC is not available as expected
            result = {
                file_name: action.name,
                wkhtmltopdf_state: 'ok'
            };
        }
    } catch (err) {
        console.error("RPC call failed:", err);
        result = {
            file_name: action.name,
            wkhtmltopdf_state: 'ok'
        };
    }

    const state = result.wkhtmltopdf_state;
    const WKHTMLTOPDF_MESSAGES = {
        broken: _t("Your installation of Wkhtmltopdf seems to be broken."),
        install: _t("Unable to find Wkhtmltopdf on this system."),
        upgrade: _t("Please upgrade Wkhtmltopdf to at least 0.12.0."),
        workers: _t("You need to start Odoo with at least two workers."),
    };

    if (state in WKHTMLTOPDF_MESSAGES) {
        notification.add(WKHTMLTOPDF_MESSAGES[state], { sticky: true, title: _t("Report") });
    }

    if (state === "upgrade" || state === "ok") {
        const url = await getReportUrl(action, env, result.file_name);

        if (session.preview_print) {
            openPDFPreview(url, action.name);
        }

        if (session.automatic_printing) {
            try {
                const pdf = window.open(url);
                pdf.print();
            } catch (err) {
                notification.add(
                    _t("Please allow popups in your browser to preview the report."),
                    { sticky: true, title: _t("Report") }
                );
            }
        }
        return true;
    }
}

registry.category("actions").add("pdf_print_preview", PdfPrintPreview);
