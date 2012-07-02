import gevent
import zmq

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

class EventIOApp(object):
    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/socket.io'):
            gevent.spawn(socketio_manage(environ, {'': EventStream}))

class EventStream(BaseNamespace, BroadcastMixin):
    """Stream events"""
    def on_stream(self, msg):
        context = zmq.Context()
        sock = context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect("tcp://127.0.0.1:5000")
        print "Connected, ready to stream events..."
        while True:
            msg = sock.recv()
            # For now just streaming events straight to user
            # need to connect to eventhandler instead
            self.broadcast_event('event', msg)
            gevent.sleep(0.1)