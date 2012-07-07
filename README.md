Mini-Triage
===========

A prototype app that allows user(s) to triage events into various categories.

gevent, gevent-socketio, zeromq and flask are used to stitch this together.

Overview
--------

The idea is that as events are happening, user(s) can triage these events into defined categories. All users see these categories and are able to update the events. The event updates are broadcasted to the other users. A new user arriving will get the same state as everyone else and will be able to start updating events.

Updates etc on the events are automatically dispersed to the user(s) currently on the system.

To Install and Run
------------------

    python setup.py install
    python producer.py
    python app.py

Then point multiple browsers at http://localhost:8000
