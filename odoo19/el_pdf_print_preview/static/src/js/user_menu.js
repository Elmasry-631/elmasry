/** @odoo-module **/
/*
 * el_pdf_print_preview — User Menu Entry (Odoo 19)
 * ==================================================
 *
 * Adds a "Report Preview Settings" entry to the user menu (top-right).
 * Opens a dialog form where the user can toggle preview_print and
 * automatic_printing.
 *
 * v1.1.2 FIX (vs original):
 *   - Uses doAction("xml_id") directly (not /web/action/load with string ID)
 *   - Simplified RPC (removed dead fallback branches)
 *   - Sets res_id to current user via context
 */

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";
import { user } from "@web/core/user";

function ReportPreviewMenuItem(env) {
    return {
        type: "item",
        id: "report_preview_settings",
        description: _t("Report Preview Settings"),
        callback: () => {
            const userId = user.userId;
            env.services.action.doAction({
                type: "ir.actions.act_window",
                name: _t("Preview Settings"),
                res_model: "res.users",
                res_id: userId,
                view_mode: "form",
                target: "new",
                views: [
                    [false, "form"],
                ],
                context: {
                    default_preview_print: true,
                },
            });
        },
        sequence: 50,
    };
}

registry.category("user_menuitems").add(
    "report_preview_settings",
    ReportPreviewMenuItem
);
