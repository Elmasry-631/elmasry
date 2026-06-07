/** @odoo-module */

import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { FormController } from "@web/views/form/form_controller";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

let menu_group = false;

patch(FormController.prototype,{

    setup(){
        super.setup();
        this.actionService = useService("action");
        var def_delete = user.hasGroup('bi_global_custom_fields.global_custom_fields_group').then(function (has_delete_group) {
            if(has_delete_group){
                menu_group = has_delete_group;
            }      
        });
    },

    getStaticActionMenuItems() {
        const { activeActions } = this.archInfo;
        return {
            archive: {
                isAvailable: () => this.archiveEnabled && this.model.root.isActive,
                sequence: 10,
                description: _t("Archive"),
                icon: "oi oi-archive",
                callback: () => {
                    this.dialogService.add(ConfirmationDialog, this.archiveDialogProps);
                },
            },
            unarchive: {
                isAvailable: () => this.archiveEnabled && !this.model.root.isActive,
                sequence: 20,
                icon: "oi oi-unarchive",
                description: _t("Unarchive"),
                callback: () => this.model.root.unarchive(),
            },
            duplicate: {
                isAvailable: () => activeActions.create && activeActions.duplicate,
                sequence: 30,
                icon: "fa fa-clone",
                description: _t("Duplicate"),
                callback: () => this.duplicateRecord(),
            },
            delete: {
                isAvailable: () => activeActions.delete && !this.model.root.isNew,
                sequence: 40,
                icon: "fa fa-trash-o",
                description: _t("Delete"),
                callback: () => this.deleteRecord(),
                skipSave: true,
            },
            field: {
                isAvailable: function() {
                    return menu_group;
                },
                sequence: 50,
                icon: "fa fa-custom-icon1",
                description: _t("Add Global Custom Fields"),
                callback: function() {
                    this.env.services.action.doAction({
                        name: 'Add Global Custom Fields Wizard', 
                        type: 'ir.actions.act_window',
                        res_model: 'ir.models.fields.custom', 
                        target: 'new',
                        views: [[false, 'form']],
                        context:{
                            'active_model': this.props.resModel
                        },
                    });
                }.bind(this),
            },
            tab: {
                isAvailable: function() {
                    return menu_group;
                },
                sequence: 60,
                icon: "fa fa-custom-icon1",
                description: _t("Add Global Custom Tabs"),
                callback: function() {
                    this.env.services.action.doAction({
                        name: 'Add Global Custom Tabs Wizard', 
                        type: 'ir.actions.act_window',
                        res_model: 'ir.global.tabs', 
                        target: 'new',
                        views: [[false, 'form']],
                        context:{
                            'active_model': this.props.resModel
                        },
                    });
                }.bind(this),
            },
            addPropertyFieldValue: {
                isAvailable: () => activeActions.addPropertyFieldValue,
                sequence: 50,
                icon: "fa fa-cogs",
                description: _t("Add Properties"),
                callback: () => this.model.bus.trigger("PROPERTY_FIELD:ADD_PROPERTY_VALUE"),
            },
        };
    }

});
