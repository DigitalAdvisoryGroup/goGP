odoo.define('goGP.portal', function (require) {
    'use strict';

    var core = require('web.core');
    var publicWidget = require('web.public.widget');
    var _t = core._t;
    var Dialog = require('web.Dialog');

    $(document).ready(function(){
        var delete_id;
        $("button.delete-btn").on('click', function (ev) {
            $('.popup_open').modal('show');
            delete_id = window.location.origin+'/my/gogp/vehicle/delete/'+ev.currentTarget.previousElementSibling.value
            $("a.delete-confirm").attr("href", delete_id);
        });

        $('select[name="brand_id"]').change(function(e){
            var brand_id = $(this).val();
            $('select[name="model_id"]').val("");
            $('select[name="model_id"]').find('option').removeAttr('selected');
            $('select[name="model_id"]').find('option').hide();
            $('select[name="model_id"]').find(`option[brand_id="${brand_id}"]`).show();
        });
        if($('select[name="brand_id"]').length == 1 & $('select[name="model_id"]').length == 1){
            var brand_id = $('select[name="brand_id"]').val();
            var model_id = $('select[name="model_id"]').val();
            $('select[name="model_id"]').val("");
            $('select[name="model_id"]').find('option').hide();
            $('select[name="model_id"]').find(`option[brand_id="${brand_id}"]`).show();
            $('select[name="model_id"]').val(model_id);
        }

    });
      $(document).on('submit','#attendee_registration',function(){
            debugger;
            var values = $(this).find("input[type='email']")
                      .map(function(){return $(this).val();}).get();
            debugger
            var unique_email = _.unique(values);
            if(unique_email.length != values.length){
                $("#attendee_registration").find('.b-submit').removeAttr('disabled');
                $("#attendee_registration").find('.fa-spinner').remove();
                 var buttons = [
                {
                    text: _t("Ok"),
                    close: true,
                }
            ];
                var dialog = new Dialog(this, {
                buttons: buttons,
                title: _t("Please enter unique email for each ticket"),
            }).open();
            }
            else {
            return true
            }
            return false
        });

    publicWidget.registry.PortalAvatar = publicWidget.Widget.extend({
        selector: '#gogp_portal_avatar',
        read_events: {
            'click .gogp_portal_avatar_edit': '_onEditAvatarClick',
            'change .gogp_portal_avatar_upload': '_onAvatarUploadChange',
            'click .gogp_portal_avatar_clear': '_onClearAvatarClick',
        },

        init: function () {
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
        },

        _onEditAvatarClick: function (ev) {
            ev.preventDefault();
            $(ev.currentTarget).closest('form').find('.gogp_portal_avatar_upload').trigger('click');
        },

        _onAvatarUploadChange: function (ev) {
            if (!ev.currentTarget.files.length) {
                return;
            }
            $.blockUI()
            var $form = $(ev.currentTarget).closest('form');
            var reader = new window.FileReader();
            reader.readAsDataURL(ev.currentTarget.files[0]);
            reader.onload = function (ev) {
                $form.find('.gogp_portal_avatar_img').attr('src', ev.target.result);
                $form.find('.gogp_portal_avatar_img').attr('style', 'border-radius: 50%; width: 128px; height: 128px;');
                $.unblockUI();
            };
            $form.find('#portal_clear_avatar').remove();
        },

        _onClearAvatarClick: function (ev) {
            var $form = $(ev.currentTarget).closest('form');
            $form.find('.gogp_portal_avatar_img').attr('src', '/web/static/src/img/placeholder.png');
            $form.find('.gogp_portal_avatar_img').attr('style', 'border-radius: 50%; width: 128px; height: 128px;')
            $form.append($('<input/>', {
                name: 'clear_avatar',
                id: 'portal_clear_avatar',
                type: 'hidden',
            }));
        },
    })
});
