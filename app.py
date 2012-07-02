import gevent
import uuid

from flask import Flask, render_template, redirect, url_for
from gevent.pywsgi import WSGIServer

from models import EventHandler, User

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
    return render_template("index.html", data=event_handler, uid=uid)

def main():
    # Setup server to handle webserver requests
    http_server = WSGIServer(('', 8000), app)

    gevent.joinall([
        gevent.spawn(http_server.serve_forever)
    ])

if __name__ == "__main__":
    main()