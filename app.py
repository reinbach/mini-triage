import gevent

from flask import Flask, render_template
from gevent.pywsgi import WSGIServer

app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template("index.html")

def main():
    # Setup server to handle webserver requests
    http_server = WSGIServer(('', 8000), app)

    gevent.joinall([
        gevent.spawn(http_server.serve_forever)
    ])

if __name__ == "__main__":
    main()