import datetime
import json
import uuid

CATEGORIES = ['Sales', 'IT', 'Accounts']
STATUSES = ['New', 'Closed', 'Hold', 'Working']

class Event(object):
    """An event

    Something that happens and can be categorized, status set and comments added
    """
    def __init__(self, message):
        self.uid = u"{0}".format(uuid.uuid1())
        self.message = message
        self.category = None
        self.status = 'New'
        self.comments = []

    def __repr__(self):
        return u"{0}".format(self.uid)

    def to_json(self):
        return json.dumps(self.__dict__)

    def set_id(self, event_id):
        self.uid = event_id

    def set_category(self, category):
        """Categorize event"""
        if category in CATEGORIES:
            self.category = category

    def set_status(self, status):
        """Set status of event"""
        if status in STATUSES:
            self.status = status

    def add_comment(self, comment):
        """Add comment to event"""
        date = datetime.datetime.now()
        self.comments.append((date.strftime("%m/%d/%Y"), comment))

    def update(self, data):
        if type(data) == dict:
            if data.get('category', False):
                self.set_category(data.get('category'))
            if data.get('status', False):
                self.set_status(data.get('status'))
            if data.get('comment', False):
                self.add_comment(data.get('comment'))

class EventHandler(object):
    """Wrapper for events"""

    def __init__(self):
        self.events = {}

    def add(self, data):
        """Add new event and inform users"""
        msg = json.loads(data).get('message')
        new_event = Event(msg)
        self.events[new_event.uid] = new_event
        return new_event

    def update(self, data):
        """Update specific event and inform users"""
        event_data = {}
        for field in data:
            event_data[field.get('name')] = field.get('value')
        event = self.events[event_data.get('event_id')]
        event.update(event_data)
        return event

    def delete(self, event_id):
        """Delete event and inform users"""
        del(self.events[event_id])

    def find(self, event_id):
        """Find event given event id"""
        return self.events[event_id]
