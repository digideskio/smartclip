(function() {
    $(document).on({
	mouseenter: function() {
	    $(this).find(".options").show();
	},
	mouseleave: function() {	
	    $(this).find(".options").hide();    
	}
    }, '.clip-listing');

    $(document).on("click", "a[id^='show']", function(e) {
	    e.preventDefault();
	    var id = $(this).attr('id').split("-")[1];
	    $('#clip-frame').attr("src", "/htmlview/?clip_id="+id);
    });

    $(document).on("click", "a[id^='delete']", function(e) {
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

    $(document).on("click", "a[id^='edit']", function(e) {
	e.preventDefault();
	var id = $(this).attr('id').split("-")[1];
	var parent = $(this).parents('.clip-listing');
	$.ajax({
	    url: "/formview/",
	    data: {"clip_id": id},
	    success: function(data) {
		parent.children('td').hide();
		parent.append(data);
	    }
	});
    });

    $(document).on("click", "a[id^='cancel']", function(e) {
	e.preventDefault();
	var form = $(this).parents('td');
	form.sibling('td').show();
	form.remove();
    });

    // $(document).on("click", "a[id^='save']", function(e) {
    // });

}).call(this);