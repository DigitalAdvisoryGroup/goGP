odoo.define('goGP.racefields', function (require) {
    'use strict';

    var ajax = require('web.ajax');

	$(document).ready(function(){
		
		var records_per_page = 6;
		
		var myarr = [];
		
		
		// on page load collect data to load pagination as well as table
        const data = { "req_per_page": 6, "page_no": 1 };

        // At a time maximum allowed pages to be shown in pagination div
        const pagination_visible_pages = 4;


        // hide pages from pagination from beginning if more than pagination_visible_pages
        function hide_from_beginning(element) {
        	
        	if (element.style.display === "" || element.style.display === "block" && element.id != 'next_link') {
        		console.log("If Big===",element)
        		element.style.display = "none";
            } else {
            	console.log("Else Big===",element)
                hide_from_beginning(element.nextSibling);
            }
        }
        
        // hide pages from pagination ending if more than pagination_visible_pages
        function hide_from_end(element) {
        	console.log("Element--",element)
        	if (element.style.display === "" || element.style.display === "block") {
        		console.log("If===")
                element.style.display = "none";
            } else {
            	console.log("Else===")
                hide_from_end(element.previousSibling);
            }
        }
        
        // load data and style for active page
        function active_page(element, rows, req_per_page) {
            var current_page = document.getElementsByClassName('vehicle-active');
            var next_link = document.getElementById('next_link');
            var prev_link = document.getElementById('prev_link');
            var next_tab = current_page[0].nextSibling; 
            var prev_tab = current_page[0].previousSibling;
            current_page[0].className = current_page[0].className.replace("vehicle-active", "");
            
            console.log("CUrrent page---",current_page,element)
            if (element === "next") {
                if (parseInt(next_tab.text).toString() === 'NaN') {
                    next_tab.previousSibling.className += " vehicle-active";
                    next_tab.setAttribute("onclick", "return false");
                } else {
                    next_tab.className += " vehicle-active"
                    render_table_rows(rows, parseInt(req_per_page), parseInt(next_tab.text));
                    if (prev_link.getAttribute("onclick") === "return false") {
                    	$(prev_link).unbind('click').bind('click',function(es){
                    		es.preventDefault()
                    		es.stopPropagation();
                    		active_page("prev",rows,req_per_page)
                    	})
                    }
                    if (next_tab.style.display === "none") {
                        next_tab.style.display = "block";
                        hide_from_beginning(prev_link.nextSibling)
                    }
                }
            } else if (element === "prev") {
                if (parseInt(prev_tab.text).toString() === 'NaN') {
                    prev_tab.nextSibling.className += " vehicle-active";
                    prev_tab.setAttribute("onclick", "return false");
                } else {
                    prev_tab.className += " vehicle-active";
                    render_table_rows(rows, parseInt(req_per_page), parseInt(prev_tab.text));
                    if (next_link.getAttribute("onclick") === "return false") {
                    	$(next_link).unbind('click').bind('click',function(es){
                    		es.preventDefault()
                    		es.stopPropagation();
                    		active_page("next",rows,req_per_page)
                    	})
                    }
                    if (prev_tab.style.display === "none") {
                        prev_tab.style.display = "block";
                        console.log("Hide From End Callled---")
                        hide_from_end(next_link.previousSibling)
                    }
                }
            } else {
                element.className += " vehicle-active";
                render_table_rows(rows, parseInt(req_per_page), parseInt(element.text));
                if (prev_link.getAttribute("onclick") === "return false") {
                	
                	$(prev_link).unbind('click').bind('click',function(es){
                		es.preventDefault()
                		es.stopPropagation();
                		active_page("prev",rows,req_per_page)
                	})
                }
                if (next_link.getAttribute("onclick") === "return false") {
                	
                	$(next_link).unbind('click').bind('click',function(es){
                		es.preventDefault()
                		es.stopPropagation();
                		active_page("next",rows,req_per_page)
                	})
                }
            }
        }

        // Render the table's row in table request-table
        function render_table_rows(rows, req_per_page, page_no) {
            const response = JSON.parse(window.atob(rows));
            const resp = response.slice(req_per_page * (page_no - 1), req_per_page * page_no)
            $('#listingTable').empty()
//            $('#request-table').append('<tr><th>Index</th><th>Request No</th><th>Title</th></tr>');
            resp.forEach(function (element, index) {
                if (Object.keys(element).length > 0) {                    
                    var vehicle_image = '/web/static/src/img/placeholder.png';
    		    	
		        	if(element.image) {
		        		vehicle_image = 'data:image/png;base64,' + element.image
		        	}
		        	
		        	var vehicle_name = element.brand + ' ' + element.model
		        	
		        	var vehicle_card = '<div class="card col-sm-3 col-md-3 col-lg-3 col-4" style="width: 18rem;padding:0;margin-bottom:1%;height:50%;">'+
							'<div class="vehicle_card">'+
								'<h6 class="card-title vehicle_name" title="' + vehicle_name + '">' + vehicle_name + '</h6>'+
								'<span class="card-text">' + element.model_year + ' | ' + element.cm + 'ccm' + '</span><br/>' +
								'<span class="card-text">' + element.cylinders + ' Zylinder' + ' | ' + element.horsepower + 'PS' + '</span><br/>' +
								'<span class="card-text">' + element.pitid + ' Box Id' + ' | ' + element.startnumber + ' Start Number' + '</span><br/>' +
							'</div>'+
							'<img src="' + vehicle_image  + '"class="card-img-top" alt="..." style="width:100%;height:150px;">'+
						'</div>';
		        	$('#listingTable').append(vehicle_card);
                }
            });
        }

        // Pagination logic implementation
        function pagination(data, myarr) {
            const all_data = window.btoa(JSON.stringify(myarr));
            $(".vehicle-pagination").empty();
            if (data.req_per_page !== 'ALL') {
                let pager = '<a href="#" id="prev_link">&laquo;</a>' +
                    '<a class="normal_page vehicle-active" href="#">1</a>';
                const total_page = Math.ceil(parseInt(myarr.length) / parseInt(data.req_per_page));
                if (total_page < pagination_visible_pages) {
                    render_table_rows(all_data, data.req_per_page, data.page_no);
                    for (let num = 2; num <= total_page; num++) {
                        pager += '<a class="normal_page" href="#">' + num + '</a>';
                    }
                } else {
                    render_table_rows(all_data, data.req_per_page, data.page_no);
                    for (let num = 2; num <= pagination_visible_pages; num++) {
                        pager += '<a class="normal_page" href="#">' + num + '</a>';
                    }
                    for (let num = pagination_visible_pages + 1; num <= total_page; num++) {
                        pager += '<a style="display:none;" class="normal_page" href="#">' + num + '</a>';
                    }
                }
                pager += '<a href="#" id="next_link">&raquo;</a>';
                
                
                
        		$(".vehicle-pagination").append(pager);
        		
        		$(".vehicle-pagination").find('a#prev_link').unbind('click').bind('click',function(ev){
                	ev.preventDefault();
                	ev.stopPropagation();
                	active_page("prev",all_data,data.req_per_page)
                })
        		
                $(".vehicle-pagination").find('a#next_link').unbind('click').bind('click',function(ev){
                	ev.preventDefault();
                	ev.stopPropagation();
                	active_page("next",all_data,data.req_per_page)
                })
                
                $(".vehicle-pagination").find('a.normal_page').unbind('click').bind('click',function(ev){
                	ev.preventDefault();
                	ev.stopPropagation();
                	active_page(this,all_data,data.req_per_page)
                })
            } else {
                render_table_rows(all_data, myarr.length, 1);
            }
        }

        


        // trigger when requests per page dropdown changes
        function filter_requests() {
            const data = { "req_per_page": document.getElementById("req_per_page").value, "page_no": 1 };
            pagination(data, myarr);
        }


		
		$('.racefield_li').click(function(ev){
			console.log("RaceField-----",$(ev.currentTarget).data('race-id'))
			ajax.jsonRpc('/get_racefields/data', 'call', {'raceid' : $(ev.currentTarget).data('race-id')}).then(function(result){
	        	console.log("Data=---",result)
	        	if(result) {
	        		$('.racefield_li').removeClass('active')
	        		$(ev.currentTarget).addClass('active');
	        		
	        		$('.racefield_content').removeClass('d-none');
	        		$('.racefield_name').text(result['name']);
	        		
	        		if(result['image']) {
	        			var imagesrc = 'data:image/png;base64,' + result['image']
    					$('.racefield_image').attr('src',imagesrc)
	        		}
	        		else {
	        			$('.racefield_image').attr('src','/web/static/src/img/placeholder.png')
	        		}
	        		
	        		if(result['vehicle_list'].length > 0) {
	        			myarr = result['vehicle_list'];
	        			data.page_no = 1;
	        	        pagination(data, myarr);
	        		}
	        		else {
	        			myarr = [];
	        			data.page_no = 1;
	        			pagination(data, myarr);
	        		}
	        		
	        	}
	        });
		});
		
		if($('ul.racefields_ul').length > 0) {
			$('ul.racefields_ul').find('li')[0].click()
		}
	})

});