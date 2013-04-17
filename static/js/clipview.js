(function() {

    $(document).on("click", "a[id^='show']", function(e) {
	e.preventDefault();
	var id = $(this).attr('id').split("-")[1];
	$(this).parents('li').attr("class", "active");
	$(this).parents('li').siblings().removeClass("active");
	$('#clip_preview_frame').attr("src", "/htmlview/?clip_id="+id);
    });

    $(document).on("click", "a[id^='delete']", function(e) {
	e.preventDefault();
	var id = $(this).attr('id').split("-")[1];
	var parent = $(this).parents('li');
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
	var parent = $(this).parents('li');
	parent.attr("class", "active");
	parent.siblings().removeClass("active");
	$('#clip_preview_frame').attr("src", "/htmlview/?clip_id="+id);
	$.ajax({
	    url: "/formview/"+id,
	    success: function(data) {
		parent.children().hide();
		parent.append(data);
	    }
	});
    });

    $(document).on("click", "button[id^='cancel']", function(e) {
	e.preventDefault();
	var form = $(this).parents('form');
	var clip_list = $(this).parents('li');
	clip_list.children().show();
	form.remove();
    });

    $(document).on("click", "button[id^='save']", function(e) {
	e.preventDefault();
	var id = $(this).attr('id').split("-")[1];
	var form = $(this).parents('form');
	$.ajax({
	    url: "/formview/"+id,
	    type: "POST",
	    data: form.serialize(),
	    success: function(data) {
		if (data == 'Successful Save') {
		    form.siblings().show();
		    form.remove();
		    $('.statuses').html('<div class="alert alert-success">Saved!</div>').fadeOut(2000,
											      function(){
												  $(this).remove();
											      });
		} else {
		    form.replaceWith(data);
		}
	    }
	});
    });

}).call(this);