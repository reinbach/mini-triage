import os
import uuid

from flask import Flask, render_template, redirect, url_for, request
from gevent import monkey
from socketio import socketio_manage
from socketio.server import SocketIOServer
from werkzeug.wsgi import SharedDataMiddleware

import eventio
from models import EventHandler, User

monkey.patch_all()

app = Flask(__name__)
app.debug = True

users = {}
event_handler = EventHandler()

@app.route("/")
def home():
    """Set uuid for user and redirect to triage page"""
    uid = uuid.uuid1()
    user = users[u"{0}".format(uid)] = User()
    event_handler.subscribe(user)
    return redirect("/{0}/".format(uid))

@app.route("/<uid>/")
def triage(uid):
    # Make sure user has uuid, otherwise redirect to home
    if not users.get(uid, False):
        return redirect(url_for("home"))
    return render_template("index.html", events=event_handler.events, uid=uid)

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