from Patent2Net.app.dex import set_directory_request_data, get_directory_request_data

class ProcessList:
    """represents the data recovery status for a list of queries created after a split"""
    
    KEY = "process_list"

    def __init__(self, directory):
        self.directory = directory

    def get(self):
        return get_directory_request_data(self.directory, self.KEY, {})
    
    def save(self, process_list):
        set_directory_request_data(self.directory, self.KEY, process_list)
    

    def start(self, queue_list, done_list):
        """execute when the process starts"""
        process_list = self.get()

        process_list["start"] = True
        process_list["queue_list"] = queue_list
        process_list["done_list"] = done_list

        self.save(process_list)

    def add_done(self, done):
        """execute when a request is finished"""
        process_list = self.get()

        if "done_list" not in process_list:
            process_list["done_list"] = []

        process_list["done_list"].append(done)

        self.save(process_list)

    def end(self):
        """execute when the process ends"""
        process_list = self.get()
        process_list["end"] = True
        
        self.save(process_list)