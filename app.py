import os

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
    SocketIOServer(
        ('', 8000), http_app,
        namespace='socket.io',
        policy_server=False
    ).serve_forever()

if __name__ == "__main__":
    main()