/**
 * Dashboard Builder - Calendar Widget
 * 
 * Renders calendar view for date-based records.
 */

odoo.define('el_dashboard_builder.widgets.Calendar', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var _t = core._t;
    var qweb = core.qweb;

    var CalendarWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.CalendarWidget',
        calendar: null,

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.model = options.config.model;
            this.dateStart = options.config.date_start;
            this.dateStop = options.config.date_stop || options.config.date_start;
            this.titleField = options.config.title_field;
            this.colorField = options.config.color_field;
            this.domain = options.config.domain || [];
            this.defaultView = options.config.default_view || 'month';
            this.showWeekends = options.config.show_weekends !== false;
            this.allDaySlot = options.config.all_day_slot !== false;
            this.slotDuration = options.config.slot_duration || '00:30:00';
        },

        willStart: function () {
            return this._super.apply(this, arguments).then(function () {
                return this._fetchEvents();
            }.bind(this));
        },

        _fetchEvents: function () {
            var self = this;
            var domain = this.domain.slice();
            
            if (this.globalFilters) {
                domain = domain.concat(this.globalFilters);
            }

            var fields = [this.dateStart, this.dateStop, this.titleField];
            if (this.colorField) {
                fields.push(this.colorField);
            }

            return rpc.query({
                model: this.model,
                method: 'search_read',
                args: [domain, fields],
            }).then(function (records) {
                self.events = records.map(function (record) {
                    var start = record[self.dateStart];
                    var end = record[self.dateStop];
                    var title = record[self.titleField];
                    var color = self.colorField ? record[self.colorField] : undefined;
                    
                    // Handle many2one fields
                    if (Array.isArray(title)) title = title[1];
                    if (Array.isArray(color)) color = color[1];
                    
                    return {
                        title: title,
                        start: start,
                        end: end,
                        color: color,
                        record_id: record.id,
                    };
                });
            });
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self._renderCalendar();
            });
        },

        _renderCalendar: function () {
            var self = this;
            var $calendar = this.$('.o_calendar_canvas');
            
            if (!window.FullCalendar) {
                $container.html('<div class="alert alert-warning">FullCalendar library not loaded</div>');
                return;
            }
            
            if (this.calendar) {
                this.calendar.destroy();
            }
            
            this.calendar = new FullCalendar.Calendar($calendar[0], {
                initialView: this.defaultView,
                events: this.events || [],
                weekends: this.showWeekends,
                allDaySlot: this.allDaySlot,
                slotDuration: this.slotDuration,
                headerToolbar: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'dayGridMonth,timeGridWeek,timeGridDay',
                },
                eventClick: function (info) {
                    if (info.event.extendedProps.record_id) {
                        self.do_action({
                            type: 'ir.actions.act_window',
                            res_model: self.model,
                            res_id: info.event.extendedProps.record_id,
                            view_mode: 'form',
                            target: 'current',
                        });
                    }
                },
                eventDidMount: function (info) {
                    if (info.event.backgroundColor) {
                        info.el.style.backgroundColor = info.event.backgroundColor;
                        info.el.style.borderColor = info.event.backgroundColor;
                    }
                },
            });
            
            this.calendar.render();
        },

        destroy: function () {
            if (this.calendar) {
                this.calendar.destroy();
            }
            this._super.apply(this, arguments);
        },
    });

    // Register widget component
    window.DashboardCalendar = CalendarWidget;
    return CalendarWidget;
});