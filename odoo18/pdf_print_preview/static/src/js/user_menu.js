/** @odoo-module **/

import { registry } from "@web/core/registry";
import { _t } from "@web/core/l10n/translation";

function ReportPreviewItem(env) {
    return {
        type: "item",
        id: "report_preview",
        description: _t("Report preview"),
        callback: async function () {
            // في أودو 18، خدمة rpc هي كائن يحتوي على دالة call أو يتم استدعاؤها مباشرة في بعض الحالات
            // الطريقة الأكثر استقراراً هي استخدام env.services.rpc مباشرة إذا كانت دالة، 
            // أو استخدام env.services.action لفتح الأكشن مباشرة دون الحاجة لـ RPC يدوي إذا أمكن
            try {
                const actionService = env.services.action;
                const rpcService = env.services.rpc;
                
                // محاولة تحميل الأكشن عبر RPC
                let actionDescription;
                if (typeof rpcService === 'function') {
                    actionDescription = await rpcService("/web/action/load", {
                        action_id: "pdf_print_preview.action_short_preview_print"
                    });
                } else if (rpcService && typeof rpcService.call === 'function') {
                    actionDescription = await rpcService.call("/web/action/load", {
                        action_id: "pdf_print_preview.action_short_preview_print"
                    });
                } else {
                    // إذا فشل كل شيء، نستخدم doAction بالاسم التقني مباشرة وهو مدعوم في أودو
                    return actionService.doAction("pdf_print_preview.action_short_preview_print");
                }
                
                actionDescription.res_id = env.services.user.userId;
                actionService.doAction(actionDescription);
            } catch (err) {
                console.error("Failed to open preview settings:", err);
                // محاولة أخيرة باستخدام الاسم التقني
                env.services.action.doAction("pdf_print_preview.action_short_preview_print");
            }
        },
        sequence: 50,
    };
}

registry.category("user_menuitems").add("report_preview", ReportPreviewItem);
