import gevent
import json
import zmq

from jinja2 import Environment, PackageLoader
from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

from models import CATEGORIES, STATUSES

class EventIOApp(BaseNamespace, BroadcastMixin):

    def __init__(self, *args, **kwargs):
        super(EventIOApp, self).__init__(*args, **kwargs)
        self.env = Environment(loader=PackageLoader('app', 'templates'))

    def render_event(self, event):
        template = self.env.get_template("event.html")
        return template.render(
            event=event,
            categories=CATEGORIES,
            statuses=STATUSES
        )

    def subscribe(self):
        context = zmq.Context()
        sock = context.socket(zmq.SUB)
        sock.setsockopt(zmq.SUBSCRIBE, "")
        sock.connect("tcp://127.0.0.1:5000")

        while True:
            msg = sock.recv()
            event = self.request.add(msg)
            self.broadcast_event('event_add', self.render_event(event))
            gevent.sleep(0.1)

    def on_stream(self, msg):
        self.spawn(self.subscribe)

    def on_update(self, data):
        event = self.request.update(data.get('event_id'), data)
        self.broadcast_event_not_me('event_update', event.to_json())

    def on_delete(self, data):
        event_id = data.get('event_id')
        self.request.delete(event_id)
        self.broadcast_event_not_me('event_delete', json.dumps({'uid': event_id}))