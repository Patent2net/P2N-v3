from Patent2Net.app.dex import set_directory_request_data, get_directory_request_data, delete_directory_request_data
from Patent2Net.app.events.dex_change_event import DexChangeEvent
from Patent2Net.app.event import send_new_event

class FusionList:
    """represents the merged state of the data"""
    
    KEY = "fusion_list"

    def __init__(self, directory):
        self.directory = directory

    def get(self):
        self.prevData = get_directory_request_data(self.directory, self.KEY, {})
        return self.prevData.copy()
    
    def save(self, process_list):
        set_directory_request_data(self.directory, self.KEY, process_list)
        send_new_event( DexChangeEvent(self.directory, self.KEY, self.prevData, process_list) )

    def reset(self):
        delete_directory_request_data(self.directory, self.KEY)

    def start(self, queue_list, done_list):
        process_list = self.get()

        process_list["start"] = True
        process_list["queue_list"] = queue_list
        process_list["done_list"] = done_list

        print("TESTTEST ")

        self.save(process_list)

    def add_done(self, done):
        process_list = self.get()

        if "done_list" not in process_list:
            process_list["done_list"] = []

        process_list["done_list"].append(done)

        self.save(process_list)

    def end(self):
        process_list = self.get()
        process_list["end"] = True

        self.save(process_list)
