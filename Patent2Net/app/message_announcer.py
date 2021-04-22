import queue
import requests

class MessageAnnouncer:

    def __init__(self):
        self.listeners = []

    def listen(self):
        self.listeners.append(queue.Queue(maxsize=5))
        return self.listeners[-1]

    def announce(self, msg):
        # We go in reverse order because we might have to delete an element, which will shift the
        # indices backward
        for i in reversed(range(len(self.listeners))):
            try:
                self.listeners[i].put_nowait(msg)
            except queue.Full:
                del self.listeners[i]

def AnnonceProgres(Appli, valActu, valMax):
    if valActu and valMax:
        valActu = "%.2f" % valActu 
        try:
            requests.get('http://localhost:5000/announce?appli=%s&ValActu=%s&valMax=%s' %(Appli, valActu, valMax) )
        except:
            pass
    else:
        pass # must be a error

def AnnonceLog(Appli, texte):

    try:
        requests.get('http://localhost:5000/announce?appli=%s&log=%s' %(Appli+'Log', texte) )
    except:
        pass
