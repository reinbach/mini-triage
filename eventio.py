import gevent
import json
import zmq

from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

class EventIOApp(object):

    def __init__(self, event_handler):
        self.event_handler = event_handler

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/socket.io'):
            gevent.spawn(socketio_manage(environ, {'': EventStream}, request=self.event_handler))

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
            event = self.request.add(msg)
            self.broadcast_event('event_add', json.dumps(event.__dict__))
            gevent.sleep(0.1)

    def on_update(self, data):
        event = self.request.update(data.get('event_id'), data)
        self.broadcast_event('event_update', json.dumps(event.__dict__))