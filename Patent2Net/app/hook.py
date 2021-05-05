import requests
import queue
import json

class HookListener:

    def __init__(self):
        self.listeners = []

    def listen(self):
        self.listeners.append(queue.Queue(maxsize=5))
        return self.listeners[-1]

    def send_hook(self, hook):
        # We go in reverse order because we might have to delete an element, which will shift the
        # indices backward
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(hook)
            except queue.Full:
                del self.listeners[i]

def send_hook(hook):
    serialized = hook.serialize()
    header = {"content-type": "application/json"}
    requests.post("http://localhost:5000/api/v1/hook", data=json.dumps(serialized), headers=header, verify=False )