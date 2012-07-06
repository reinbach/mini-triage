$(function() {
    // Open up a connection to our server
    var socket = io.connect();

    // Save our event placeholder
    var $placeholder = $('#placeholder');

    // Handle a new message/event?
    socket.on('event_add', function(data) {
        $placeholder.append(data);
    });

    // Handle updating of event
    function getLabel(collapse) {
	var label_name = $(collapse).attr("id").replace("collapse", "label");
	return $("#" + label_name);
    }
    $(".collapse").on("hidden", function() {
	// change the text and remove class
	$label = getLabel(this);
	$label.text("Edit");
	$label.removeClass("label-important");
    });
    $(".collapse").on("shown", function() {
	// change text and add class
	$label = getLabel(this);
	$label.text("Cancel");
	$label.addClass("label-important");
    });
    $(".event-form").live("submit", function(e) {
	// prevent form being submitted
	e.preventDefault();
	var category = $("select[name=category]", this).val();
	var event_id = $("input[name=event_id]", this).val();
	var comment_field = $("textarea[name=comment]", this);
	var comment = comment_field.val();
	var event = $("#" + event_id);
	// close form
	$("#" + event_id + " .collapse").collapse("hide");
	// move event to relevant category
	$("#" + category).append(event);
	// append comments to event, only if there are any
	if (comment != "") {
	    var current_time = new Date()
	    var month = current_time.getMonth() + 1;
	    var day = current_time.getDate();
	    var year = current_time.getFullYear();
	    $(".comments", event).append(
		"<blockquote>" + comment + "<small>" + month + "/" + day + "/" + year + "</small></blockquote>"
	    );
	}
	// send data via socket.io
	socket.emit("update", $(this).serializeArray());
	// need to clear comments from form
	comment_field.val("");
    });
    socket.on('event_update', function(data) {
	var d = $.parseJSON(data);
	$("#" + d.uid).remove();
	$("#" + d.category).append(d.event);
    });

    // Handle deleting of event
    $(".event").alert();
    $(".event").live("closed", function() {
	// let server know that event has been deleted
	socket.emit("delete", {'event_id': $(this).attr("id")});
    });
    socket.on('event_delete', function(data) {
	var d = $.parseJSON(data);
	$("#" + d.uid).remove();
    });

    // Just update our conn_status field with the connection status
    socket.on('connect', function() {
        $('#conn_status').html('<b>Connected</b>');
	$('#conn_status').attr("class", "label label-success")
	// this is the call that streams the events being added
	socket.emit('stream', '');
    });
    socket.on('error', function() {
        $('#conn_status').html('<b>Error</b>');
	$('#conn_status').attr("class", "label label-important")
    });
    socket.on('disconnect', function() {
        $('#conn_status').html('<b>Closed</b>');
	$('#conn_status').attr("class", "label label-warning")
    });
});
