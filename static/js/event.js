$(function() {
    // Open up a connection to our server
    var socket = io.connect("", {'host': 'localhost', 'port': 9999});

    // Save our event placeholder
    var $placeholder = $('#placeholder');

    // What do we do when we get a message/event?
    socket.on('event', function(msg) {
        var d = $.parseJSON(msg);
        $placeholder.append("<div>" + d.message + "</div>");
    });

    // Just update our conn_status field with the connection status
    socket.on('connect', function() {
        $('#conn_status').html('<b>Connected</b>');
	// this is the call that streams the sine wave data
	socket.emit('stream', '');
    });
    socket.on('error', function() {
        $('#conn_status').html('<b>Error</b>');
    });
    socket.on('disconnect', function() {
        $('#conn_status').html('<b>Closed</b>');
    });
});
