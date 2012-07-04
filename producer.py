import json
import random
import time
import zmq

def event_producer():
    """Produce events in a random fashion"""
    print "Event producer is running, generating events..."
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://127.0.0.1:5000")

    EVENT_MESSAGES = [
        "Hello World!",
        "Call me",
        "Server is down",
        "Need those reports in triplicate",
    ]

    while True:
        # randomly select event message
        random_event_message = random.sample(EVENT_MESSAGES, 1)[0]
        random_time_delay = random.randint(5, 10)
        socket.send(json.dumps(dict(message=random_event_message)))
        print "Sent message: {0}".format(random_event_message)
        time.sleep(random_time_delay)

if __name__ == "__main__":
    event_producer()