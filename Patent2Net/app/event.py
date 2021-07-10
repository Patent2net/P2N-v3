import json
import queue

import requests


class EventListener:

    def __init__(self):
        self.listeners = []

    def listen(self):
        self.listeners.append(queue.Queue(maxsize=5))
        return self.listeners[-1]

    def push_event(self, event):
        # We go in reverse order because we might have to delete an element, which will shift the
        # indices backward
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(event)
            except queue.Full:
                del self.listeners[i]

def send_new_event(event):
    """
    Allows to send an event to the web server.
    The list of events is in the events directory

    Each event object must have the serialize and deserialize methods to be able to use the model before sending and after sending on the web side
    
    Be careful, the objective of sending an event is not to make a mutation on the state of the application.
    It simply allows to inform the interface part of the current executions. 
    """
    serialized = event.serialize()
    header = {"content-type": "application/json"}
    requests.post("http://localhost:5000/api/v1/events", data=json.dumps(serialized), headers=header, verify=False )