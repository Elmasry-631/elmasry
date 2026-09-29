/** @odoo-module **/
import { session } from "@web/session";
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

if (session.is_readonly_user) {
    patch(FormController.prototype, {
        setup() {
            super.setup();
            this.canCreate = false;
            this.canEdit = false;
        },
    });
}
