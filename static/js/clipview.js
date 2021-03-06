(function() {
    $(document).ready(function() {
	$("#sortby-newest").click(function(e) {
	    e.preventDefault();
	    $(".dropdown-toggle").html('Sorting...<span class="caret"></span>');
	    $.ajax({
		url: "/sort_clips",
		data: {"sort_key" : "-date_modified"},
		success: function(data) {
		    $(".clip_list ul").html(data);
		    $(".dropdown-toggle").html('Sort By <span class="caret"></span>');
		}
	    });
	});

	$("#sortby-oldest").click(function(e) {
	    e.preventDefault();	
	    $(".dropdown-toggle").html('Sorting...<span class="caret"></span>');
	    $.ajax({
		url: "/sort_clips",
		data: {"sort_key" : "date_modified"},
		success: function(data) {
		    $(".clip_list ul").html(data);	
		    $(".dropdown-toggle").html('Sort By <span class="caret"></span>');
		}
	    });
	});

	$("#sortby-title").click(function(e) {
	    e.preventDefault();
	    $(".dropdown-toggle").html('Sorting...<span class="caret"></span>');
	    $.ajax({
		url: "/sort_clips",
		data: {"sort_key" : "title"},
		success: function(data) {
		    $(".clip_list ul").html(data);	
		    $(".dropdown-toggle").html('Sort By <span class="caret"></span>');
		}
	    });
	});
    });

    $(document).on("click", "li[class^='clip_li']", function(e) {
    	e.preventDefault();
    	var id = $(this).find('a[id^="show"]').attr('id').split("-")[1];
    	$(this).attr("class", "clip_li active");
    	$(this).siblings().removeClass("active");
    	$('#clip_preview_frame').attr("src", "/htmlview/?clip_id="+id);
    });

    $(document).on("click", "a[id^='show']", function(e) {
	e.preventDefault();
	var id = $(this).attr('id').split("-")[1];
	$(this).parents('li').attr("class", "clip_li active");
	$(this).parents('li').siblings().removeClass("active");
	$('#clip_preview_frame').attr("src", "/htmlview/?clip_id="+id);
    });

    $(document).on("click", "a[id^='delete']", function(e) {
	e.preventDefault();
	var id = $(this).attr('id').split("-")[1];
	var parent = $(this).parents('li');
	$.ajax({
	    url: "/ext/delete/"+id,
	    success: function(data) {
		if (data=='deleted') {
		    $('.statuses').show();
		    $('.statuses').append('<div class="alert alert-error">Deleted!</div>').fadeOut(2500,
												   function(){
												       $('.alert').remove();
												   });
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
	parent.attr("class", "clip_li active");
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

    $(document).on("click", "a[id^='share']", function(e) {
    	e.preventDefault();
    	var id = $(this).attr('id').split("-")[1];
    	var parent = $(this).parents('li');
    	parent.attr("class", "clip_li active");
    	parent.siblings().removeClass("active");
    	$('#clip_preview_frame').attr("src", "/htmlview/?clip_id="+id);
    	$.ajax({
    	    url: "/share/"+id,
    	    success: function(data) {
    		$('.modal-body').html(data);
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
		if (data.indexOf('<li') != -1) {
		    $('.statuses').show();
		    $('.statuses').append('<div class="alert alert-success">Saved Successully!</div>').fadeOut(2500,
													       function(){
														   $('.alert').remove();
													       });
		    form.siblings().remove();
		    form.replaceWith(data);
		} else {
		    form.replaceWith(data);
		}
	    }
	});
    });

    $(document).on("click", "button[id^='sharesave']", function(e) {
	e.preventDefault();
	var id = $(this).attr('id').split("-")[1];
	var form = $(this).parents('form');
	$.ajax({
	    url: "/share/"+id,
	    type: "POST",
	    data: form.serialize(),
	    success: function(data) {
		if (data == 'success') {
		    form.remove();
		    $('#myModal').modal('hide');
		    $('.statuses').show();
		    $('.statuses').append('<div class="alert alert-success">Email Sent!</div>').fadeOut(2500,
													       function(){
														   $('.alert').remove();
													       });
		} else {
		    form.replaceWith(data);
		}
	    }
	});
    });

    $(document).on("click", "a[id^='download']", function(e) {
	var clip_id = $(this).attr('id').split('-')[1];
	window.open('/pdfview/?clip_id='+clip_id);
    });

}).call(this);