mini-triage
===========

A prototype app that allows user(s) to triage events into various categories.

Overview
--------

The idea is that as events are happening, user(s) can triage these events into user defined categories. Users can signup for these categories and as soon as the event is assigned to the category the user can start working on the event.

Updates etc on the events are automatically dispersed to the user(s) currently on the system.


Flow
----

1. User registers.
2.a. User Triages. User categorizes incoming events.
2.b. User signs up for specific categories.
 -- Able to view events assigned to these categories.
 -- "Work" the events. In this app, "working" means user can change status and/or add comments to the event.
3. Manage categories.


To Install and Run
------------------

    python setup.py install
    python producer.py
    python app.py

Then point a browser at http://localhost:8000
