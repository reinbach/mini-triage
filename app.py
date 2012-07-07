import gevent
import os
import zmq

from flask import Flask, render_template, request
from gevent import monkey
from socketio import socketio_manage
from socketio.server import SocketIOServer
from werkzeug.wsgi import SharedDataMiddleware

import eventio
from models import EventHandler, CATEGORIES, STATUSES

monkey.patch_all()

app = Flask(__name__)
app.debug = True

event_handler = EventHandler()

def event_subscriber(event_handler):
    """Handle the events being produced

    Create the events and add them to the event handler
    and send the events to any connected users
    """
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    sock.setsockopt(zmq.SUBSCRIBE, "")
    sock.connect("tcp://127.0.0.1:5000")

    stream = context.socket(zmq.PUB)
    stream.bind("tcp://127.0.0.1:5001")

    poller = zmq.Poller()
    poller.register(sock, zmq.POLLIN)

    while True:
        events = dict(poller.poll(1))

        if events:
            msg = sock.recv()
            event = event_handler.add(msg)
            stream.send_unicode(event.uid)
        gevent.sleep(0.1)


@app.route("/")
def home():
    return render_template(
        "index.html",
        events=event_handler.events,
        categories=CATEGORIES,
        statuses=STATUSES
    )

@app.route('/socket.io/<path:path>')
def socketio_server(path):
    socketio_manage(
        request.environ,
        {'': eventio.EventIOApp},
        request=event_handler
    )
    return {}

def main():
    http_app = SharedDataMiddleware(app, {
        '/': os.path.join(os.path.dirname(__file__), 'static')
    })
    socket_server = SocketIOServer(
        ('', 8000), http_app,
        namespace='socket.io',
        policy_server=False
    )

    gevent.joinall([
        gevent.spawn(socket_server.serve_forever),
        gevent.spawn(event_subscriber, event_handler),
    ])

if __name__ == "__main__":
    main()