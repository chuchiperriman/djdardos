$(document).ready(function() {
    $(".tweet").hover(
        function (){
            $(this).addClass("tweet-light")
        },
        function (){
            $(this).removeClass("tweet-light")
        }
    );
    
    $("#tweet-text-box").bind('keydown keypress keyup click blur focus change paste', function() {
	    el = $(this);
	    var maxc = 140;
		if (el.val().length > maxc) {
		    el.val(el.val().substring(0, maxc));
		};
		$("#charCount").html((maxc - el.val().length));
    });
});
