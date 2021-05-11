
class SplitResultAdded:
    """Event used when a new query file has been created during the separation of a query file"""

    NAME = "SPLIT_RESULT_ADDED"

    def __init__(self, directory, name, date, find):
        self.directory = directory
        self.name = name
        self.date = date
        self.find = find


    def serialize(self):
        return {
            "name": self.NAME,
            "data": {
                "directory": self.directory,
                "name": self.name,
                "date": self.date,
                "find": self.find
            }
        }

    @staticmethod
    def deserialize(serializedHook):
        data = serializedHook["data"]
        directory = data["directory"] if "directory" in data else None
        name = data["name"] if "name" in data else None
        date = data["date"] if "date" in data else None
        find = data["find"] if "find" in data else None

        return SplitResultAdded(directory, name, date, find)