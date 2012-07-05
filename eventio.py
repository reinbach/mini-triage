import gevent
import json
import zmq

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

class EventIOApp(BaseNamespace, BroadcastMixin):
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
        self.broadcast_event_not_me('event_update', json.dumps(event.__dict__))

    def on_delete(self, data):
        event_id = data.get('event_id')
        self.request.delete(event_id)
        self.broadcast_event('event_delete', json.dumps({'uid': event_id}))