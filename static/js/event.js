$(function() {
    // Open up a connection to our server
    var socket = io.connect();

    // Save our event placeholder
    var $placeholder = $('#placeholder');

    // Handle a new message/event?
    socket.on('event_add', function(data) {
        var d = $.parseJSON(data);
        $placeholder.append(
	    "<div id='" + d.uid +
		"' class='event well'><button class='close' data-dismiss='alert'>&times;</button>" + d.message +
		"</div>"
	);
    });

    // Handle updating of event
    socket.on('event_update', function(data) {
	var d = $.parseJSON(data);
	// update event information
	// move to relevant category/placeholder
    });

    // Handle deleting of event
    $(".event").alert();
    $(".event").live("closed", function() {
	// let server know that event has been deleted
	socket.emit("delete", {'event_id': $(this).attr("id")});
    });
    socket.on('event_delete', function(data) {
	var d = $.parseJSON(data);
	$("#" + d.uid).hide();
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
