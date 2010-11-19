function cargar_calendarios(){
    $(".datepicker").datepicker({
    	    showAnim: "slideDown",
    	    showOn: "both",
    	    dateFormat: "dd/mm/yy",
			buttonImage: "/site_media/images/calendar.png",
			buttonImageOnly: true
    	});
}

$(document).ready(function() {
    cargar_calendarios();
});
