
odoo.define('goGP.gogpkanban', function(require) {
"use strict";
var KanbanRecord = require('web.KanbanRecord');

KanbanRecord.include({
        /**
     * Renders the record
     *
     * @returns {Promise}
     */
    _render: function () {
        var self = this;
        if (this.modelName == 'gogp.social_groups'){
            this.defs = [];

            // call 'on_detach_callback' on each subwidget as they will be removed
            // from the DOM at the next line
            _.invoke(this.subWidgets, 'on_detach_callback');
            var result =  this._rpc({
                model: 'res.partner',
                method: 'search_read',
                domain: [
                    ['id', 'in', self.qweb_context.record.partner_ids.raw_value],
                ],
                fields: ['name','email','phone','mobile'],
            }).then(function(res){
                self.qweb_context.record.partner_ids.raw_value = res
                self._replaceElement(self.qweb.render('kanban-box', self.qweb_context));
                self.$el.addClass('o_kanban_record').attr("tabindex", 0);
                self.$el.attr('role', 'article');
                self.$el.data('record', self);
                // forcefully add class oe_kanban_global_click to have clickable record always to select it
                if (self.selectionMode) {
                    self.$el.addClass('oe_kanban_global_click');
                }
                if (self.$el.hasClass('oe_kanban_global_click') ||
                    self.$el.hasClass('oe_kanban_global_click_edit')) {
                    self.$el.on('click', self._onGlobalClick.bind(self));
                    self.$el.on('keydown', self._onKeyDownCard.bind(self));
                } else {
                    self.$el.on('keydown', self._onKeyDownOpenFirstLink.bind(self));
                }
                self._processFields();
                self._processWidgets();
                self._setupColor();
                self._setupColorPicker();
                self._attachTooltip();

                // We use boostrap tooltips for better and faster display
                self.$('span.o_tag').tooltip({ delay: { 'show': 50 } });

                return Promise.all(self.defs);
            })
        }
        else{
             self._super.apply(self, arguments);
        }

    },
});

});
