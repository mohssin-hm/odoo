odoo.define('ehcs_evo_tech.theme', function(require) {
	"use strict";


	console.log("WEBSITE")
	/*Scroll to top when arrow up clicked BEGIN*/
	$(window).scroll(function() {
		var height = $(window).scrollTop();
		if (height > 120) {
			$('#back2Top').fadeIn();
		} else {
			$('#back2Top').fadeOut();
		}
	});
	$(document).ready(function() {
		$("#back2Top").click(function(event) {
			event.preventDefault();
			$("html, body").animate({ scrollTop: 0 }, "slow");
			return false;
		});

	});
	
	
	

});
