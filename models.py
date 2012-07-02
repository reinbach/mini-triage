import datetime
import json
import uuid

from gevent import queue

class Event(object):
    """An event

    Something that happens and can be categorized, status set and comments added
    """

    CATEGORIES = ['Sales', 'IT', 'Customer Service']
    STATUSES = ['New', 'Closed', 'Hold', 'Working']

    def __init__(self, message):
        self.uid = uuid.uuid1()
        self.message = message
        self.category = None
        self.status = 'New'
        self.comments = []

    def set_id(self, event_id):
        self.uid = event_id

    def set_category(self, category):
        """Categorize event"""
        if category in self.CATEGORIES:
            self.category = category

    def set_status(self, status):
        """Set status of event"""
        if status in self.STATUSES:
            self.status = status

    def add_comment(self, comment):
        """Add comment to event"""
        self.comments.append((datetime.datetime.now(), comment))

    def update(self, data):
        if type(data) == dict:
            if data.get('category', False):
                self.set_category(data.get('category'))
            if data.get('status', False):
                self.set_status(data.get('status'))
            if data.get('comment', False):
                self.add_comment(data.get('comment'))

class User(object):
    """Users of the app"""
    def __init__(self):
        self.queue = queue.Queue()

class EventHandler(object):
    """Wrapper for events"""

    def __init__(self):
        self.users = set()
        self.events = {}

    def add(self, data):
        """Add new event and inform users"""
        new_event = Event(data)
        self.events[new_event.uid] = new_event
        for user in self.users:
            user.queue.put_nowait(json.dumps(new_event))

    def update(self, event_id, data):
        """Update specific event and inform users"""
        self.events[event_id].update(data)

    def subscribe(self, user):
        """User subscribes to a category"""
        self.users.add(user)

