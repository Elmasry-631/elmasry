/**
 * Dashboard Builder - HTML/Markdown Widget
 * 
 * Renders custom HTML or Markdown content.
 */

odoo.define('el_dashboard_builder.widgets.Html', function (require) {
    "use strict";

    var AbstractWidget = require('el_dashboard_builder.widgets.AbstractWidget');
    var core = require('web.core');

    var _t = core._t;
    var qweb = core.qweb;

    var HtmlWidget = AbstractWidget.extend({
        template: 'el_dashboard_builder.HtmlWidget',

        init: function (parent, options) {
            this._super.apply(this, arguments);
            this.content = options.config.content || '';
            this.contentType = options.config.content_type || 'html';
            this.sanitize = options.config.sanitize !== false;
            this.variables = options.config.variables || {};
        },

        willStart: function () {
            return this._super.apply(this, arguments);
        },

        _renderContent: function () {
            var content = this.content;
            
            // Replace template variables
            Object.keys(this.variables).forEach(function (key) {
                var regex = new RegExp('{{' + key + '}}', 'g');
                content = content.replace(regex, this.variables[key]);
            }.bind(this));
            
            // Also replace from global context
            if (this.globalContext) {
                Object.keys(this.globalContext).forEach(function (key) {
                    var regex = new RegExp('{{' + key + '}}', 'g');
                    content = content.replace(regex, this.globalContext[key]);
                }.bind(this));
            }
            
            if (this.contentType === 'markdown') {
                // Simple markdown rendering (would use a markdown library in production)
                content = this._markdownToHtml(content);
            }
            
            if (this.sanitize) {
                content = this._sanitizeHtml(content);
            }
            
            return content;
        },

        _markdownToHtml: function (md) {
            // Very basic markdown conversion
            return md
                .replace(/^### (.*$)/gim, '<h3>$1</h3>')
                .replace(/^## (.*$)/gim, '<h2>$1</h2>')
                .replace(/^# (.*$)/gim, '<h1>$1</h1>')
                .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
                .replace(/\*(.*)\*/gim, '<em>$1</em>')
                .replace(/`(.*)`/gim, '<code>$1</code>')
                .replace(/\[([^\]]+)\]\(([^)]+)\)/gim, '<a href="$2" target="_blank">$1</a>')
                .replace(/^\- (.*$)/gim, '<li>$1</li>')
                .replace(/\n/gim, '<br>');
        },

        _sanitizeHtml: function (html) {
            // Basic sanitization - in production use DOMPurify or similar
            var allowedTags = ['p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 
                              'ul', 'ol', 'li', 'a', 'code', 'pre', 'blockquote', 'div', 'span',
                              'table', 'thead', 'tbody', 'tr', 'th', 'td', 'img'];
            var allowedAttrs = ['href', 'target', 'src', 'alt', 'class', 'style', 'id'];
            
            // This is a placeholder - real implementation would use a proper sanitizer
            return html;
        },

        start: function () {
            var self = this;
            return this._super.apply(this, arguments).then(function () {
                self.$('.o_html_content').html(self._renderContent());
            });
        },
    });

    window.DashboardHtml = HtmlWidget;
    return HtmlWidget;
});