
class SplitEnd:
    """Event used when the separation of a request into several files is completed"""
    
    NAME = "SPLIT_END"

    def __init__(self, directory):
        self.directory = directory

    def serialize(self):
        return {
            "name": self.NAME,
            "data": {
                "directory": self.directory
            }
        }

    @staticmethod
    def deserialize(serializedHook):
        data = serializedHook["data"]
        directory = data["directory"] if "directory" in data else None

        return SplitEnd(directory)