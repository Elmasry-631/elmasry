/** @odoo-module **/

import { useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useRecordObserver } from "@web/model/relational_model/utils";
import { selectionField, SelectionField } from "@web/views/fields/selection/selection_field";
import { useService } from "@web/core/utils/hooks";

export class ButtonSelectorField extends SelectionField {
    static template = "el_button_access_control.ButtonSelector";

    setup() {
        super.setup();
        this.orm = useService("orm");
        let lastModelId = null;
        let lastViewType = null;

        useRecordObserver(async (record) => {
            const modelId = record.data.model_id?.id || null;
            const viewType = record.data.view_type || "form";
            const field = record.fields[this.props.name];
            const currentValue = record.data[this.props.name];

            if (modelId === lastModelId && viewType === lastViewType) {
                return;
            }
            lastModelId = modelId;
            lastViewType = viewType;

            if (!modelId) {
                field.selection = [
                    [false, ""],
                    ...field.selection.filter(([val]) => val && val === currentValue),
                ];
                return;
            }

            try {
                const buttons = await this.orm.call(
                    "el.button.access.rule",
                    "rpc_get_available_buttons",
                    [modelId, viewType]
                );

                const newSelection = [[false, ""]];
                for (const btn of buttons) {
                    newSelection.push([btn.name, `${btn.name} \u2014 ${btn.label}`]);
                }

                if (currentValue && !newSelection.some(([val]) => val === currentValue)) {
                    newSelection.push([currentValue, currentValue]);
                }

                field.selection = newSelection;
            } catch (e) {
                console.error("[ButtonSelector] RPC error:", e);
            }
        });
    }
}

export const buttonSelectorField = {
    ...selectionField,
    component: ButtonSelectorField,
    supportedTypes: ["selection"],
};

registry.category("fields").add("button_selector", buttonSelectorField);
