(function() {
    $(document).ready(function() {
	$(".clip-listing").hover(
	    function() {
		$(this).find(".options").show();
	    },
	    function() {	
		$(this).find(".options").hide();    
	    }
	);

	$("a[id^='show']").click(function(e) {
	    e.preventDefault();
	    var id = $(this).attr('id').split("-")[1];
	    $('#clip-frame').attr("src", "/htmlview/?clip_id="+id);
	});

	$("a[id^='delete']").click(function(e) {
	    e.preventDefault();
	    var id = $(this).attr('id').split("-")[1];
	    var parent = $(this).parents('.clip-listing');
	    $.ajax({
		url: "/api/v1/clipping/"+id,
		type: "DELETE",
		complete: function(xhr, errrorText) {
		    if (xhr.status==204) {
			$('.statuses').html('Deleted!');
			parent.fadeOut("normal", function() {
			    $(this).remove();
			});
		    }
		}
	    });
	});

    });


}).call(this);