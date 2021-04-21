odoo.define('web_image_zoom_cr.imagepreview', function (require) {
"use strict";


var core = require('web.core');
var QWeb = core.qweb;
var BasicFields = require('web.basic_fields');
var KanbanRenderer = require('web.KanbanRenderer');

	KanbanRenderer.include({
		
		_addImageHoverEvent : function(){
			var self = this;
			if(self.$el.find('.o_kanban_image_fill_left').length > 0 || self.$el.find('.o_kanban_image_fill_right').length > 0 || self.$el.find('.o_kanban_image_full').length > 0 || self.$el.find('.o_kanban_image').length > 0) {
				clearInterval(self.imagehoverinterval);
				self.$el.find('.o_kanban_image_fill_left').unbind('click').bind('click',function(ev){
					ev.preventDefault();
					ev.stopPropagation();
					var imagesrc = false;
					
					if($(this).css('background-image') && $(this).css('background-image').includes('url(')) {
						imagesrc = $(this).css('background-image').replace('url(','').replace(')','').replace(/\"/gi, "");
					}
					
					else if($(this).attr('src')) {
						imagesrc = $(this).attr('src')
					}
					
					else if($(this).find('img').length > 0) {
						imagesrc = $(this).find('img').attr('src')
					}
					
					
					if(imagesrc) {
						$('#ImageZoomModal').modal('hide');
						$('#ImageZoomModal').remove()
						var $imageModal = QWeb.render('web_image_zoom_cr.ImageZoom');
						var imageclone = '<img src="' + imagesrc + '" style="width:100%;"></img>';
						$('body').append($imageModal);
						$('#ImageZoomModal').find('.image-body').append(imageclone)
						$('#ImageZoomModal').find('a.download_img').attr('href',imagesrc)
						$('#ImageZoomModal').modal('show');
					}
				});
						
						
				self.$el.find('.o_kanban_image_fill_right').unbind('click').bind('click',function(ev){
					ev.preventDefault();
					ev.stopPropagation();
					
					var imagesrc = false;
					if($(this).css('background-image') && $(this).css('background-image').includes('url(')) {
						imagesrc = $(this).css('background-image').replace('url(','').replace(')','').replace(/\"/gi, "");
					}
					
					else if($(this).attr('src')) {
						imagesrc = $(this).attr('src')
					}
					
					else if($(this).find('img').length > 0) {
						imagesrc = $(this).find('img').attr('src')
					}
					
					
					if(imagesrc) {
						$('#ImageZoomModal').modal('hide');
						$('#ImageZoomModal').remove()
						var $imageModal = QWeb.render('web_image_zoom_cr.ImageZoom');
						var imageclone = '<img src="' + imagesrc + '" style="width:100%;"></img>';
						$('body').append($imageModal);
						$('#ImageZoomModal').find('.image-body').append(imageclone)
						$('#ImageZoomModal').find('a.download_img').attr('href',imagesrc)
						$('#ImageZoomModal').modal('show');
					}
				});
				
				self.$el.find('.o_kanban_image_full').unbind('click').bind('click',function(ev){
					ev.preventDefault();
					ev.stopPropagation();
				
					var imagesrc = false;
					if($(this).css('background-image') && $(this).css('background-image').includes('url(')) {
						imagesrc = $(this).css('background-image').replace('url(','').replace(')','').replace(/\"/gi, "");
					}
					
					else if($(this).attr('src')) {
						imagesrc = $(this).attr('src')
					}
					
					else if($(this).find('img').length > 0) {
						imagesrc = $(this).find('img').attr('src')
					}
					
					
					if(imagesrc) {
						$('#ImageZoomModal').modal('hide');
						$('#ImageZoomModal').remove()
						var $imageModal = QWeb.render('web_image_zoom_cr.ImageZoom');
						var imageclone = '<img src="' + imagesrc + '" style="width:100%;"></img>';
						$(body).append($imageModal);
						$('#ImageZoomModal').find('.image-body').append(imageclone)
						$('#ImageZoomModal').find('a.download_img').attr('href',imagesrc)
						$('#ImageZoomModal').modal('show');
					}
				});
				
				
				self.$el.find('.o_kanban_image').unbind('click').bind('click',function(ev){
					ev.preventDefault();
					ev.stopPropagation();
				
					var imagesrc = false;
					if($(this).css('background-image') && $(this).css('background-image').includes('url(')) {
						imagesrc = $(this).css('background-image').replace('url(','').replace(')','').replace(/\"/gi, "");
					}
					
					else if($(this).attr('src')) {
						imagesrc = $(this).attr('src')
					}
					
					else if($(this).find('img').length > 0) {
						imagesrc = $(this).find('img').attr('src')
					}
					
					
					if(imagesrc) {
						$('#ImageZoomModal').modal('hide');
						$('#ImageZoomModal').remove()
						var $imageModal = QWeb.render('web_image_zoom_cr.ImageZoom');
						var imageclone = '<img src="' + imagesrc + '" style="width:100%;"></img>';
						$(body).append($imageModal);
						$('#ImageZoomModal').find('.image-body').append(imageclone)
						$('#ImageZoomModal').find('a.download_img').attr('href',imagesrc)
						$('#ImageZoomModal').modal('show');
					}
				});
			}
		},
		
		_renderView: function () {
			var self = this; 
			return Promise.all([this._super.apply(this, arguments)]).then(function () {
				self.imagehoverinterval = setInterval(function(){ 
					self._addImageHoverEvent();
				}, 100);
			});
		},
		
	})

	BasicFields.FieldBinaryImage.include({
		
		events: _.extend({}, BasicFields.FieldBinaryImage.prototype.events, {
			'click img': 'OnImageMouseOver',
	    }),
		
		_renderReadonly: function () {
	        this._super.apply(this, arguments);
		},
		
		OnImageMouseOver : function (){
			if(this.mode != 'edit') {
				$('#ImageZoomModal').modal('dispose');
				$('#ImageZoomModal').remove()
				
				var $imageModal = QWeb.render('web_image_zoom_cr.ImageZoom');
				var imageclone = this.$el.find('img').clone().css({'width':'100%'});
				$(body).append($imageModal);
				$('#ImageZoomModal').find('.image-body').append(imageclone)
				$('#ImageZoomModal').find('a.download_img').attr('href',imageclone.attr('src'))
				$('#ImageZoomModal').modal('show');
			}
		},
	});
	

});