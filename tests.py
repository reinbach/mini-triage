import unittest

import models

class EventTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testEventAdd(self):
        message = "Hello World!"
        event = models.Event(message)
        assert event.message == message
        assert event.status == 'New'
        assert event.category is None
        assert event.comments == []

    def testEventUpdate(self):
        message = "Hello World!"
        event = models.Event(message)
        data = dict(
            category='IT',
            status='Hold',
            comment='Testing'
        )
        event.update(data)
        assert event.message == message
        assert event.category == data.get('category')
        assert event.status == data.get('status')
        assert len(event.comments) == 1

class EventHandlerTest(unittest.TestCase):

    def testEventHandlerAdd(self):
        message = "Hello World!"
        event_handler = models.EventHandler()
        event_handler.add(message)
        assert len(event_handler.events) == 1

if __name__ == "__main__":
    unittest.main()