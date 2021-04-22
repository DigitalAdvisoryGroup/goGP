odoo.define('goGP.racefields', function (require) {
    'use strict';


	$(document).ready(function(){
		
		$('img.vehicle_img').click(function(){
			$('#ImageZoomModal').modal('hide');
			$('#ImageZoomModal').remove()
			var $imageModal = '<div class="modal fade" id="ImageZoomModal" tabindex="-1" role="dialog" aria-labelledby="ImageZoomModal" aria-hidden="false">'+
							    '<div class="modal-dialog modal-dialog-centered" role="dialog">'+
							      '<div class="modal-content">'+
							        '<div class="modal-header">'+
							          '<a class="download_img btn fa fa-download" href="#" download="zoomimage"/>'+
							          '<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
							            '<span aria-hidden="false">×</span>'+
							          '</button>'+
							        '</div>'+
							        '<div class="modal-body image-body" style="padding:0;">'+
							        '</div>'+
							      '</div>'+
							    '</div>'+
						  	'</div>';
			var imageclone = '<img src="' + $(this).attr('src') + '" style="width:100%;"></img>';
			$('body').append($imageModal);
			$('#ImageZoomModal').find('.image-body').append(imageclone)
			$('#ImageZoomModal').find('a.download_img').attr('download',$(this).attr('title'));
			$('#ImageZoomModal').find('a.download_img').attr('href',$(this).attr('src'))
			$('#ImageZoomModal').modal('show');
		});
		
		$('img.racefield_image').click(function(){
			$('#ImageZoomModal').modal('hide');
			$('#ImageZoomModal').remove()
			var $imageModal = '<div class="modal fade" id="ImageZoomModal" tabindex="-1" role="dialog" aria-labelledby="ImageZoomModal" aria-hidden="false">'+
							    '<div class="modal-dialog modal-dialog-centered" role="dialog">'+
							      '<div class="modal-content">'+
							        '<div class="modal-header">'+
							          '<a class="download_img btn fa fa-download" href="#" download="zoomimage"/>'+
							          '<button type="button" class="close" data-dismiss="modal" aria-label="Close">'+
							            '<span aria-hidden="false">×</span>'+
							          '</button>'+
							        '</div>'+
							        '<div class="modal-body image-body" style="padding:0;">'+
							        '</div>'+
							      '</div>'+
							    '</div>'+
						  	'</div>';
			var imageclone = '<img src="' + $(this).attr('src') + '" style="width:100%;"></img>';
			$('body').append($imageModal);
			$('#ImageZoomModal').find('.image-body').append(imageclone)
			$('#ImageZoomModal').find('a.download_img').attr('download',$(this).attr('title'));
			$('#ImageZoomModal').find('a.download_img').attr('href',$(this).attr('src'))
			$('#ImageZoomModal').modal('show');
		});
		
	})

});