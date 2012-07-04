$(function() {
    // Open up a connection to our server
    var socket = io.connect("", {'host': 'localhost', 'port': 9999});

    // Save our event placeholder
    var $placeholder = $('#placeholder');

    // Handle a new message/event?
    socket.on('event_add', function(msg) {
        var d = $.parseJSON(msg);
        $placeholder.append("<div id='" + d.uid + "' class='well'>" + d.message + "</div>");
    });

    // Handle updating of event
    socket.on('event_update', function(msg) {
	var d = $.parseJSON(msg);
	// update event information
	// move to relevant category/placeholder
    });

    // Just update our conn_status field with the connection status
    socket.on('connect', function() {
        $('#conn_status').html('<b>Connected</b>');
	$('#conn_status').attr("class", "label label-success")
	// this is the call that streams the sine wave data
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
